# -*- coding: utf-8 -*-
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting


class RedirectionToolLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.RedirectionTool

        self.loadZCML(package=Products.RedirectionTool)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "Products.RedirectionTool:default")


REDIRECTION_TOOL_FIXTURE = RedirectionToolLayer()

REDIRECTION_TOOL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(REDIRECTION_TOOL_FIXTURE,), name="Products.RedirectionTool:Integration"
)
