"""
$Id$
"""

from Products.CMFCore.utils import ToolInit, ContentInit

import RedirectionTool

redirection_tool_globals=globals()


def initialize( context ):
    
    ToolInit('Redirection Tool', 
            tools=(RedirectionTool.RedirectionTool, ), 
            icon='action_icon.gif'
            ).initialize(context)
