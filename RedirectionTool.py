# Copyright (C) 2004 
# Plone Solutions AS <info@plonesolutions.com>
#  http://www.plonesolutions.com
#
# Learning Lab Denmark
#  http://www.lld.dk
"""
$Id$
"""

import os
from Globals import InitializeClass, DTMLFile, package_home
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from BTrees.OOBTree import OOBTree, OOSet
from AccessControl import getSecurityManager

from Products.CMFCore.utils import UniqueObject, getToolByName
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.permissions import View, ModifyPortalContent

from Products.CMFCore.ActionInformation import ActionInformation
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore.Expression import Expression

from types import StringType

from interfaces import IRedirectionTool

# List of ids to always ignore when trying to search for moved or missing content
ignoreids = ( 'index_html'
            , 'FrontPage'
            , 'folder_listing'
            , 'folder_contents'
            , 'view'
            )

class RedirectionTool( UniqueObject, ActionProviderBase, SimpleItem ):

    id = 'portal_redirection'
    meta_type = 'Redirection Tool'

    __implements__ = (IRedirectionTool, ActionProviderBase.__implements__)
    _actions = (ActionInformation(id='redirection'
                                , title='Aliases'
                                , action=Expression(
                text='string: ${object_url}/@@manage-aliases')
                                , condition=Expression(
                text='python: object is not None and ' +
                'portal.portal_redirection.isRedirectionAllowedFor(object)')
                                , permissions=(ModifyPortalContent,)
                                , category='object'
                                , visible=1
                                 )
               ,
               )

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
        fromref = redirectfrom
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
        # Make sure the user is allowed to edit the object in question
        redirectto = self._redirectionmap.get(redirectfrom, None)
        if not redirectto or not self.checkPermission(ModifyPortalContent, redirectto):
            return 0
        # The redirectfrom is always a string with the path relative to the portal root
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
    def isRedirectionAllowedFor(self, object):
        """Checks whether the user is allowed to make a redirect for the object"""
        return getSecurityManager().checkPermission(ModifyPortalContent, object) and (not hasattr(self, '_redirectionTypes')  or getattr(object, 'portal_type', '') in self.getRedirectionAllowedForTypes())

    security.declareProtected(View, 'getRedirectionAllowedForTypes')
    def getRedirectionAllowedForTypes(self):
        """ Return the list of portal types that can be redirected to, default is all """
        return getattr(self, '_redirectionTypes', getToolByName(self, 'portal_types').listContentTypes())

    security.declareProtected(ManagePortal, 'setRedirectionAllowedForTypes')
    def setRedirectionAllowedForTypes(self, types=None):
        """ Set the list of portal types that allows redirection, blank if list==[] """
        if types is not None:
            self._redirectionTypes = list(types)
        else:
            if hasattr(self, '_redirectionTypes'):
                del self._redirectionTypes

#    security.declareProtected(View, 'debugVar')
#    def debugVar(self, var=None):
#        import pdb
#        pdb.set_trace()
#        tmpvar = var

    security.declareProtected(View, 'getRedirectObject')
    def getRedirectObject(self, redirectfrom):
        """Return the redirect if it exists"""
        # Redirectfrom is always a string with the path.
        # Check for object existance and return path to redirect to
        if redirectfrom.find('http://') != -1:
            comps = [redirectfrom]
        else:
            comps = redirectfrom.split('/')
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
            portal = getToolByName(self, 'portal_url').getPortalObject()
            obj = portal.restrictedTraverse(redirectto[1:], None)
        else:
            reftool = getToolByName(self, 'reference_catalog', getToolByName(self, 'archetype_tool', None))

            if not reftool:
                return None
            obj = reftool.lookupObject(redirectto)

        # Delete redirect if the object it points to doesn't exist
#        if not obj:
#            self.removeRedirect(redirectfrom)
#            return None
        if obj and remainingcomps:
            return obj.restrictedTraverse('/'.join(remainingcomps), None)

        return obj

    security.declareProtected(View, 'getRedirect')
    def getRedirect(self, redirectfrom):
        """Return the redirect if it exists"""
        redirectobject = self.getRedirectObject(redirectfrom)
        return redirectobject and redirectobject.absolute_url() or redirectobject

    security.declareProtected(View, 'getRedirectFromPathInfo')
    def getRedirectFromPathInfo(self, path_info):
        """Redirect based on path info"""
        siteroot = getToolByName(self, 'portal_url').getPortalObject().getPhysicalPath()
        pathelements = path_info.split('/')
        try:
            pathelements = pathelements[pathelements.index(siteroot[-1])+1:]
            if 'VirtualHostRoot' in pathelements:
                pathelements.remove('VirtualHostRoot')
        except IndexError:
            # Filter some other way
            pass
        key = '/'.join(pathelements)
        if key[0] != '/':
            key = '/' + key
        # Remove trailing slash
        if key.endswith('/') and len(key) > 1:
            key = key[:-1]
        redirect = self.getRedirect(key)

        # As a last resort, let's try a catalogsearch to see if we find the requested object
        # This search will only find items visible for Anonymous
        if not redirect:
            ct = getToolByName(self, 'portal_catalog')
            searchcomp = ''
            for comp in pathelements:
                if comp and comp not in ignoreids:
                    searchcomp = comp
#            res = ct(getId=searchcomp)
            res = ct(id=searchcomp)
            if len(res)==1:
                return res[0].getURL()

        return redirect

    security.declareProtected(View, 'getFirstRealObjectFromPath')
    def getFirstRealObjectFromPath(self, path_info):
        """Redirect based on path info"""
        portal = getToolByName(self, 'portal_url').getPortalObject()
        pathelements = path_info.split('/')
        try:
            if 'VirtualHostRoot' in pathelements:
                pathelements = pathelements[pathelements.index('VirtualHostRoot')+1:]
            else:
                siteroot = portal.getPhysicalPath()
                pathelements = pathelements[pathelements.index(siteroot[-1])+1:]
        except IndexError:
            # Filter some other way
            pass
        pathelements = [x for x in pathelements if x]
        for i in range(len(pathelements)-1,0,-1):
            obj = portal.restrictedTraverse('/'.join(pathelements[:i]), None)
            if obj and obj is not self:
                return obj
        return None


    security.declareProtected(View, 'getAlternativePages')
    def getAlternativePages(self, path_info):
        """Redirect based on path info"""
        ct = getToolByName(self, 'portal_catalog')
        pathelements = path_info.split('/')
        try:
            if 'VirtualHostRoot' in pathelements:
                pathelements = pathelements[pathelements.index('VirtualHostRoot')+1:]
            else:
                siteroot = getToolByName(self, 'portal_url').getPortalObject().getPhysicalPath()
                pathelements = pathelements[pathelements.index(siteroot[-1])+1:]
        except IndexError:
            # Filter some other way
            pass
        pathelements = [x for x in pathelements if x]
        pathelements.reverse()
        for comp in pathelements:
            if comp not in ignoreids:
                res = ct(SearchableText=comp)
                if res:
                    return res[:5]
        return []


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
            if reftool.lookupObject(source):
                return source
            # Not a reference, check path
            sourceobj = 0
            if source.startswith('/'):
                sourceobj = portal.restrictedTraverse(source[1:], None)
            else:
                sourceobj = portal.restrictedTraverse(source,None)
            if sourceobj:
                return self.extractReference(sourceobj)
        # Assume this is an object
        else:
            if reftool and reftool.isReferenceable(source):
                return source.UID()
            else:
                try:
                    urltool = getToolByName(self, 'portal_url')
                    return '/%s' % urltool.getRelativeContentURL(source)
                except AttributeError:
                    pass
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


InitializeClass( RedirectionTool )
