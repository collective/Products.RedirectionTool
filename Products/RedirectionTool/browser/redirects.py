import csv
from cStringIO import StringIO

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


def absolutize_path(path, context=None, is_alias=True):
    """Check whether `path` is a well-formed path from the portal root, and
       make it Zope-root-relative. If `is_alias` (as opposed to "is_target"),
       also make sure the user has the requisite ModifyAliases permissions to
       make an alias from that path. Return a 2-tuple: (absolute redirection path,
       an error message iff something goes wrong and otherwise '').

    Assume relative paths are relative to `context`; reject relative paths if
    `context` is None.

    """
    portal = getUtility(ISiteRoot)
    err = None
    if path is None or path == '':
        err = is_alias and _(u"You have to enter an alias.") \
                        or _(u"You have to enter a target.")
    elif '://' in path:
        err = is_alias and _(u"An alias is a path from the portal root and doesn't include http:// or alike.") \
                        or _(u"Target path must be relative to the portal root and not include http:// or the like.")
    else:
        if path.startswith('/'):
            context_path = "/".join(portal.getPhysicalPath())
            path = "%s%s" % (context_path, path)
        else:
            if context is None:
                err = is_alias and _(u"Alias path must start with a slash.") \
                                or _(u"Target path must start with a slash.")
            else:
                context_path = "/".join(context.getPhysicalPath()[:-1])
                path = "%s/%s" % (context_path, path)
        if not err and is_alias:  # XXX should we require Modify Alias permission on the target as well?
            source = path.split('/')
            while len(source):
                obj = portal.unrestrictedTraverse(source, None)
                if obj is None:
                    source = source[:-1]
                else:
                    if not getSecurityManager().checkPermission(ModifyAliases, obj):
                        obj = None
                    break
            if obj is None:
                err = _(u"You don't have the permission to set an alias from the location you provided.")
            else:
                pass
                # XXX check if there is an existing alias
                # XXX check whether there is an object
    return path, err


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
        request = self.request
        form = request.form
        status = IStatusMessage(self.request)
        errors = {}

        if 'form.button.Add' in form:
            redirection, err = absolutize_path(form.get('redirection'), is_alias=True)
            if err:
                errors['redirection'] = err
                status.addStatusMessage(err, type='error')
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

    def __init__(self, context, request):
        super(RedirectsControlPanel, self).__init__(context, request)
        self.errors = []  # list of tuples: (line_number, absolute_redirection_path, err_msg, target)

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
        elif 'form.button.Upload' in form:
            self.upload(form['file'], portal, storage, status)

        self.widgets = setUpWidgets(
            self.form_fields, 'form', self.context, self.request,
            form=self, ignore_request=True)

        return self.template()

    def upload(self, file, portal, storage, status):
        """Add the redirections from the CSV file `file`. If anything goes wrong, do nothing."""
        # Turn all kinds of newlines into LF ones. The csv module doesn't do
        # its own newline sniffing and requires either \n or \r.
        file = StringIO('\n'.join(file.read().splitlines()))

        # Use first two lines as a representative sample for guessing format,
        # in case one is a bunch of headers.
        dialect = csv.Sniffer().sniff(file.readline() + file.readline())
        file.seek(0)

        portal_path = "/".join(portal.getPhysicalPath())
        successes = []  # list of tuples: (abs_redirection, target)
        had_errors = False
        for i, fields in enumerate(csv.reader(file, dialect)):
            if len(fields) == 2:
                redirection, target = fields
                abs_redirection, err = absolutize_path(redirection, is_alias=True)
                abs_target, target_err = absolutize_path(target, is_alias=False)
                if err and target_err:
                    err = "%s %s" % (err, target_err)  # sloppy w.r.t. i18n
                elif target_err:
                    err = target_err
                else:
                    if abs_redirection == abs_target:
                        err = _(u"Aliases that point to themselves will cause \
                            an endless cycle of redirects.") # TODO: detect indirect recursion
            else:
                err = _(u"Each line must have 2 columns.")

            if not err:
                if not had_errors:  # else don't bother
                    successes.append((abs_redirection, abs_target))
            else:
                had_errors = True
                self.errors.append(dict(line_number=i+1, line=dialect.delimiter.join(fields), message=err))

        if not had_errors:
            for abs_redirection, abs_target in successes:
                storage.add(abs_redirection, abs_target)
            status.addStatusMessage(_(u"%i aliases added.") % len(successes), type='info')

    @memoize
    def view_url(self):
        return self.context.absolute_url() + '/@@aliases-controlpanel'
