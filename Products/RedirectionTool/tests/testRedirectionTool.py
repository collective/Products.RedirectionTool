# -*- coding: utf-8 -*-
from BTrees.OOBTree import OOBTree
from plone.app.redirector.interfaces import IRedirectionStorage
from plone.app.testing import login
from plone.app.testing import SITE_OWNER_NAME
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.utils import base_hasattr
from Products.RedirectionTool import setuphandlers
from Products.RedirectionTool.testing import REDIRECTION_TOOL_INTEGRATION_TESTING
from zope.component import getUtility

import logging
import unittest
import utils


class TestRedirectionTool(unittest.TestCase):

    layer = REDIRECTION_TOOL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.rt = self.portal.portal_redirection

    # Test helper methods
    def testExtractReferenceFromNonExistingString(self):
        self.assertRaises(NameError, self.rt.extractReference, "nonexisting")

    def testExtractReferenceFromATObject(self):
        login(self.portal, SITE_OWNER_NAME)
        testobj = utils.makeContent(self.portal, "Document", "testobj")
        reference = self.rt.extractReference(testobj)
        self.assertTrue(reference)
        self.assertEqual(reference, "/".join(testobj.getPhysicalPath()))
        self.assertEqual(reference, self.rt.extractReference(testobj.UID()))
        self.assertEqual(
            reference,
            self.rt.extractReference(
                "/%s" % self.portal.portal_url.getRelativeContentURL(testobj)
            ),
        )
        self.assertEqual(
            reference,
            self.rt.extractReference(
                self.portal.portal_url.getRelativeContentURL(testobj)
            ),
        )

    def testExtractReferenceFromNonATObject(self):
        login(self.portal, SITE_OWNER_NAME)
        testobj = _createObjectByType("TempFolder", self.portal, "testobj")
        reference = self.rt.extractReference(testobj)
        self.assertTrue(reference)
        self.assertEqual(reference, "/".join(testobj.getPhysicalPath()))
        self.assertEqual(
            reference,
            self.rt.extractReference(
                "/%s" % self.portal.portal_url.getRelativeContentURL(testobj)
            ),
        )
        self.assertEqual(
            reference,
            self.rt.extractReference(
                self.portal.portal_url.getRelativeContentURL(testobj)
            ),
        )

    # Test interface
    def testAddRedirectToNonExisting(self):
        self.assertRaises(NameError, self.rt.addRedirect, "/nonexisting", "nonexisting")
        self.assertRaises(NameError, self.rt.addRedirect, "/nonexisting", None)

    def testBasicAddRedirectToObjectAndGetRedirect(self):
        login(self.portal, SITE_OWNER_NAME)
        testurl = "/testredirect"
        testobj = utils.makeContent(self.portal, "Document", "testobj")
        self.assertTrue(self.rt.addRedirect(testurl, testobj))
        self.assertTrue(self.rt.getRedirect(testurl))
        self.assertEqual(self.rt.getRedirectObject(testurl), testobj)

    def testBasicAddRedirectToUIDAndGetRedirect(self):
        login(self.portal, SITE_OWNER_NAME)
        testurl = "/testredirect"
        testobj = utils.makeContent(self.portal, "Document", "testobj")
        self.assertTrue(self.rt.addRedirect(testurl, testobj.UID()))
        self.assertTrue(self.rt.getRedirect(testurl))
        self.assertEqual(self.rt.getRedirectObject(testurl), testobj)

    def testBasicAddRedirectToPathAndGetRedirect(self):
        login(self.portal, SITE_OWNER_NAME)
        testurl = "/testredirect"
        testobj = utils.makeContent(self.portal, "Document", "testobj")
        testpath = self.portal.portal_url.getRelativeContentURL(testobj)
        self.assertTrue(self.rt.addRedirect(testurl, testpath))
        self.assertTrue(self.rt.getRedirect(testurl))
        self.assertEqual(self.rt.getRedirectObject(testurl), testobj)

    def testAddRedirectToObjectAndGetRedirect(self):
        login(self.portal, SITE_OWNER_NAME)
        testid = "testobj"
        testfolderid = "testfolder"
        testurl = "/testredirect"
        testfolderurl = "/testfolderredirect"
        testfolder = utils.makeContent(self.portal, "Folder", testfolderid)
        testobj = utils.makeContent(testfolder, "Document", testid)
        self.assertTrue(self.rt.addRedirect(testurl, testobj))
        self.assertTrue(self.rt.getRedirect(testurl))
        self.assertEqual(self.rt.getRedirectObject(testurl), testobj)
        self.assertTrue(self.rt.getRedirect(testurl + "/"))
        self.assertEqual(self.rt.getRedirectObject(testurl + "/"), testobj)
        self.assertTrue(self.rt.addRedirect(testfolderurl, testfolder))
        self.assertTrue(self.rt.getRedirect(testfolderurl))
        self.assertEqual(self.rt.getRedirectObject(testfolderurl), testfolder)
        self.assertTrue(self.rt.getRedirect("%s/%s" % (testfolderurl, testid)))
        self.assertEqual(
            self.rt.getRedirectObject("%s/%s" % (testfolderurl, testid)), testobj
        )

    def testAddRedirectToUIDAndGetRedirect(self):
        login(self.portal, SITE_OWNER_NAME)
        testid = "testobj"
        testfolderid = "testfolder"
        testurl = "/testredirect"
        testfolderurl = "/testfolderredirect"
        testfolder = utils.makeContent(self.portal, "Folder", testfolderid)
        testobj = utils.makeContent(testfolder, "Document", testid)
        self.assertTrue(self.rt.addRedirect(testurl, testobj.UID()))
        self.assertTrue(self.rt.getRedirect(testurl))
        self.assertEqual(self.rt.getRedirectObject(testurl), testobj)
        self.assertTrue(self.rt.getRedirect(testurl + "/"))
        self.assertEqual(self.rt.getRedirectObject(testurl + "/"), testobj)
        self.assertTrue(self.rt.addRedirect(testfolderurl, testfolder.UID()))
        self.assertTrue(self.rt.getRedirect(testfolderurl))
        self.assertEqual(self.rt.getRedirectObject(testfolderurl), testfolder)
        self.assertTrue(self.rt.getRedirect("%s/%s" % (testfolderurl, testid)))
        self.assertEqual(
            self.rt.getRedirectObject("%s/%s" % (testfolderurl, testid)), testobj
        )

    def testAddRedirectToPathAndGetRedirect(self):
        login(self.portal, SITE_OWNER_NAME)
        testid = "testobj"
        testfolderid = "testfolder"
        testurl = "/testredirect"
        testfolderurl = "/testfolderredirect"
        testfolder = utils.makeContent(self.portal, "Folder", testfolderid)
        testobj = utils.makeContent(testfolder, "Document", testid)
        self.assertTrue(
            self.rt.addRedirect(
                testurl, self.portal.portal_url.getRelativeContentURL(testobj)
            )
        )
        self.assertTrue(self.rt.getRedirect(testurl))
        self.assertEqual(self.rt.getRedirectObject(testurl), testobj)
        self.assertTrue(self.rt.getRedirect(testurl + "/"))
        self.assertEqual(self.rt.getRedirectObject(testurl + "/"), testobj)
        self.assertTrue(
            self.rt.addRedirect(
                testfolderurl, self.portal.portal_url.getRelativeContentURL(testfolder)
            )
        )
        self.assertTrue(self.rt.getRedirect(testfolderurl))
        self.assertEqual(self.rt.getRedirectObject(testfolderurl), testfolder)
        self.assertTrue(self.rt.getRedirect("%s/%s" % (testfolderurl, testid)))
        self.assertEqual(
            self.rt.getRedirectObject("%s/%s" % (testfolderurl, testid)), testobj
        )

    def testRemoveNonExisting(self):
        login(self.portal, SITE_OWNER_NAME)
        self.assertFalse(self.rt.removeRedirect("/nonexisting"))

    def testRemoveRedirect(self):
        login(self.portal, SITE_OWNER_NAME)
        testurl = "/testredirect"
        testobj = utils.makeContent(self.portal, "Document", "testobj")
        self.rt.addRedirect(testurl, testobj)
        self.assertTrue(self.rt.getRedirect(testurl))
        self.assertTrue(self.rt.removeRedirect(testurl))
        self.assertFalse(self.rt.getRedirect(testurl))

    def testGetRedirectFromNotExisting(self):
        self.assertTrue(self.rt.getRedirect("/norealurl") is None)


class TestRedirectionToolMigration(unittest.TestCase):
    layer = REDIRECTION_TOOL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.rt = self.portal.portal_redirection

        self.rt._redirectionmap = OOBTree()
        self.rt._reverse_redirectionmap = OOBTree()

    def testOldStorageRemoved(self):
        logger = logging.getLogger("RedirectionTool")
        self.rt.migrateStorage(logger)
        self.assertFalse(base_hasattr(self.rt, "_redirectionmap"))
        self.assertFalse(base_hasattr(self.rt, "_reverse_redirectionmap"))

    def testRepeatedMigrationDoesntFail(self):
        logger = logging.getLogger("RedirectionTool")
        self.rt.migrateStorage(logger)
        self.rt.migrateStorage(logger)

    def testMigrationOfUIDs(self):
        logger = logging.getLogger("RedirectionTool")
        storage = getUtility(IRedirectionStorage)
        login(self.portal, SITE_OWNER_NAME)
        testurl = "/testredirect"
        testobj = utils.makeContent(self.portal, "Document", "testobj")
        self.rt._redirectionmap[testurl] = testobj.UID()

        self.assertEqual(self.rt.getRedirect(testurl), None)
        self.assertEqual(storage.get("/plone%s" % testurl), None)

        self.rt.migrateStorage(logger)

        self.assertEqual(self.rt.getRedirectObject(testurl), testobj)
        self.assertEqual(
            storage.get("/plone%s" % testurl), "/".join(testobj.getPhysicalPath())
        )

    def testMigrationOfPaths(self):
        logger = logging.getLogger("RedirectionTool")
        storage = getUtility(IRedirectionStorage)
        urltool = getToolByName(self.portal, "portal_url")
        login(self.portal, SITE_OWNER_NAME)
        testurl = "/testredirect"
        testobj = utils.makeContent(self.portal, "Document", "testobj")
        path = "/%s" % urltool.getRelativeContentURL(testobj)
        self.rt._redirectionmap[testurl] = path

        self.assertEqual(self.rt.getRedirect(testurl), None)
        self.assertEqual(storage.get("/plone%s" % testurl), None)

        self.rt.migrateStorage(logger)

        self.assertEqual(self.rt.getRedirectObject(testurl), testobj)
        self.assertEqual(
            storage.get("/plone%s" % testurl), "/".join(testobj.getPhysicalPath())
        )

    def testMigrationOfBrokenRedirect(self):
        logger = logging.getLogger("RedirectionTool")
        storage = getUtility(IRedirectionStorage)
        login(self.portal, SITE_OWNER_NAME)
        testurl = "/testredirect"
        self.rt._redirectionmap[testurl] = "foobar"

        self.assertEqual(self.rt.getRedirect(testurl), None)
        self.assertEqual(storage.get("/plone%s" % testurl), None)

        self.rt.migrateStorage(logger)

        self.assertEqual(self.rt.getRedirect(testurl), None)
        self.assertEqual(storage.get("/plone%s" % testurl), None)
        self.assertFalse(base_hasattr(self.rt, "_redirectionmap"))
        self.assertFalse(base_hasattr(self.rt, "_reverse_redirectionmap"))


class TestRedirectionToolUpgrades(unittest.TestCase):
    layer = REDIRECTION_TOOL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

    def testControlPanelUpgrade(self):
        cptool = getToolByName(self.portal, "portal_controlpanel")
        configlet = cptool.getActionObject("Products/RedirectionTool")

        # Plone versions < 4 don't have this
        if hasattr(configlet, "icon_expr"):
            # Fake a pre-upgrade state without icon expression
            configlet.setIconExpression("")
            self.assertEqual(configlet.icon_expr, "")

            setuphandlers.upgrade_controlpanel(self.portal)

            new_configlet = cptool.getActionObject("Products/RedirectionTool")
            self.assertFalse(new_configlet.icon_expr == "")
