from zope.interface import implements
from zope.component import getUtility

from Products.CMFCore.interfaces import ISiteRoot

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.redirector.interfaces import IRedirectionStorage

from plone.memoize.instance import memoize


class RedirectsView(BrowserView):
    template = ViewPageTemplateFile('manage-redirects.pt')

    def redirects(self):
        storage = getUtility(IRedirectionStorage)
        portal = getUtility(ISiteRoot)
        context_path = "/".join(self.context.getPhysicalPath())
        portal_path = "/".join(portal.getPhysicalPath())
        redirects = storage.redirects(context_path)
        for redirect in redirects:
            path = "/%s" % redirect.lstrip(portal_path)
            yield {
                'redirect': redirect,
                'path': path,
            }

    def __call__(self):
        return self.template()

    @memoize
    def view_url(self):
        return self.context.absolute_url() + '/@@manage-redirects'
