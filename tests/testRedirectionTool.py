#
# Skeleton PloneTestCase
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
import RedirectionToolTestCase
import utils

class TestRedirectionTool(RedirectionToolTestCase.RedirectionToolTestCase):

    # Test helper methods
    def testExtractReferenceFromNonExistingString(self):
        self.failUnlessRaises(NameError, self.rt.extractReference, 'nonexisting')

    def testExtractReferenceFromATObject(self):
        self.loginAsPortalOwner()
        testobj = utils.makeContent(self.portal, 'DDocument', 'testobj')
        reference = self.rt.extractReference(testobj)
        self.failUnless(reference)
        self.failUnlessEqual(reference, testobj.UID())
        self.failUnlessEqual(reference, self.rt.extractReference(testobj.UID()))
        self.failUnlessEqual(reference, self.rt.extractReference('/%s' % self.portal.portal_url.getRelativeContentURL(testobj)))
        self.failUnlessEqual(reference, self.rt.extractReference(self.portal.portal_url.getRelativeContentURL(testobj)))
        self.logout()

    def testExtractReferenceFromNonATObject(self):
        self.loginAsPortalOwner()
        testobj = utils.makeContent(self.portal, 'Document', 'testobj')
        reference = self.rt.extractReference(testobj)
        self.failUnless(reference)
        self.failUnlessEqual(reference, self.rt.extractReference('/%s' % self.portal.portal_url.getRelativeContentURL(testobj)))
        self.failUnlessEqual(reference, self.rt.extractReference(self.portal.portal_url.getRelativeContentURL(testobj)))
        self.logout()

    # Test interface
    def testAddRedirectToNonExisting(self):
        self.failUnlessRaises(NameError, self.rt.addRedirect, '/nonexisting', 'nonexisting')
        self.failUnlessRaises(NameError, self.rt.addRedirect, '/nonexisting', None)

    def testBasicAddRedirectToObjectAndGetRedirect(self):
        self.loginAsPortalOwner()
        testurl = '/testredirect'
        testobj = utils.makeContent(self.portal, 'Document', 'testobj')
        self.failUnless(self.rt.addRedirect(testurl, testobj))
        self.failUnless(self.rt.getRedirect(testurl))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl), testobj)
        self.logout()

    def testBasicAddRedirectToUIDAndGetRedirect(self):
        self.loginAsPortalOwner()
        testurl = '/testredirect'
        testobj = utils.makeContent(self.portal, 'DDocument', 'testobj')
        self.failUnless(self.rt.addRedirect(testurl, testobj.UID()))
        self.failUnless(self.rt.getRedirect(testurl))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl), testobj)
        self.logout()

    def testBasicAddRedirectToPathAndGetRedirect(self):
        self.loginAsPortalOwner()
        testurl = '/testredirect'
        testobj = utils.makeContent(self.portal, 'Document', 'testobj')
        testpath = self.portal.portal_url.getRelativeContentURL(testobj)
        self.failUnless(self.rt.addRedirect(testurl, testpath))
        self.failUnless(self.rt.getRedirect(testurl))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl), testobj)
        self.logout()

    def testAddRedirectToObjectAndGetRedirect(self):
        self.loginAsPortalOwner()
        testid = 'testobj'
        testfolderid = 'testfolder'
        testurl = '/testredirect'
        testfolderurl = '/testfolderredirect'
        testfolder = utils.makeContent(self.portal, 'Folder', testfolderid)
        testobj = utils.makeContent(testfolder, 'Document', testid)
        self.failUnless(self.rt.addRedirect(testurl, testobj))
        self.failUnless(self.rt.getRedirect(testurl))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl), testobj)
        self.failUnless(self.rt.getRedirect(testurl+'/'))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl+'/'), testobj)
        self.failUnless(self.rt.addRedirect(testfolderurl, testfolder))
        self.failUnless(self.rt.getRedirect(testfolderurl))
        self.failUnlessEqual(self.rt.getRedirectObject(testfolderurl), testfolder)
        self.failUnless(self.rt.getRedirect('%s/%s'%(testfolderurl,testid)))
        self.failUnlessEqual(self.rt.getRedirectObject('%s/%s'%(testfolderurl,testid)), testobj)
        self.logout()

    def testAddRedirectToUIDAndGetRedirect(self):
        self.loginAsPortalOwner()
        testid = 'testobj'
        testfolderid = 'testfolder'
        testurl = '/testredirect'
        testfolderurl = '/testfolderredirect'
        testfolder = utils.makeContent(self.portal, 'SimpleFolder', testfolderid)
        testobj = utils.makeContent(testfolder, 'DDocument', testid)
        self.failUnless(self.rt.addRedirect(testurl, testobj.UID()))
        self.failUnless(self.rt.getRedirect(testurl))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl), testobj)
        self.failUnless(self.rt.getRedirect(testurl+'/'))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl+'/'), testobj)
        self.failUnless(self.rt.addRedirect(testfolderurl, testfolder.UID()))
        self.failUnless(self.rt.getRedirect(testfolderurl))
        self.failUnlessEqual(self.rt.getRedirectObject(testfolderurl), testfolder)
        self.failUnless(self.rt.getRedirect('%s/%s'%(testfolderurl,testid)))
        self.failUnlessEqual(self.rt.getRedirectObject('%s/%s'%(testfolderurl,testid)), testobj)
        self.logout()

    def testAddRedirectToPathAndGetRedirect(self):
        #testfolder -+            <--/testfolderredirect
        #            +-testobj    <--/testredirect, /testredirect/
        # 
        self.loginAsPortalOwner()
        testid = 'testobj'
        testfolderid = 'testfolder'
        testurl = '/testredirect'
        testfolderurl = '/testfolderredirect'
        testfolder = utils.makeContent(self.portal, 'Folder', testfolderid)
        testobj = utils.makeContent(testfolder, 'Document', testid)
        self.failUnless(
           self.rt.addRedirect(testurl,
           self.portal.portal_url.getRelativeContentURL(testobj)))
        self.failUnless(self.rt.getRedirect(testurl))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl), testobj)
        self.failUnless(self.rt.getRedirect(testurl+'/'))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl+'/'), testobj)
        self.failUnless(\
          self.rt.addRedirect(testfolderurl, 
          self.portal.portal_url.getRelativeContentURL(testfolder)))
        self.failUnless(self.rt.getRedirect(testfolderurl))
        self.failUnlessEqual(\
          self.rt.getRedirectObject(testfolderurl), testfolder)
        self.failUnless(self.rt.getRedirect('%s/%s'%(testfolderurl,testid)))
        self.failUnlessEqual(\
          self.rt.getRedirectObject('%s/%s'%(testfolderurl,testid)), testobj)
        self.logout()

    def testRemoveNonExisting(self):
        self.loginAsPortalOwner()
        self.failIf(self.rt.removeRedirect('/nonexisting'))
        self.logout()

    def testRemoveRedirect(self):
        self.loginAsPortalOwner()
        testurl = '/testredirect'
        testobj = utils.makeContent(self.portal, 'Document', 'testobj')
        self.rt.addRedirect(testurl, testobj)
        self.failUnless(self.rt.getRedirect(testurl))
        self.failUnless(self.rt.removeRedirect(testurl))
        self.failIf(self.rt.getRedirect(testurl))
        self.logout()

    def testGetRedirectFromNotExisting(self):
        self.failUnless(self.rt.getRedirect('/norealurl') is None)

    def getRedirectsToNonExisting(self):
        pass


if __name__ == '__main__':
    framework()
else:
    # While framework.py provides its own test_suite()
    # method the testrunner utility does not.
    from unittest import TestSuite, makeSuite
    def test_suite():
        suite = TestSuite()
        suite.addTest(makeSuite(TestRedirectionTool))
        return suite
