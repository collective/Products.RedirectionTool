from Products.PloneTestCase import PloneTestCase
import utils

PloneTestCase.installProduct('Archetypes')
PloneTestCase.installProduct('PortalTransforms')
PloneTestCase.installProduct('MimetypesRegistry')
PloneTestCase.installProduct('RedirectionTool')


class RedirectionToolTestCase(PloneTestCase.PloneTestCase):
    def afterSetUp(self):
        utils.disableScriptValidators(self.portal)

        self.rt = self.portal.portal_redirection


PloneTestCase.setupPloneSite(products=['RedirectionTool'])
