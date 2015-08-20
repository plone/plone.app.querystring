# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getUtility
from plone.registry.interfaces import IRegistry


def upgrade_1_to_2_typo_in_registry(context):
    registry = getUtility(IRegistry)
    name = 'plone.app.querystring.field.getObjPositionInParent.operations'
    wrong_value = 'plone.app.querystring.operation.int.greaterThan'
    right_value = 'plone.app.querystring.operation.int.largerThan'
    values = registry.get(name)
    if not values:
        return
    if wrong_value in values:
        del values[values.index(wrong_value)]
    if right_value not in values:
        values.append(right_value)
    registry[name] = values


def fix_select_all_existing_collections(context):

    ops_to_fix = [
        u'portal_type',
        u'review_state'
    ]
    old_val = u"plone.app.querystring.operation.selection.is"
    new_val = u"plone.app.querystring.operation.selection.any"

    catalog = context.portal_catalog
    results = catalog.unrestrictedSearchResults(
        portal_type="Collection"
    )

    for elem in results:
        changed = False
        obj = elem.getObject()
        aux = list()
        for op in obj.query:
            if op['i'] in ops_to_fix and op['o'] == old_val:
                op['o'] = new_val
                changed = True
            aux.append(op)

        if changed:
            obj.query = aux
            obj.reindexObject()
