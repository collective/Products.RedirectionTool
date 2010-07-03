import RedirectionToolTestCase
import utils
from Products.CMFPlone.utils import _createObjectByType, base_hasattr
from Products.CMFCore.utils import getToolByName
from BTrees.OOBTree import OOBTree
from zope.component import getUtility
from plone.app.redirector.interfaces import IRedirectionStorage
import logging


class TestRedirectionTool(RedirectionToolTestCase.RedirectionToolTestCase):

    # Test helper methods
    def testExtractReferenceFromNonExistingString(self):
        self.failUnlessRaises(NameError, self.rt.extractReference, 'nonexisting')

    def testExtractReferenceFromATObject(self):
        self.setRoles(['Manager'])
        testobj = utils.makeContent(self.portal, 'Document', 'testobj')
        reference = self.rt.extractReference(testobj)
        self.failUnless(reference)
        self.failUnlessEqual(reference, "/".join(testobj.getPhysicalPath()))
        self.failUnlessEqual(reference, self.rt.extractReference(testobj.UID()))
        self.failUnlessEqual(reference, self.rt.extractReference('/%s' % self.portal.portal_url.getRelativeContentURL(testobj)))
        self.failUnlessEqual(reference, self.rt.extractReference(self.portal.portal_url.getRelativeContentURL(testobj)))
        self.setRoles(['Member'])

    def testExtractReferenceFromNonATObject(self):
        self.setRoles(['Manager'])
        testobj = _createObjectByType('TempFolder', self.portal, 'testobj')
        reference = self.rt.extractReference(testobj)
        self.failUnless(reference)
        self.failUnlessEqual(reference, "/".join(testobj.getPhysicalPath()))
        self.failUnlessEqual(reference, self.rt.extractReference('/%s' % self.portal.portal_url.getRelativeContentURL(testobj)))
        self.failUnlessEqual(reference, self.rt.extractReference(self.portal.portal_url.getRelativeContentURL(testobj)))
        self.setRoles(['Member'])

    # Test interface
    def testAddRedirectToNonExisting(self):
        self.failUnlessRaises(NameError, self.rt.addRedirect, '/nonexisting', 'nonexisting')
        self.failUnlessRaises(NameError, self.rt.addRedirect, '/nonexisting', None)

    def testBasicAddRedirectToObjectAndGetRedirect(self):
        self.setRoles(['Manager'])
        testurl = '/testredirect'
        testobj = utils.makeContent(self.portal, 'Document', 'testobj')
        self.failUnless(self.rt.addRedirect(testurl, testobj))
        self.failUnless(self.rt.getRedirect(testurl))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl), testobj)
        self.setRoles(['Member'])

    def testBasicAddRedirectToUIDAndGetRedirect(self):
        self.setRoles(['Manager'])
        testurl = '/testredirect'
        testobj = utils.makeContent(self.portal, 'Document', 'testobj')
        self.failUnless(self.rt.addRedirect(testurl, testobj.UID()))
        self.failUnless(self.rt.getRedirect(testurl))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl), testobj)
        self.setRoles(['Member'])

    def testBasicAddRedirectToPathAndGetRedirect(self):
        self.setRoles(['Manager'])
        testurl = '/testredirect'
        testobj = utils.makeContent(self.portal, 'Document', 'testobj')
        testpath = self.portal.portal_url.getRelativeContentURL(testobj)
        self.failUnless(self.rt.addRedirect(testurl, testpath))
        self.failUnless(self.rt.getRedirect(testurl))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl), testobj)
        self.setRoles(['Member'])

    def testAddRedirectToObjectAndGetRedirect(self):
        self.setRoles(['Manager'])
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
        self.setRoles(['Member'])

    def testAddRedirectToUIDAndGetRedirect(self):
        self.setRoles(['Manager'])
        testid = 'testobj'
        testfolderid = 'testfolder'
        testurl = '/testredirect'
        testfolderurl = '/testfolderredirect'
        testfolder = utils.makeContent(self.portal, 'Folder', testfolderid)
        testobj = utils.makeContent(testfolder, 'Document', testid)
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
        self.setRoles(['Member'])

    def testAddRedirectToPathAndGetRedirect(self):
        self.setRoles(['Manager'])
        testid = 'testobj'
        testfolderid = 'testfolder'
        testurl = '/testredirect'
        testfolderurl = '/testfolderredirect'
        testfolder = utils.makeContent(self.portal, 'Folder', testfolderid)
        testobj = utils.makeContent(testfolder, 'Document', testid)
        self.failUnless(self.rt.addRedirect(testurl, self.portal.portal_url.getRelativeContentURL(testobj)))
        self.failUnless(self.rt.getRedirect(testurl))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl), testobj)
        self.failUnless(self.rt.getRedirect(testurl+'/'))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl+'/'), testobj)
        self.failUnless(self.rt.addRedirect(testfolderurl, self.portal.portal_url.getRelativeContentURL(testfolder)))
        self.failUnless(self.rt.getRedirect(testfolderurl))
        self.failUnlessEqual(self.rt.getRedirectObject(testfolderurl), testfolder)
        self.failUnless(self.rt.getRedirect('%s/%s'%(testfolderurl,testid)))
        self.failUnlessEqual(self.rt.getRedirectObject('%s/%s'%(testfolderurl,testid)), testobj)
        self.setRoles(['Member'])

    def testRemoveNonExisting(self):
        self.setRoles(['Manager'])
        self.failIf(self.rt.removeRedirect('/nonexisting'))
        self.setRoles(['Member'])

    def testRemoveRedirect(self):
        self.setRoles(['Manager'])
        testurl = '/testredirect'
        testobj = utils.makeContent(self.portal, 'Document', 'testobj')
        self.rt.addRedirect(testurl, testobj)
        self.failUnless(self.rt.getRedirect(testurl))
        self.failUnless(self.rt.removeRedirect(testurl))
        self.failIf(self.rt.getRedirect(testurl))
        self.setRoles(['Member'])

    def testGetRedirectFromNotExisting(self):
        self.failUnless(self.rt.getRedirect('/norealurl') is None)


class TestRedirectionToolMigration(RedirectionToolTestCase.RedirectionToolTestCase):
    def afterSetUp(self):
        RedirectionToolTestCase.RedirectionToolTestCase.afterSetUp(self)
        self.rt._redirectionmap = OOBTree()
        self.rt._reverse_redirectionmap = OOBTree()

    def testOldStorageRemoved(self):
        logger = logging.getLogger("RedirectionTool")
        self.rt.migrateStorage(logger)
        self.failIf(base_hasattr(self.rt, '_redirectionmap'))
        self.failIf(base_hasattr(self.rt, '_reverse_redirectionmap'))

    def testRepeatedMigrationDoesntFail(self):
        logger = logging.getLogger("RedirectionTool")
        self.rt.migrateStorage(logger)
        self.rt.migrateStorage(logger)

    def testMigrationOfUIDs(self):
        logger = logging.getLogger("RedirectionTool")
        storage = getUtility(IRedirectionStorage)
        self.setRoles(['Manager'])
        testurl = '/testredirect'
        testobj = utils.makeContent(self.portal, 'Document', 'testobj')
        self.rt._redirectionmap[testurl] = testobj.UID()

        self.assertEquals(self.rt.getRedirect(testurl), None)
        self.assertEquals(storage.get('/plone%s' % testurl), None)

        self.rt.migrateStorage(logger)

        self.assertEquals(self.rt.getRedirectObject(testurl), testobj)
        self.assertEquals(storage.get('/plone%s' % testurl), "/".join(testobj.getPhysicalPath()))

    def testMigrationOfPaths(self):
        logger = logging.getLogger("RedirectionTool")
        storage = getUtility(IRedirectionStorage)
        urltool = getToolByName(self.portal, 'portal_url')
        self.setRoles(['Manager'])
        testurl = '/testredirect'
        testobj = utils.makeContent(self.portal, 'Document', 'testobj')
        path = '/%s' % urltool.getRelativeContentURL(testobj)
        self.rt._redirectionmap[testurl] = path

        self.assertEquals(self.rt.getRedirect(testurl), None)
        self.assertEquals(storage.get('/plone%s' % testurl), None)

        self.rt.migrateStorage(logger)

        self.assertEquals(self.rt.getRedirectObject(testurl), testobj)
        self.assertEquals(storage.get('/plone%s' % testurl), "/".join(testobj.getPhysicalPath()))

    def testMigrationOfBrokenRedirect(self):
        logger = logging.getLogger("RedirectionTool")
        storage = getUtility(IRedirectionStorage)
        self.setRoles(['Manager'])
        testurl = '/testredirect'
        self.rt._redirectionmap[testurl] = "foobar"

        self.assertEquals(self.rt.getRedirect(testurl), None)
        self.assertEquals(storage.get('/plone%s' % testurl), None)

        self.rt.migrateStorage(logger)

        self.assertEquals(self.rt.getRedirect(testurl), None)
        self.assertEquals(storage.get('/plone%s' % testurl), None)
        self.failIf(base_hasattr(self.rt, '_redirectionmap'))
        self.failIf(base_hasattr(self.rt, '_reverse_redirectionmap'))


from unittest import TestSuite, makeSuite
def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestRedirectionTool))
    suite.addTest(makeSuite(TestRedirectionToolMigration))
    return suite
