#
# Skeleton PloneTestCase
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
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
        self.login('user1')
        folder = self.membership.getHomeFolder('user1')
        testobj = utils.makeContent(folder, 'Document', 'testobj')
        self.failUnless(self.rt.checkPermission('Modify portal content', testobj))
        self.failUnless(self.rt.checkPermission('Modify portal content', testobj.UID()))
        self.failUnless(self.rt.checkPermission('Modify portal content', self.portal.portal_url.getRelativeContentURL(testobj)))
        testobj.manage_permission('Modify portal content', ['Manager',], 0)
        self.logout()
        self.login('user2')
        self.failIf(self.rt.checkPermission('Modify portal content', testobj))
        self.failIf(self.rt.checkPermission('Modify portal content', testobj.UID()))
        self.failIf(self.rt.checkPermission('Modify portal content', self.portal.portal_url.getRelativeContentURL(testobj)))
        self.logout()

    def testAddRedirectNotAllowed(self):
        pass

    def testRemoveRedirectNotAllowed(self):
        pass

    def testIsRedirectionAllowedFor(self):
        pass

    def testIsRedirectionAllowedForNotAllowed(self):
        pass

    def testGetRedirectFromNotAllowed(self):
        pass

if __name__ == '__main__':
    framework()
else:
    # While framework.py provides its own test_suite()
    # method the testrunner utility does not.
    from unittest import TestSuite, makeSuite
    def test_suite():
        suite = TestSuite()
        suite.addTest(makeSuite(TestRedirectionToolSecurity))
        return suite
