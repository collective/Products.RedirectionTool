from Testing import ZopeTestCase
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
import time
import utils
import transaction

ZopeTestCase.installProduct('Archetypes')
ZopeTestCase.installProduct('PortalTransforms')
ZopeTestCase.installProduct('MimetypesRegistry')
ZopeTestCase.installProduct('RedirectionTool')

from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.Archetypes.Extensions.Install import install as installArchetypes

class RedirectionToolTestCase(PloneTestCase):
    def afterSetUp(self):
#        self.refreshSkinData()
        self.loginAsPortalOwner()

        #
        # setupRedirectionTool
        # Until Plone 2.5.2, this was done once and committed 
        # by the setupRedirectionTool method, below.
        # Moved here because of a problem getting the old mechanism working.
        # 
        uf = self.portal.acl_users
        # setup
        uf._doAddUser('PloneMember', '', ['Members'], [])
        uf._doAddUser('PloneManager', '', ['Manager'], [])
        # login as manager
        user = uf.getUserById('PloneManager').__of__(uf)
        newSecurityManager(None, user)

        # Add Redirection Tool
        self.portal.portal_quickinstaller.installProduct('RedirectionTool')
        installArchetypes(self.portal, include_demo=1)
        # Log out
        noSecurityManager()
        # /setupRedirectionTool
        # 

        self.rt = self.portal.portal_redirection
        self.logout()
                
def setupRedirectionTool(app, quiet=0):
    transaction.get()
    _start = time.time()
    if not quiet: ZopeTestCase._print('Adding Redirection Tool ... ')

    uf = app.portal.acl_users
    # setup
    uf._doAddUser('PloneMember', '', ['Members'], [])
    uf._doAddUser('PloneManager', '', ['Manager'], [])
    # login as manager
    user = uf.getUserById('PloneManager').__of__(uf)
    newSecurityManager(None, user)
    
    # Add Redirection Tool
    app.portal.portal_quickinstaller.installProduct('RedirectionTool')
    installArchetypes(app.portal, include_demo=1)

    # Log out
    noSecurityManager()
    transaction.get().commit()
    if not quiet: ZopeTestCase._print('done (%.3fs)\n' % (time.time()-_start,))
