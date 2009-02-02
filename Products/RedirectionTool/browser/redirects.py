from zope.interface import implements, Interface
from zope.component import adapts, getUtility
from zope.schema import Choice, Tuple

from AccessControl import getSecurityManager
from Products.RedirectionTool.permissions import ModifyAliases

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.redirector.interfaces import IRedirectionStorage
from plone.app.controlpanel.widgets import MultiCheckBoxThreeColumnWidget
from zope.formlib.form import setUpWidgets, FormFields

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
            path = redirect[len(portal_path):]
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
                msg = _(u"You have to enter an alias.")
                errors['redirection'] = msg
                status.addStatusMessage(msg, type='error')
            elif '://' in redirection:
                msg = _(u"An alias is a path from the portal root and doesn't include http:// or alike.")
                errors['redirection'] = msg
                status.addStatusMessage(msg, type='error')
            else:
                if redirection[0] != '/':
                    path = "/".join(self.context.getPhysicalPath()[:-1])
                    redirection = "%s/%s" % (path, redirection)
                else:
                    path = "/".join(portal.getPhysicalPath())
                    redirection = "%s%s" % (path, redirection)
                source = redirection.split('/')
                while len(source):
                    obj = portal.unrestrictedTraverse(source, None)
                    if obj is None:
                        source = source[:-1]
                    else:
                        if not getSecurityManager().checkPermission(ModifyAliases, obj):
                            obj = None
                        break
                if obj is None:
                    msg = _(u"You don't have the permission to set an alias from the location you provided.")
                    errors['redirection'] = msg
                    status.addStatusMessage(msg, type='error')
                else:
                    # XXX check if there is an existing alias
                    # XXX check whether there is an object
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
        return self.context.absolute_url() + '/@@manage-aliases'


class IAliasesSchema(Interface):

    managed_types = Tuple(title=_(u"Managed types"),
                          description=_(u"Select the types for which the "
                                         "aliases can be managed"),
                          required=True,
                          missing_value=tuple(),
                          value_type=Choice(
                              vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes"))


class RedirectsControlPanelAdapter(object):

    adapts(IPloneSiteRoot)
    implements(IAliasesSchema)

    def __init__(self, context):
        self.context = context
        self.rt = getToolByName(context, 'portal_redirection')

    def get_managed_types(self):
        return self.rt.getRedirectionAllowedForTypes()

    def set_managed_types(self, value):
        self.rt.setRedirectionAllowedForTypes(value)

    managed_types = property(get_managed_types, set_managed_types)


class RedirectsControlPanel(BrowserView):
    template = ViewPageTemplateFile('redirects-controlpanel.pt')

    form_fields = FormFields(IAliasesSchema, render_context=True)
    form_fields['managed_types'].custom_widget = MultiCheckBoxThreeColumnWidget
    form_fields['managed_types'].custom_widget.cssClass='label'

    def redirects(self):
        storage = getUtility(IRedirectionStorage)
        portal = getUtility(ISiteRoot)
        context_path = "/".join(self.context.getPhysicalPath())
        portal_path = "/".join(portal.getPhysicalPath())
        portal_path_len = len(portal_path)
        for redirect in storage:
            if redirect.startswith(portal_path):
                path = redirect[portal_path_len:]
            else:
                path = redirect
            redirectto = storage.get(redirect)
            if redirectto.startswith(portal_path):
                redirectto = redirectto[portal_path_len:]
            yield {
                'redirect': redirect,
                'path': path,
                'redirect-to': redirectto,
            }

    def __call__(self):
        storage = getUtility(IRedirectionStorage)
        portal = getUtility(ISiteRoot)
        request = self.request
        form = request.form
        status = IStatusMessage(self.request)
        errors = {}

        if 'form.button.Remove' in form:
            redirects = form.get('redirects', ())
            for redirect in redirects:
                storage.remove(redirect)
            if len(redirects) == 0:
                status.addStatusMessage(_(u"No aliases selected for removal."), type='info')
            elif len(redirects) > 1:
                status.addStatusMessage(_(u"Aliases removed."), type='info')
            else:
                status.addStatusMessage(_(u"Alias removed."), type='info')
        elif 'form.button.Save' in form:
            dst = IAliasesSchema(self.context)
            dst.managed_types = self.request.form['form.managed_types']

        self.widgets = setUpWidgets(
            self.form_fields, 'form', self.context, self.request,
            form=self, ignore_request=True)

        return self.template(errors=errors)

    @memoize
    def view_url(self):
        return self.context.absolute_url() + '/@@aliases-controlpanel'
