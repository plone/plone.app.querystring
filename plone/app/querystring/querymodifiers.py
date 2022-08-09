# -*- coding: utf-8 -*-
from plone.app.querystring.interfaces import IQueryModifier
from zope.interface import provider
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from zope.schema.interfaces import IVocabularyFactory


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

@provider(IQueryModifier)
def vocabulary_value_look_up(query):
    registry = getUtility(IRegistry)

    for query_param in query:
        query_field_name = query_param.get('i')
        query_vocabulary_name = registry.get(f"plone.app.querystring.field.{query_field_name}.vocabulary")

        if query_vocabulary_name:

            query_terms = query_param.get('v')
            factory = getUtility(IVocabularyFactory, query_vocabulary_name)
            vocabulary = factory(None)
            if type(query_terms) is list:
                new_terms = []
                for query_term in query_terms:
                    try:
                        vocabulary_term = vocabulary.getTerm(query_term)
                        new_terms.append(query_term)

                    except:
                        for term in vocabulary:
                            if term.token == query_term:
                                new_terms.append(term.value)
                                break
                query_param['v']= new_terms
            elif type(query_terms) is str:
                try:
                    vocabulary_term = vocabulary.getTerm(query_terms)
                except:
                    for term in vocabulary:
                        if term.token == query_terms:
                            query_terms=term.value
                            break
            query_param['v']= query_terms

        query_vocabulary_name = None

    return query




