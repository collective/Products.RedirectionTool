# -*- coding: utf-8 -*-
from plone.app.testing.bbb import PloneTestCase
from Products.RedirectionTool.testing import REDIRECTION_TOOL_INTEGRATION_TESTING

import utils


class TestRedirectionToolSecurity(PloneTestCase):

    layer = REDIRECTION_TOOL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.rt = self.portal.portal_redirection
        self.portal.acl_users._doAddUser("user1", "secret", ["Member"], [])
        self.portal.acl_users._doAddUser("user2", "secret", ["Member"], [])
        self.membership = self.portal.portal_membership
        self.createMemberarea("user1")
        self.createMemberarea("user2")

    def testCheckPermission(self):
        portal_path = self.portal.getPhysicalPath()
        self.login("user1")
        folder = self.membership.getHomeFolder("user1")
        testobj = utils.makeContent(folder, "Document", "testobj")
        folder_path = folder.getPhysicalPath()[len(portal_path):]
        testurl = "/%s/foo" % "/".join(folder_path)
        # user should be able to add redirects to his own objects
        self.assertTrue(self.rt.addRedirect(testurl, testobj))
        self.assertEqual(self.rt.getRedirectObject(testurl), testobj)

        folder = self.membership.getHomeFolder("user2")
        folder_path = folder.getPhysicalPath()[len(portal_path):]
        testurl = "/%s/foo" % "/".join(folder_path)
        # but only if the alias is in a place which belongs to him
        self.assertFalse(self.rt.addRedirect(testurl, testobj))
        self.assertEqual(self.rt.getRedirectObject(testurl), None)
        testurl = "/bar"
        self.assertFalse(self.rt.addRedirect(testurl, testobj))
        self.assertEqual(self.rt.getRedirectObject(testurl), None)
