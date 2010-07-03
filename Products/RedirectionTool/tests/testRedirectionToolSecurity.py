import RedirectionToolTestCase
import utils

class TestRedirectionToolSecurity(RedirectionToolTestCase.RedirectionToolTestCase):

    def afterSetUp(self):
        RedirectionToolTestCase.RedirectionToolTestCase.afterSetUp(self)
        self.portal.acl_users._doAddUser('user1', 'secret', ['Member'], [])
        self.portal.acl_users._doAddUser('user2', 'secret', ['Member'], [])
        self.membership = self.portal.portal_membership
        self.createMemberarea('user1')
        self.createMemberarea('user2')

    def testCheckPermission(self):
        portal_path = self.portal.getPhysicalPath()
        self.login('user1')
        folder = self.membership.getHomeFolder('user1')
        testobj = utils.makeContent(folder, 'Document', 'testobj')
        folder_path = folder.getPhysicalPath()[len(portal_path):]
        testurl = '/%s/foo' % '/'.join(folder_path)
        # user should be able to add redirects to his own objects
        self.failUnless(self.rt.addRedirect(testurl, testobj))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl), testobj)

        folder = self.membership.getHomeFolder('user2')
        folder_path = folder.getPhysicalPath()[len(portal_path):]
        testurl = '/%s/foo' % '/'.join(folder_path)
        # but only if the alias is in a place which belongs to him
        self.failIf(self.rt.addRedirect(testurl, testobj))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl), None)
        testurl = '/bar'
        self.failIf(self.rt.addRedirect(testurl, testobj))
        self.failUnlessEqual(self.rt.getRedirectObject(testurl), None)


from unittest import TestSuite, makeSuite
def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestRedirectionToolSecurity))
    return suite
