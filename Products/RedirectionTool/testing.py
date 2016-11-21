# -*- coding: utf-8 -*-
"""Setup testing fixture."""
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import pkg_resources


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.RedirectionTool
        self.loadZCML(package=Products.RedirectionTool)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'Products.RedirectionTool:default')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='Products.RedirectionTool:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='Products.RedirectionTool:Functional')
