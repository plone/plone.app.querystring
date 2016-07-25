# -*- coding: utf-8 -*-
from plone.app.querystring.interfaces import IQueryModifier
from zope.interface import provider


@provider(IQueryModifier)
def modify_query_to_enforce_navigation_root(query):
    """enforce a search in the current navigation root

    if not already a path was given we search only for contents in the current
    IVavigationRoot.
    """
    if not query:
        return query

    has_path_criteria = any(
        (criteria['i'] == 'path')
        for criteria in query
    )
    if not has_path_criteria:
        query = list(query)
        query.append({
            'i': 'path',
            'o': 'plone.app.querystring.operation.string.path',
            'v': '/',
        })
    return query
