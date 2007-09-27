from zope.interface import implements
from zope.component import getUtility

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.interfaces import ISiteRoot
from plone.app.redirector.interfaces import IRedirectionStorage

from plone.memoize.instance import memoize

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('RedirectionTool')


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
        storage = getUtility(IRedirectionStorage)
        portal = getUtility(ISiteRoot)
        request = self.request
        form = request.form
        status = IStatusMessage(self.request)
        errors = {}

        if 'form.button.Add' in form:
            redirection = form.get('redirection')
            if redirection is None or redirection == '':
                errors['redirection'] = _(u"You have to enter an alias.")
                status.addStatusMessage(_(u"You have to enter an alias."), type='error')
            else:
                if redirection[0] != '/':
                    path = "/".join(self.context.getPhysicalPath()[:-1])
                    redirection = "%s/%s" % (path, redirection)
                else:
                    path = "/".join(portal.getPhysicalPath())
                    redirection = "%s%s" % (path, redirection)
                del form['redirection']
                storage.add(redirection, "/".join(self.context.getPhysicalPath()))
                status.addStatusMessage(_(u"Alias added."), type='info')
        elif 'form.button.Remove' in form:
            redirects = form.get('redirects', ())
            for redirect in redirects:
                storage.remove(redirect)
            if len(redirects) > 1:
                status.addStatusMessage(_(u"Aliases removed."), type='info')
            else:
                status.addStatusMessage(_(u"Alias removed."), type='info')

        return self.template(errors=errors)

    @memoize
    def view_url(self):
        return self.context.absolute_url() + '/@@manage-redirects'
