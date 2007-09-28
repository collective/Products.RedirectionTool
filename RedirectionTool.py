# Copyright (C) 2004 
# Plone Solutions AS <info@plonesolutions.com>
#  http://www.plonesolutions.com
#
# Learning Lab Denmark
#  http://www.lld.dk
"""
$Id$
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from BTrees.OOBTree import OOBTree, OOSet
from AccessControl import getSecurityManager

from Products.CMFCore.utils import UniqueObject, getToolByName
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.permissions import View, ModifyPortalContent

from types import StringType

from interfaces import IRedirectionTool


class RedirectionTool(UniqueObject, SimpleItem):

    id = 'portal_redirection'
    meta_type = 'Redirection Tool'

    __implements__ = (IRedirectionTool,)

    security = ClassSecurityInfo()

    def __init__(self):
        self._redirectionmap = OOBTree()         # path or referenceid -> path or referenceid
        self._reverse_redirectionmap = OOBTree() # path or referenceid -> Set of paths or referenceids

    # ZMI methods

    # 'portal_redirection' interface methods
    security.declareProtected(View, 'addRedirect')
    def addRedirect(self, redirectfrom, redirectto):
        """Create a redirect"""
        # Make sure the user is allowed to edit the object in question
        if not self.checkPermission(ModifyPortalContent, redirectto):
            return 0
        # Remove trailing slash except where length is 1 (we dont want null strings instead of /)
        if redirectfrom.endswith('/') and len(redirectfrom) > 1:
            redirectfrom = redirectfrom[:-1]
        # Add the reference to the redirectionmap and the reversemap.
        # The redirectfrom is always a string with the path relative to the portal root
        portal = getToolByName(self, 'portal_url').getPortalObject()
        portal_path = "/".join(portal.getPhysicalPath())
        fromref = "%s%s" % (portal_path, redirectfrom)
        toref = self.extractReference(redirectto)
        redirmap = self._redirectionmap
        reversemap = self._reverse_redirectionmap

        # If the redirect already exists, remove so it can be be added again (basically overwritten).
        if redirmap.has_key(fromref):
            # Get the old redirect
            oldtoref = redirmap[fromref]
            # Remove it from the reverse map
            reversemap[oldtoref].remove(fromref)
            if len(reversemap[oldtoref]) == 0:
                del reversemap[oldtoref]

        redirmap[fromref] = toref
        torefset = reversemap.get(toref, None)
        # Create a new Set if no set exists
        if not torefset:
            torefset = OOSet()
            reversemap[toref] = torefset
        torefset.insert(fromref)
        return 1

    security.declareProtected(View, 'removeRedirect')
    def removeRedirect(self, redirectfrom):
        """Remove existing redirect"""
        # The redirectfrom is always a string with the path relative to the portal root
        portal = getToolByName(self, 'portal_url').getPortalObject()
        portal_path = "/".join(portal.getPhysicalPath())
        redirectfrom = "%s%s" % (portal_path, redirectfrom)
        # Make sure the user is allowed to edit the object in question
        redirectto = self._redirectionmap.get(redirectfrom, None)
        if not redirectto or not self.checkPermission(ModifyPortalContent, redirectto):
            return 0
        redirmap = self._redirectionmap
        reversemap = self._reverse_redirectionmap
        fromref = redirectfrom
        toref = redirmap[fromref]

        # Delete from redirection map
        del redirmap[fromref]

        # Delete from reversemap, and delete entire entry in reversemap if
        # it was the only entry in the set.
        toset = reversemap.get(toref)
        toset.remove(fromref)
        if len(toset) == 0:
            del reversemap[toref]
        return 1

    security.declareProtected(View, 'isRedirectionAllowedFor')
    def isRedirectionAllowedFor(self, obj):
        """Checks whether the user is allowed to make a redirect for the object"""
        if obj is None:
            return False
        if not getSecurityManager().checkPermission(ModifyPortalContent, obj):
            return False
        types = getattr(self, '_redirectionTypes', None)
        if types is None:
            return True
        return getattr(obj, 'portal_type', '') in self.getRedirectionAllowedForTypes()

    security.declareProtected(View, 'getRedirectionAllowedForTypes')
    def getRedirectionAllowedForTypes(self):
        """ Return the list of portal types that can be redirected to, default is all """
        types = getattr(self, '_redirectionTypes', None)
        if types is None:
            types = getToolByName(self, 'portal_types').listContentTypes()
        return types

    security.declareProtected(ManagePortal, 'setRedirectionAllowedForTypes')
    def setRedirectionAllowedForTypes(self, types=None):
        """ Set the list of portal types that allows redirection, blank if list==[] """
        if types is not None:
            self._redirectionTypes = list(types)
        else:
            if getattr(self, '_redirectionTypes', None) is not None:
                del self._redirectionTypes

    security.declareProtected(View, 'getRedirectObject')
    def getRedirectObject(self, redirectfrom):
        """Return the redirect if it exists"""
        # Redirectfrom is always a string with the path.
        # Check for object existance and return path to redirect to
        if redirectfrom.find('http://') != -1:
            comps = [redirectfrom]
        else:
            portal = getToolByName(self, 'portal_url').getPortalObject()
            portal_path = "/".join(portal.getPhysicalPath())
            fromref = "%s%s" % (portal_path, redirectfrom)
            comps = fromref.split('/')
            comps = ['']+[x for x in comps if x]
        redirectto = None
        remainingcomps = []
        i = len(comps)
        #Take the chunks of the url and see if folders higher up the tree have redirects as well
        #So if portal/folder has a redirect to portal/newfolder accessing portal/folder/someobject will redirect to portal/newfolder/someobject
        while not redirectto and i > 0:
            redirectto = self._redirectionmap.get('/'.join(comps[:i]), None)
            remainingcomps = comps[i:]
            i-=1
        if not redirectto:
            return None
        obj = None
        # Find out if it's a path or a referenceid
        if redirectto.startswith('/'):
            # Check if the path is valid, otherwise return None
            obj = self.restrictedTraverse(redirectto, None)
        else:
            reftool = getToolByName(self, 'reference_catalog', getToolByName(self, 'archetype_tool', None))

            if not reftool:
                return None
            obj = reftool.lookupObject(redirectto)

        if obj and remainingcomps:
            return obj.restrictedTraverse('/'.join(remainingcomps), None)

        return obj

    security.declareProtected(View, 'getRedirect')
    def getRedirect(self, redirectfrom):
        """Return the redirect if it exists"""
        # The redirectfrom is always a string with the path relative to the portal root
        redirectobject = self.getRedirectObject(redirectfrom)
        return redirectobject and redirectobject.absolute_url() or redirectobject

    security.declareProtected(View, 'getRedirectsTo')
    def getRedirectsTo(self, redirectto):
        """Return the list of redirects"""
        if not self.checkPermission(View, redirectto):
            return []
        toref = self.extractReference(redirectto)
        return list(self._reverse_redirectionmap.get(toref, []))

    security.declarePrivate('extractReference')
    def extractReference(self, source):
        """Extract the reference from the source"""
        # Prefer the UID, otherwise use path.
        # Check path or reference if string
        reftool = getToolByName(self, 'reference_catalog', getToolByName(self, 'archetype_tool', None))
        if type(source) is StringType:
            portal = getToolByName(self, 'portal_url').getPortalObject()
            # Check for reference
            sourceobj = reftool.lookupObject(source)
            if sourceobj is not None:
                return "/".join(sourceobj.getPhysicalPath())
            # Not a reference, check path
            if source.startswith('/'):
                sourceobj = portal.restrictedTraverse(source[1:], None)
            else:
                sourceobj = portal.restrictedTraverse(source, None)
            if sourceobj is not None:
                return "/".join(sourceobj.getPhysicalPath())
        # Assume this is an object
        else:
            return "/".join(source.getPhysicalPath())
        raise NameError('Could not find source')

    security.declarePublic('checkPermission')
    def checkPermission(self, permission, source):
        """Extract the object from the source and check the permission"""
        # Check for referencable, otherwise get path for instances
        # Check path or reference if string
        obj = None
        if isinstance(source, StringType):
            portal = getToolByName(self, 'portal_url').getPortalObject()
            obj = portal.unrestrictedTraverse(source[1:], portal.unrestrictedTraverse(source,None))
            if not obj:
                # Wasn't a path, check for reference
                reftool = getToolByName(self, 'reference_catalog', getToolByName(self, 'archetype_tool', None))

                obj = reftool.lookupObject(source)
        else:
            # Assume this is an object
            obj = source
        if obj is None:
            raise NameError('No such object %s' % source)
        return getSecurityManager().checkPermission( permission, obj )


InitializeClass(RedirectionTool)
