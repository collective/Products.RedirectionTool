from Testing import ZopeTestCase
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Products.CMFPlone.tests import PloneTestCase
import time
import utils

ZopeTestCase.installProduct('Archetypes')
ZopeTestCase.installProduct('PortalTransforms')
ZopeTestCase.installProduct('MimetypesRegistry')
ZopeTestCase.installProduct('RedirectionTool')


class RedirectionToolTestCase(PloneTestCase.PloneTestCase):
    def afterSetUp(self):
#        self.refreshSkinData()
        self.loginPortalOwner()
        utils.disableScriptValidators(self.portal)

        self.rt = self.portal.portal_redirection
        
        self.logout()
        
def setupRedirectionTool(app, quiet=0):
    get_transaction().begin()
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
    # Add Archetypes (need the archetypestool) - use Install method directly until quickinstaller takes arguments
#    app.portal.portal_quickinstaller.installProduct('Archetypes', include_demo=1)
    from Products.Archetypes.Extensions.Install import install as installArchetypes
    installArchetypes(app.portal, include_demo=1)


    # Log out
    noSecurityManager()
    get_transaction().commit()
    if not quiet: ZopeTestCase._print('done (%.3fs)\n' % (time.time()-_start,))

app = ZopeTestCase.app()
setupRedirectionTool(app)
ZopeTestCase.close(app)