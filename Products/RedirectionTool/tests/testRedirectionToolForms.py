from Products.PloneTestCase import PloneTestCase
import RedirectionToolTestCase
from Products.Five.testbrowser import Browser
from Products.PloneTestCase.setup import portal_owner, default_password


class TestRedirectionToolForms(RedirectionToolTestCase.RedirectionToolTestCase,
                               PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        RedirectionToolTestCase.RedirectionToolTestCase.afterSetUp(self)

    def testSecurity(self):
        browser = Browser()
        portal_url = self.portal.absolute_url()
        url = portal_url + '/@@manage-aliases'
        browser.open(url)
        self.assertNotEquals(url, browser.url)
        browser.addHeader("Authorization", "Basic %s:%s" % (portal_owner, default_password))
        browser.open(url)
        self.assertEquals(url, browser.url)

    def testAliasesTab(self):
        browser = Browser()
        browser.addHeader("Authorization", "Basic %s:%s" % (portal_owner, default_password))
        browser.open(self.portal.absolute_url())
        aliases = browser.getLink(text='Aliases')
        self.failUnless('@@manage-aliases' in aliases.url)

    def testAddingAlias(self):
        browser = Browser()
        browser.addHeader("Authorization", "Basic %s:%s" % (portal_owner, default_password))
        portal_url = self.portal.absolute_url()
        url = portal_url + '/@@manage-aliases'
        browser.open(url)
        control = browser.getControl(name='redirection')
        control.value = '/bar'
        browser.getControl(name='form.button.Add').click()
        self.failUnless('Alias added' in browser.contents)
        self.assertEquals(self.rt.getRedirectObject('/bar'), self.portal)


from unittest import TestSuite, makeSuite
def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestRedirectionToolForms))
    return suite
