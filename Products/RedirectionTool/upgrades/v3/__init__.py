# -*- coding: utf-8 -*-
from Products.RedirectionTool.logger import logger
from Products.CMFCore.utils import getToolByName

TOOLS = ('portal_actions', 'portal_controlpanel')


def fix_i18n_domain(setup_tool):
    """Fix i18n domain."""
    for name in TOOLS:
        tool = getToolByName(setup_tool, name)
        tool.i18ndomain = 'Products.RedirectionTool'
    logger.info('i18n domain was fixed')
