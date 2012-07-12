from collections import namedtuple
import logging

from Acquisition import aq_parent
from DateTime import DateTime
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import getNavigationRoot
from Products.CMFPlone.utils import base_hasattr
from zope.component import getUtility
from zope.dottedname.resolve import resolve

logger = logging.getLogger('plone.app.querystring')

Row = namedtuple('Row', ['index', 'operator', 'values'])


def parseFormquery(context, formquery, sort_on=None, sort_order=None):
    if not formquery:
        return {}
    reg = getUtility(IRegistry)

    # Make sure the things in formquery are dictionaries
    formquery = map(dict, formquery)

    query = {}
    for row in formquery:
        operator = row.get('o', None)
        function_path = reg["%s.operation" % operator]

        # The functions expect this pattern of object, so lets give it to
        # them in a named tuple instead of jamming things onto the request
        row = Row(index=row.get('i', None),
                  operator=function_path,
                  values=row.get('v', None))

        kwargs = {}
        parser = resolve(row.operator)
        kwargs = parser(context, row)
        query.update(kwargs)

    if not query:
        # If the query is empty fall back onto the equality query
        query = _equal(context, row)

    # Check for valid indexes
    catalog = getToolByName(context, 'portal_catalog')
    valid_indexes = [index for index in query if index in catalog.indexes()]

    # We'll ignore any invalid index, but will return an empty set if none of
    # the indexes are valid.
    if not valid_indexes:
        logger.warning(
            "Using empty query because there are no valid indexes used.")
        return {}

    # Add sorting (sort_on and sort_order) to the query
    if sort_on:
        query['sort_on'] = sort_on
    if sort_order:
        query['sort_order'] = sort_order
    return query


# Query operators

def _contains(context, row):
    return _equal(context, row)


def _equal(context, row):
    return {row.index: {'query': row.values, }}


def _isTrue(context, row):
    return {row.index: {'query': True, }}


def _isFalse(context, row):
    return {row.index: {'query': False, }}


def _between(context, row):
    tmp = {row.index: {
              'query': sorted(row.values),
              'range': 'minmax',
              },
          }
    return tmp


def _largerThan(context, row):
    tmp = {row.index: {
              'query': row.values,
              'range': 'min',
              },
          }
    return tmp


def _lessThan(context, row):
    tmp = {row.index: {
              'query': row.values,
              'range': 'max',
              },
          }
    return tmp


def _currentUser(context, row):
    """Current user lookup"""
    mt = getToolByName(context, 'portal_membership')
    user = mt.getAuthenticatedMember()
    return {row.index: {
              'query': user.getUserName(),
              },
          }


def _lessThanRelativeDate(context, row):
    """ "Between now and N days from now." """
    # INFO: Values is the number of days
    try:
        values = int(row.values)
    except ValueError:
        values = 0
    now = DateTime()
    start_date = now.earliestTime()
    end_date = now + values
    end_date = end_date.latestTime()
    row = Row(index=row.index,
              operator=row.operator,
              values=(start_date, end_date))
    return _between(context, row)


def _moreThanRelativeDate(context, row):
    """ "Between now and N days ago." """
    # INFO: Values is the number of days
    try:
        values = int(row.values)
    except ValueError:
        values = 0
    now = DateTime()
    start_date = now - values
    start_date = start_date.earliestTime()
    end_date = now.latestTime()
    row = Row(index=row.index,
              operator=row.operator,
              values=(start_date, end_date))
    return _between(context, row)


def _betweenDates(context, row):
    try:
        start_date = DateTime(row.values[0])
    except DateTime.DateTimeError:
        start_date = DateTime(0)
    try:
        end_date = DateTime(row.values[1])
    except DateTime.DateTimeError:
        row = Row(index=row.index,
                  operator=row.operator,
                  values=start_date)
        return _largerThan(context, row)
    else:
        row = Row(index=row.index,
                  operator=row.operator,
                  values=(start_date, end_date))

        return _between(context, row)


def _today(context, row):
    now = DateTime()
    start_date = now.earliestTime()
    end_date = now.latestTime()
    row = Row(index=row.index,
              operator=row.operator,
              values=(start_date, end_date))
    return _between(context, row)


def _afterToday(context, row):
    row = Row(index=row.index,
              operator=row.operator,
              values=DateTime())
    return _largerThan(context, row)


def _beforeToday(context, row):
    row = Row(index=row.index,
              operator=row.operator,
              values=DateTime())
    return _lessThan(context, row)


def _path(context, row):
    values = row.values
    if not '/' in values:
        # It must be a UID
        values = '/'.join(getPathByUID(context, values))
    # take care of absolute paths without nav_root
    nav_root = getNavigationRoot(context)
    if not values.startswith(nav_root):
        values = nav_root + values
    tmp = {row.index: {'query': values, }}
    return tmp


def _relativePath(context, row):
    # Walk through the tree
    obj = context
    for x in [r for r in row.values.split('/') if r]:
        if x == "..":
            if INavigationRoot.providedBy(obj):
                break
            parent = aq_parent(obj)
            if parent:
                obj = parent
        else:
            if base_hasattr(obj, x):
                child = getattr(obj, x, None)
                if child and base_hasattr(child, "getPhysicalPath"):
                    obj = child

    row = Row(index=row.index,
              operator=row.operator,
              values='/'.join(obj.getPhysicalPath()))

    return _path(context, row)


# Helper functions

def getPathByUID(context, uid):
    """Returns the path of an object specified by UID"""
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.unrestrictedSearchResults(dict(UID=uid))
    if brains:
        return brains[0].getPath()
    return ''
