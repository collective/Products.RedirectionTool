"""
$Id: __init__.py,v 1.1 2004/02/08 11:52:25 tesdal Exp $
"""

from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import ToolInit, ContentInit
from Products.CMFCore.DirectoryView import registerDirectory

import RedirectionTool

redirection_tool_globals=globals()

# Make the skins available as DirectoryViews.
registerDirectory('skins', redirection_tool_globals)

def initialize( context ):
    
    ToolInit('Redirection Tool', 
            tools=(RedirectionTool.RedirectionTool, ), 
            product_name='RedirectionTool',
            icon='tool.gif'
            ).initialize(context)
