# -*- coding: utf-8 -*-
from Products.RedirectionTool.testing import INTEGRATION_TESTING

import unittest


class UpgradeTestCaseBase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.profile_id = u'Products.RedirectionTool:default'
        self.from_version = from_version
        self.to_version = to_version

    def get_upgrade_step(self, title):
        """Get the named upgrade step."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def execute_upgrade_step(self, step):
        """Execute an upgrade step."""
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    @property
    def total_steps(self):
        """Return the number of steps in the upgrade."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        assert len(upgrades) > 0
        return len(upgrades[0])


class To3TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'2', u'3')

    def test_total_steps(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(version, self.to_version)
        self.assertEqual(self.total_steps, 1)

    def test_fix_i18n_domain(self):
        title = u'Fix i18n domain'
        step = self.get_upgrade_step(title)
        assert step is not None

        # simulate state on previous version
        from Products.CMFCore.utils import getToolByName
        from Products.RedirectionTool.upgrades.v3 import TOOLS
        for name in TOOLS:
            tool = getToolByName(self.portal, name)
            tool.i18ndomain = 'RedirectionTool'

        # execute upgrade step and verify changes were applied
        self.execute_upgrade_step(step)

        for name in TOOLS:
            tool = getToolByName(self.portal, name)
            self.assertEqual(tool.i18ndomain, 'Products.RedirectionTool')
