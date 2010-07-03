# Copyright (C) 2004
# Plone Solutions AS <info@plonesolutions.com>
#  http://www.plonesolutions.com
#
# Learning Lab Denmark
#  http://www.lld.dk

from zope.component import getUtility
from zope.interface import implements
from zope.deprecation import deprecate

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from AccessControl import getSecurityManager

from Products.CMFCore.utils import UniqueObject, getToolByName
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.permissions import View

from Products.RedirectionTool.permissions import ModifyAliases

from Products.CMFPlone.utils import base_hasattr

from types import StringType

from interfaces import IRedirectionTool
from plone.app.redirector.interfaces import IRedirectionStorage


class RedirectionTool(UniqueObject, SimpleItem):

    implements(IRedirectionTool)

    id = 'portal_redirection'
    meta_type = 'Redirection Tool'

    security = ClassSecurityInfo()

    # ZMI methods

    # 'portal_redirection' interface methods
    security.declareProtected(View, 'addRedirect')
    @deprecate("The addRedirect method of the RedirectionTool has been "
               "deprecated. Use the IRedirectionStorage utility from "
               "plone.app.redirector instead.")
    def addRedirect(self, redirectfrom, redirectto):
        """Create a redirect"""
        # Make sure the user is allowed to edit the object in question
        if not self.checkPermission(ModifyAliases, redirectto):
            return False
        # The redirectfrom is always a string with the path relative to the portal root
        portal = getToolByName(self, 'portal_url').getPortalObject()
        portal_path = "/".join(portal.getPhysicalPath())
        fromref = "%s%s" % (portal_path, redirectfrom)
        source = fromref.split('/')
        while len(source):
            obj = portal.unrestrictedTraverse(source, None)
            if obj is None:
                source = source[:-1]
            else:
                if not getSecurityManager().checkPermission(ModifyAliases, obj):
                    return False
                else:
                    break
        toref = self.extractReference(redirectto)
        storage = getUtility(IRedirectionStorage)
        storage.add(fromref, toref)
        return True

    security.declareProtected(View, 'removeRedirect')
    @deprecate("The removeRedirect method of the RedirectionTool has been "
               "deprecated. Use the IRedirectionStorage utility from "
               "plone.app.redirector instead.")
    def removeRedirect(self, redirectfrom):
        """Remove existing redirect"""
        # The redirectfrom is always a string with the path relative to the portal root
        portal = getToolByName(self, 'portal_url').getPortalObject()
        portal_path = "/".join(portal.getPhysicalPath())
        redirectfrom = "%s%s" % (portal_path, redirectfrom)
        # Make sure the user is allowed to edit the object in question
        storage = getUtility(IRedirectionStorage)
        redirectto = storage.get(redirectfrom)
        if redirectto is None or not self.checkPermission(ModifyAliases, redirectto):
            return False
        storage.remove(redirectfrom)
        return True

    security.declareProtected(View, 'isRedirectionAllowedFor')
    def isRedirectionAllowedFor(self, obj):
        """Checks whether the user is allowed to make a redirect for the object"""
        if obj is None:
            return False
        if not getSecurityManager().checkPermission(ModifyAliases, obj):
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
    @deprecate("The getRedirectObject method of the RedirectionTool has been "
               "deprecated. There is no replacement, since it was never "
               "public.")
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
        storage = getUtility(IRedirectionStorage)
        # Take the chunks of the url and see if folders higher up the tree have redirects as well
        # So if portal/folder has a redirect to portal/newfolder accessing
        # portal/folder/someobject will redirect to portal/newfolder/someobject
        while not redirectto and i > 0:
            redirectto = storage.get('/'.join(comps[:i]), None)
            remainingcomps = comps[i:]
            i-=1
        if not redirectto:
            return None
        obj = None
        # Check if the path is valid, otherwise return None
        obj = self.restrictedTraverse(redirectto, None)

        if obj and remainingcomps:
            return obj.restrictedTraverse('/'.join(remainingcomps), None)

        return obj

    security.declareProtected(View, 'getRedirect')
    @deprecate("The getRedirect method of the RedirectionTool has been "
               "deprecated. Use the IRedirectionStorage utility from "
               "plone.app.redirector instead.")
    def getRedirect(self, redirectfrom):
        """Return the redirect if it exists"""
        # The redirectfrom is always a string with the path relative to the portal root
        redirectobject = self.getRedirectObject(redirectfrom)
        return redirectobject and redirectobject.absolute_url() or redirectobject

    security.declareProtected(View, 'getRedirectsTo')
    @deprecate("The getRedirectsTo method of the RedirectionTool has been "
               "deprecated. Use the IRedirectionStorage utility from "
               "plone.app.redirector instead.")
    def getRedirectsTo(self, redirectto):
        """Return the list of redirects"""
        if not self.checkPermission(View, redirectto):
            return []
        toref = self.extractReference(redirectto)
        storage = getUtility(IRedirectionStorage)
        return storage.redirects(toref)

    security.declarePrivate('extractReference')
    @deprecate("The extractReference method of the RedirectionTool has been "
               "deprecated. There is no replacement, since it was never "
               "public.")
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
    @deprecate("The checkPermission method of the RedirectionTool has been "
               "deprecated. There is no replacement, since it was never "
               "public.")
    def checkPermission(self, permission, source):
        """Extract the object from the source and check the permission"""
        # Check for referencable, otherwise get path for instances
        # Check path or reference if string
        obj = None
        if isinstance(source, StringType):
            portal = getToolByName(self, 'portal_url').getPortalObject()
            obj = portal.unrestrictedTraverse(source, None)
            if obj is None:
                # Wasn't a path, check for reference
                reftool = getToolByName(self, 'reference_catalog', getToolByName(self, 'archetype_tool', None))

                obj = reftool.lookupObject(source)
        else:
            # Assume this is an object
            obj = source
        if obj is None:
            raise NameError('No such object %s' % source)
        return getSecurityManager().checkPermission(permission, obj)

    security.declarePrivate('migrateStorage')
    def migrateStorage(self, logger):
        if base_hasattr(self, '_reverse_redirectionmap'):
            del self._reverse_redirectionmap
        if base_hasattr(self, '_redirectionmap'):
            portal = getToolByName(self, 'portal_url').getPortalObject()
            portal_path = "/".join(portal.getPhysicalPath())
            storage = getUtility(IRedirectionStorage)
            redirmap = self._redirectionmap
            for key in redirmap:
                try:
                    dst = self.extractReference(redirmap[key])
                except NameError:
                    logger.warning("The destination '%s' for '%s' could not be "
                                   "found, the redirection was not migrated."
                                   % (redirmap[key], key))
                    continue
                src = "%s%s" % (portal_path, key)
                storage.add(src, dst)
            del self._redirectionmap

InitializeClass(RedirectionTool)
