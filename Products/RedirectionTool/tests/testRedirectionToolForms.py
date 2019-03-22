# -*- coding: utf-8 -*-
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
from Products.RedirectionTool.testing import REDIRECTION_TOOL_FUNCTIONAL_TESTING

import unittest


class TestRedirectionToolForms(unittest.TestCase):
    layer = REDIRECTION_TOOL_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.rt = self.portal.portal_redirection

    def testSecurity(self):
        browser = Browser(self.portal)
        portal_url = self.portal.absolute_url()
        url = portal_url + "/@@manage-aliases"
        browser.open(url)
        self.assertNotEquals(url, browser.url)
        browser.addHeader(
            "Authorization", "Basic %s:%s" % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        browser.open(url)
        self.assertEqual(url, browser.url)

    def testAliasesTab(self):
        browser = Browser(self.portal)
        browser.addHeader(
            "Authorization", "Basic %s:%s" % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        browser.open(self.portal.absolute_url())
        aliases = browser.getLink(text="Aliases")
        self.assertTrue("@@manage-aliases" in aliases.url)

    def testAddingAlias(self):
        browser = Browser(self.portal)
        browser.addHeader(
            "Authorization", "Basic %s:%s" % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        portal_url = self.portal.absolute_url()
        url = portal_url + "/@@manage-aliases"
        browser.open(url)
        control = browser.getControl(name="redirection")
        control.value = "/bar"
        browser.getControl(name="form.button.Add").click()
        self.assertTrue("Alias added" in browser.contents)
        self.assertEqual(self.rt.getRedirectObject("/bar"), self.portal)
