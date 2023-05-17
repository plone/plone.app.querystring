from .queryparser import parseAndModifyFormquery
from plone.app.vocabularies.catalog import CatalogVocabulary
from plone.base.navigationroot import get_navigation_root_object
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory


# this vocabulary is in this package by intend.
# since plone.app.querystring depends on plone.app.vocabularies
# we can not put it over there without creating a circular dependency.


@implementer(IVocabularyFactory)
class CatalogVocabularyFactory:
    """
    Test application of Navigation Root:

      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from plone.app.vocabularies.tests.base import DummyUrlTool
      >>> from plone.app.vocabularies.tests.base import DummyCatalog
      >>> class DummyPathCatalog(DummyCatalog):
      ...     def __call__(self, **query):
      ...         if 'path' in query and 'query' in query['path']:
      ...             return [v for v in self.values() if
      ...                     v.getPath().startswith(query['path']['query'])]
      ...         return self.values()
      >>> catalog = DummyPathCatalog(['/abcd', '/defg', '/dummy/sub-site',
      ...                             '/dummy/sub-site/ghij'])
      >>> context = create_context()
      >>> context.portal_catalog = catalog
      >>> context.portal_url = DummyUrlTool(context)
      >>> factory = CatalogVocabularyFactory()

      >>> sorted(t.token for t in factory(context))
      ['/abcd', '/defg', '/dummy/sub-site', '/dummy/sub-site/ghij']

      >>> from plone.app.vocabularies.tests.base import DummyNavRoot
      >>> nav_root = DummyNavRoot('sub-site', parent=context)
      >>> [t.token for t in factory(nav_root)]
      ['/dummy/sub-site', '/dummy/sub-site/ghij']

    """

    def __call__(self, context, query=None):
        parsed = {}
        if query:
            parsed = parseAndModifyFormquery(context, query["criteria"])
            if "sort_on" in query:
                parsed["sort_on"] = query["sort_on"]
            if "sort_order" in query:
                parsed["sort_order"] = str(query["sort_order"])

        if "path" not in parsed:
            site = getSite()
            nav_root = get_navigation_root_object(context, site)
            site_path = site.getPhysicalPath()
            if nav_root and nav_root.getPhysicalPath() != site_path:
                parsed["path"] = {
                    "query": "/".join(nav_root.getPhysicalPath()),
                    "depth": -1,
                }
        return CatalogVocabulary.fromItems(parsed, context)
