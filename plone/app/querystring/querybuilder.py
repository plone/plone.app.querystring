from operator import itemgetter
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.querystring import queryparser
from plone.app.querystring.interfaces import IParsedQueryIndexModifier
from plone.app.querystring.interfaces import IQueryModifier
from plone.app.querystring.interfaces import IQuerystringRegistryReader
from plone.batching import Batch
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.publisher.browser import BrowserView

import json
import logging
import re


logger = logging.getLogger("plone.app.querystring")
_ = MessageFactory("plone")

# We should accept both a simple space, unicode u'\u0020 but also a
# multi-space, so called 'waji-kankaku', unicode u'\u3000'
_MULTISPACE = "\u3000"
_BAD_CHARS = ("?", "-", "+", "*", _MULTISPACE)


def _quote_chars(s):
    # We need to quote parentheses when searching text indices
    if "(" in s:
        s = s.replace("(", '"("')
    if ")" in s:
        s = s.replace(")", '")"')
    if _MULTISPACE in s:
        s = s.replace(_MULTISPACE, " ")
    return s


def _quote(term):
    # The terms and, or and not must be wrapped in quotes to avoid
    # being parsed as logical query atoms.
    if term.lower() in ("and", "or", "not"):
        term = '"%s"' % term
    return term


def munge_search_term(query):
    for char in _BAD_CHARS:
        query = query.replace(char, " ")

    # extract quoted phrases first
    quoted_phrases = re.findall(r'"([^"]*)"', query)
    r = []
    for qp in quoted_phrases:
        # remove from original query
        query = query.replace(f'"{qp}"', "")
        # replace with cleaned leading/trailing whitespaces
        # and skip empty phrases
        clean_qp = qp.strip()
        if not clean_qp:
            continue
        r.append(f'"{clean_qp}"')

    r += map(_quote, query.strip().split())
    r = " AND ".join(r)
    r = _quote_chars(r) + ("*" if r and not r.endswith('"') else "")
    return r


class ContentListingView(BrowserView):
    """BrowserView for displaying query results"""

    def __call__(self, **kw):
        return self.index(**kw)


class QueryBuilder(BrowserView):
    """This view is used by the javascripts,
    fetching configuration or results"""

    def __init__(self, context, request):
        super().__init__(context, request)
        self._results = None

    def __call__(
        self,
        query,
        batch=False,
        b_start=0,
        b_size=30,
        sort_on=None,
        sort_order=None,
        limit=0,
        brains=False,
        custom_query=None,
    ):
        """Create a zope catalog query and return results.

        :param query: The querystring to be parsed into a zope catalog query.
        :type query: dictionary

        :param batch: Return a plone.batching ``Batch`` instead of a zope
                      catalog result.
        :type batch: boolean

        :param b_start: Start item of the batch.
        :type b_start: integer

        :param b_size: Size of the batch.
        :type b_size: integer

        :param sort_on: Name of the sort index for sorting the results.
        :type sort_on: string

        :param sort_order: The order of the result sorting. Either 'ascending'
                           or 'descending'. 'reverse' is an alias equivalent
                           to 'descending'.
        :type sort_order: string

        :param limit: Limit the results.
        :type limit: integer

        :param brains: Return brains or IContentListing objects.
        :type brains: boolean

        :param custom_query: A dictionary of index names and their associated
                             query values. The custom_query updates the parsed
                             query, thus overriding the query string.
                             May be None.
        :type custom_query: dictionary or None

        """
        if self._results is None:
            self._results = self._makequery(
                query=query,
                batch=batch,
                b_start=b_start,
                b_size=b_size,
                sort_on=sort_on,
                sort_order=sort_order,
                limit=limit,
                brains=brains,
                custom_query=custom_query,
            )
        return self._results

    def html_results(self, query):
        """html results, used for in the edit screen of a collection,
        used in the live update results"""
        options = dict(original_context=self.context)
        results = self(
            query,
            sort_on=self.request.get("sort_on", None),
            sort_order=self.request.get("sort_order", None),
            limit=10,
        )

        return getMultiAdapter((results, self.request), name="display_query_results")(
            **options
        )

    def _makequery(
        self,
        query=None,
        batch=False,
        b_start=0,
        b_size=30,
        sort_on=None,
        sort_order=None,
        limit=0,
        brains=False,
        custom_query=None,
    ):
        """Parse the (form)query and return using multi-adapter"""
        query_modifiers = getUtilitiesFor(IQueryModifier)
        for name, modifier in sorted(query_modifiers, key=itemgetter(0)):
            query = modifier(query)

        parsedquery = queryparser.parseFormquery(
            self.context, query, sort_on, sort_order
        )

        index_modifiers = getUtilitiesFor(IParsedQueryIndexModifier)
        for name, modifier in index_modifiers:
            if name in parsedquery:
                new_name, query = modifier(parsedquery[name])
                parsedquery[name] = query
                # if a new index name has been returned, we need to replace
                # the native ones
                if name != new_name:
                    del parsedquery[name]
                    parsedquery[new_name] = query

        # Check for valid indexes
        catalog = getToolByName(self.context, "portal_catalog")
        valid_indexes = [index for index in parsedquery if index in catalog.indexes()]

        # We'll ignore any invalid index, but will return an empty set if none
        # of the indexes are valid.
        if not valid_indexes:
            logger.warning("Using empty query because there are no valid indexes used.")
            parsedquery = {}

        empty_query = not parsedquery  # store emptiness

        if batch:
            parsedquery["b_start"] = b_start
            parsedquery["b_size"] = b_size
        elif limit:
            parsedquery["sort_limit"] = limit

        if "path" not in parsedquery:
            parsedquery["path"] = {"query": ""}

        if isinstance(custom_query, dict) and custom_query:
            # Update the parsed query with an extra query dictionary. This may
            # override the parsed query. The custom_query is a dictionary of
            # index names and their associated query values.
            for key in custom_query:
                if isinstance(parsedquery.get(key), dict) and isinstance(
                    custom_query.get(key), dict
                ):
                    parsedquery[key].update(custom_query[key])
                    continue
                parsedquery[key] = custom_query[key]
            empty_query = False

        # filter bad term and operator in query
        parsedquery = self.filter_query(parsedquery)
        results = []
        if not empty_query:
            results = catalog(**parsedquery)
            if (
                getattr(results, "actual_result_count", False)
                and limit
                and results.actual_result_count > limit
            ):
                results.actual_result_count = limit

        if not brains:
            results = IContentListing(results)
        if batch:
            results = Batch(results, b_size, start=b_start)
        return results

    def number_of_results(self, query):
        """Get the number of results"""
        results = self(query, sort_on=None, sort_order=None, limit=1)
        return translate(
            _(
                "batch_x_items_matching_your_criteria",
                default="${number} items matching your search terms.",
                mapping={"number": results.actual_result_count},
            ),
            context=self.request,
        )

    def filter_query(self, query):
        text = query.get("SearchableText", None)
        if isinstance(text, dict):
            text = text.get("query", "")
        if text:
            query["SearchableText"] = self.munge_search_term(text)
        return query

    def munge_search_term(self, q):
        return munge_search_term(q)


class RegistryConfiguration(BrowserView):
    def __call__(self):
        registry = getUtility(IRegistry)
        reader = getMultiAdapter((registry, self.request), IQuerystringRegistryReader)
        data = reader()
        return json.dumps(data)
