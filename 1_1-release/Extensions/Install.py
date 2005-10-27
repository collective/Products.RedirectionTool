# Copyright (C) 2004 
# Plone Solutions AS <info@plonesolutions.com>
#  http://www.plonesolutions.com
#
# Learning Lab Denmark
#  http://www.lld.dk
"""\
$id$

This file is an installation script for RedirectionTool.  
It is meant to be used as an External Method.  To use, add an external 
method to the root of the Plone Site that you want the tool registered 
in with the configuration:

 id: install_redirectiontool
 title: Install Redirection Tool*optional*
 module name: RedirectionTool.Install
 function name: install

Then go to the management screen for the newly added external method
and click the 'Try it' tab.  The install function will execute and give
information about the steps it took to register and install the
PloneboardDiscussionTool into the Plone Site instance. 
"""

from Products.RedirectionTool import RedirectionTool, redirection_tool_globals

from Products.CMFCore.TypesTool import ContentFactoryMetadata
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import ManagePortal

from cStringIO import StringIO
import string

configlets = \
( { 'id'         : 'RedirectionTool'
  , 'name'       : 'Redirection and Aliases'
  , 'action'     : 'string:${portal_url}/prefs_redirection_tool_form'
  , 'category'   : 'Products'
  , 'appId'      : 'RedirectionTool'
  , 'permission' : ManagePortal
  , 'imageUrl'  : 'action_icon.gif'
  }
,
)

def setupTypesandSkins(self, out):
    # If there already is a redirection tool we leave it to avoid deleting existing redirection table
    if not getToolByName(self, 'portal_redirection', None):
        addTool = self.manage_addProduct['RedirectionTool'].manage_addTool
        addTool('Redirection Tool')
        out.write('Adding Redirection Tool\n')
    else:
        out.write('Redirection Tool already existed, skipping...\n')
    
    typesTool = getToolByName(self, 'portal_types')
    skinsTool = getToolByName(self, 'portal_skins')
    
    # Add directory views
    try:  
        addDirectoryViews(skinsTool, 'skins', redirection_tool_globals)
        out.write( "Added directory views to portal_skins.\n" )
    except:
        out.write( '*** Unable to add directory views to portal_skins.\n')

    # Go through the skin configurations and insert 'redirection_tool'
    skins = skinsTool.getSkinSelections()
    for skin in skins:
        path = skinsTool.getSkinPath(skin)
        path = map(string.strip, string.split(path,','))
        changed = 0
        if 'redirection_tool' not in path:
            try: 
                path.insert(path.index('custom')+1, 'redirection_tool')
                changed = 1
            except ValueError:
                path.append('redirection_tool')
                changed = 1

        if changed:        
            path = string.join(path, ', ')
            # addSkinSelection will replace existing skins as well.
            skinsTool.addSkinSelection(skin, path)
            out.write("Added 'redirection_tool' to %s skin\n" % skin)
        else:
            out.write("Skipping %s skin, 'redirection_tool' already set up\n" % skin)

def addPortalProperties(self, out):
    pass

def addConfiglets(self, out):
    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            out.write('Adding configlet %s\n' % conf['id'])
            configTool.registerConfiglet(**conf)

def addMemberProperties(self, out):
    pass

def registerActionProvider(self, out):
    actionTool = getToolByName(self, 'portal_actions', None)
    if actionTool:
        actionTool.addActionProvider('portal_redirection')
        out.write('Registered action provider\n')
    

def install(self):
    out=StringIO()

    setupTypesandSkins(self, out)
    addPortalProperties(self, out)
    addConfiglets(self, out)
    addMemberProperties(self, out)
    registerActionProvider(self, out)
    out.write('Installation completed.\n')
    return out.getvalue()

#
# Uninstall methods
#

def removeConfiglets(self, out):
    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            out.write('Removing configlet %s\n' % conf['id'])
            configTool.unregisterConfiglet(conf['id'])

def unregisterActionProvider(self, out):
    actionTool = getToolByName(self, 'portal_actions', None)
    if actionTool:
        actionTool.deleteActionProvider('portal_redirection')
        out.write('Removed action provider\n')

# The uninstall is used by the CMFQuickInstaller for uninstalling.
# CMFQuickInstaller uninstalls skins.
def uninstall(self):
    out=StringIO()
#    removeTool(self, out)
    removeConfiglets(self, out)
    unregisterActionProvider(self, out)
    return out.getvalue()