from Products.CMFCore.utils import getToolByName


def importVarious(context):
    """Manual steps not yet covered by GS."""
    if context.readDataFile('redirectiontool-various.txt') is None:
        return

    site=context.getSite()
    logger = context.getLogger("RedirectionTool")

    removeActionProvider(site, logger)
    removeSkin(site, logger)
    migrateStorage(site, logger)


def removeActionProvider(site, logger):
    actionTool = getToolByName(site, 'portal_actions', None)
    if actionTool is not None:
        actionTool.deleteActionProvider('portal_redirection')
        logger.info('Removed action provider\n')


def removeSkin(site, logger):
    skinsTool = getToolByName(site, 'portal_skins')
    # Go through the skin configurations and remove 'redirection_tool'
    skins = skinsTool.getSkinSelections()
    for skin in skins:
        path = skinsTool.getSkinPath(skin)
        path = [x.strip() for x in path.split(',')]
        changed = 0
        new_path = []
        for layer in path:
            if layer == 'redirection_tool':
                changed = 1
            else:
                new_path.append(layer)

        if changed:
            new_path = ', '.join(new_path)
            # addSkinSelection will replace existing skins as well.
            skinsTool.addSkinSelection(skin, new_path)
            logger.info("Removed 'redirection_tool' from %s skin\n" % skin)
        else:
            logger.info("Skipping %s skin, 'redirection_tool' was not installed in it\n" % skin)


def migrateStorage(site, logger):
    rt = getToolByName(site, 'portal_redirection')
    logger.info("Migrating any existing redirects.")
    rt.migrateStorage(logger)
