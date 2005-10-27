## Controller Python Script 'removeRedirection'
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##bind state=state
##parameters=redirects
##title=Validate integer
##

# if relative url, add path to container.
redirectiontool = context.portal_redirection

for redirection in redirects:
    redirectiontool.removeRedirect(redirection)

if state.getStatus() != 'success':
    state.set(portal_status_message='Please fix your errors')

return state