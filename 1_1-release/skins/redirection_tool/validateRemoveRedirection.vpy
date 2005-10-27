## Controller Python Script 'validateRemoveRedirection'
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##bind state=state
##parameters=redirects
##title=Validate integer
##

# Make sure the redirect doesn't already exist
if not state.getError('redirection'):
    rt = context.portal_url.getPortalObject().portal_redirection
    # Make sure the user is allowed to modify the object that the redirects point to
    # They are all supposed to be the same object, but loop over just in case
    objects = {}
    for r in redirects:
        obj = rt.getRedirectObject(r)
        objects[obj.absolute_url()] = obj

    # Make sure we're allowed to edit the current object
    for r in objects.values():
        if not rt.checkPermission('Modify portal content', r):
            state.setError('redirection', 'You are not allowed to remove aliases from this content.', new_status='failure')

if state.getStatus() != 'success':
    state.set(portal_status_message='Please fix your errors')

return state