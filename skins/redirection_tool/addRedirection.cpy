## Controller Python Script 'addRedirection'
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##bind state=state
##parameters=redirection
##title=Validate integer
##

redirectiontool = context.portal_redirection

# if relative url, add path to container.
if redirection[0] != '/':
    relativeurl = context.portal_url.getRelativeContentURL(context.aq_inner.aq_parent)
    if relativeurl:
        redirection = '/%s/%s' % (relativeurl, redirection)
    else:
        redirection = '/' + redirection

redirectiontool.addRedirect(redirection, context)

if state.getStatus() != 'success':
    state.set(portal_status_message='Please fix your errors')

return state