from Products.PloneTestCase import PloneTestCase
import utils
import zope.deprecation

PloneTestCase.setupPloneSite(products=['RedirectionTool'])


class RedirectionToolTestCase(PloneTestCase.PloneTestCase):
    def afterSetUp(self):
        zope.deprecation.__show__.off()
        utils.disableScriptValidators(self.portal)

        self.rt = self.portal.portal_redirection

    def afterTearDown(self):
        zope.deprecation.__show__.on()
