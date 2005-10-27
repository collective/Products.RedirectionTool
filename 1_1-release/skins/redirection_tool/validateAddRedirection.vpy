## Controller Python Script 'validateAddRedirection'
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##bind state=state
##parameters=redirection
##title=Validate integer
##

# Make sure there are no object where the redirect points to
# Make sure the redirect doesn't already exist
if not state.getError('redirection'):
    # Make sure we're allowed to edit the current object
    rt = context.portal_url.getPortalObject().portal_redirection
    if not rt.checkPermission('Modify portal content', context):
        state.setError('redirection', 'You are not allowed to edit and add aliases to this content.', new_status='failure')
    # Massage the redirection, rip code from the addRedirection script
    if redirection[0] != '/':
        relativeurl = context.portal_url.getRelativeContentURL(context.aq_inner.aq_parent)
        if relativeurl:
            redirection = '/%s/%s' % (relativeurl, redirection)
        else:
            redirection = '/' + redirection

    ob = context.portal_url.getPortalObject().restrictedTraverse(redirection[1:], None)
    if ob:
        state.setError('redirection', 'An object exists at the indicated URL.', new_status='failure')

    if rt.getRedirect(redirection):
        state.setError('redirection', 'A redirection already exists from the indicated URL.', new_status='failure')

    if redirection.find('http://') != -1:
        state.setError('redirection', 'Redirects are relative to the portal root and does not include http://servername', new_status='failure')

if state.getStatus() != 'success':
    state.set(portal_status_message='Please fix your errors')

return state