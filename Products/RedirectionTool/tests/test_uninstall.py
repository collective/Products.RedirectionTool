# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import getToolByName
from Products.RedirectionTool.testing import REDIRECTION_TOOL_INTEGRATION_TESTING  # noqa

import unittest


class TestUninstall(unittest.TestCase):

    layer = REDIRECTION_TOOL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer = getToolByName(self.portal, "portal_quickinstaller")
        self.installer.uninstallProducts(["RedirectionTool"])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if Products.RedirectionTool is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled("RedirectionTool"))

    def test_tool_removed(self):
        self.assertNotIn("portal_redirection", self.portal)

    def test_controlpanel_action_removed(self):
        self.assertNotIn("RedirectionTool", self.portal.portal_controlpanel)
