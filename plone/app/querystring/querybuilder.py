import json

from plone.app.contentlisting.interfaces import IContentListing
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import getNavigationRoot
from plone.batching import Batch
from zope.component import getMultiAdapter, getUtility
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.publisher.browser import BrowserView

from plone.app.querystring import queryparser
from plone.app.querystring.interfaces import IQuerystringRegistryReader

_ = MessageFactory('plone')


class ContentListingView(BrowserView):
    """BrowserView for displaying query results"""

    def __call__(self, **kw):
        return self.index(**kw)


class QueryBuilder(BrowserView):
    """ This view is used by the javascripts,
        fetching configuration or results"""

    def __init__(self, context, request):
        super(QueryBuilder, self).__init__(context, request)
        self._results = None

    def __call__(self, query, batch=False, b_start=0, b_size=30,
                 sort_on=None, sort_order=None, limit=0, brains=False):
        """If there are results, make the query and return the results"""
        if self._results is None:
            self._results = self._makequery(query=query, batch=batch,
                b_start=b_start, b_size=b_size, sort_on=sort_on,
                sort_order=sort_order, limit=limit, brains=brains)
        return self._results

    def html_results(self, query):
        """html results, used for in the edit screen of a collection,
           used in the live update results"""
        options = dict(original_context=self.context)
        results = self(query, sort_on=self.request.get('sort_on', None),
                       sort_order=self.request.get('sort_order', None),
                       limit=10)

        return getMultiAdapter((results, self.request),
            name='display_query_results')(**options)

    def _makequery(self, query=None, batch=False, b_start=0, b_size=30,
                   sort_on=None, sort_order=None, limit=0, brains=False):
        """Parse the (form)query and return using multi-adapter"""
        parsedquery = queryparser.parseFormquery(
            self.context, query, sort_on, sort_order)
        if not parsedquery:
            if brains:
                return []
            else:
                return IContentListing([])

        catalog = getToolByName(self.context, 'portal_catalog')
        if batch:
            parsedquery['b_start'] = b_start
            parsedquery['b_size'] = b_size
        elif limit:
            parsedquery['sort_limit'] = limit
        if 'path' not in parsedquery:
            parsedquery['path'] = getNavigationRoot(self.context)

        # The Subject field in Plone currently uses a utf-8 encoded string.
        # When a catalog query tries to compare a unicode string from the
        # parsedquery with existing utf-8 encoded string indexes unindexing
        # will fail with a UnicodeDecodeError. To prevent this from happening
        # we always encode the Subject query.
        # XXX: As soon as Plone uses unicode for all indexes, this code can
        # be removed.
        if 'Subject' in parsedquery:
            if isinstance(parsedquery['Subject']['query'], unicode):
                parsedquery['Subject']['query'] = \
                    parsedquery['Subject']['query'].encode("utf-8")

        results = catalog(parsedquery)
        if not brains:
            results = IContentListing(results)
        if batch:
            results = Batch(results, b_size, start=b_start)
        return results

    def number_of_results(self, query):
        """Get the number of results"""
        results = self(query, sort_on=None, sort_order=None, limit=1)
        return translate(_(u"batch_x_items_matching_your_criteria",
                 default=u"${number} items matching your search terms.",
                 mapping={'number': results.actual_result_count}),
                 context=self.request)


class RegistryConfiguration(BrowserView):

    def __call__(self):
        """Return the registry configuration in JSON format"""
        return json.dumps(IQuerystringRegistryReader(getUtility(IRegistry))())
