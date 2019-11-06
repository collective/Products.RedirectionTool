# -*- coding: utf-8 -*-


def makeContent(site, portal_type, id="document", **kw):
    site.invokeFactory(type_name=portal_type, id=id)
    content = getattr(site, id)

    return content
