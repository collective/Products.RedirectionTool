from zope.interface import Interface

class IRedirectionTool(Interface):
    """
    Redirection tool stores redirects and enables you to redirect the user if she
    tries to get a moved page, or you can use it to enable multiple addresses for
    the same object.
    """
    
    def addRedirect(redirectfrom, redirectto):
        """
        The method addRedirect takes the path to redirect from, and the object, 
        referenceid or path to create a redirect to, and stores the redirect 
        internally. UID has presedence over path when choosing a reference.
        Return 1 if success, 0 otherwise.
        """

    def removeRedirect(redirectfrom):
        """
        The method addRedirect takes path to remove redirect from, and deletes 
        the redirect from the internal table. Return 1 if a redirect is removed,
        0 otherwise.
        """

    def isRedirectionAllowedFor(object):
        """
        Checks whether the user is allowed to make a redirect for the object.
        It is used for displaying the redirection tab.
        """

    def getRedirect(redirectfrom):
        """
        Gets a path and checks whether there exists a redirect. If it exists, 
        the URL to redirect to is returned, otherwise None is returned.
        """

    def getRedirectsTo(redirectto):
        """
        Returns a list of the redirects to this object, path or reference
        """