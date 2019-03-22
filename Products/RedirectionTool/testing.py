# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing import z2


class RedirectionToolLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.RedirectionTool

        self.loadZCML(package=Products.RedirectionTool)
        z2.installProduct(app, "Products.Archetypes")
        z2.installProduct(app, "Products.ATContentTypes")

    def setUpPloneSite(self, portal):

        self.applyProfile(portal, "Products.RedirectionTool:default")
        if portal.portal_setup.profileExists("Products.ATContentTypes:default"):
            applyProfile(portal, "Products.ATContentTypes:default")

        portal.acl_users.userFolderAddUser(
            SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ["Manager"], []
        )


REDIRECTION_TOOL_FIXTURE = RedirectionToolLayer()

REDIRECTION_TOOL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(REDIRECTION_TOOL_FIXTURE,), name="Products.RedirectionTool:Integration"
)

REDIRECTION_TOOL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(REDIRECTION_TOOL_FIXTURE,), name="Products.RedirectionTool:Functional"
)
