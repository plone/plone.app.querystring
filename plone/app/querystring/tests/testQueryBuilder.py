from plone.app.querystring.testing import (
    TEST_PROFILE_PLONEAPPQUERYSTRING_INTEGRATION_TESTING,
)
from zope.component import getMultiAdapter
from zope.publisher.browser import TestRequest

import unittest


class TestQuerybuilder(unittest.TestCase):
    layer = TEST_PROFILE_PLONEAPPQUERYSTRING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

        self.portal.invokeFactory(
            "Document", "collectionstestpage", title="Collectionstestpage"
        )
        testpage = self.portal["collectionstestpage"]
        self.testpage = testpage
        self.portal.portal_workflow.doActionFor(testpage, "publish")
        self.request = TestRequest()
        self.querybuilder = getMultiAdapter(
            (self.portal, self.request), name="querybuilderresults"
        )
        self.query = [
            {
                "i": "Title",
                "o": "plone.app.querystring.operation.string.is",
                "v": "Collectionstestpage",
            }
        ]
        self.portal.invokeFactory("Folder", "testfolder", title="Test Folder")
        self.folder = self.portal.testfolder

    def testQueryBuilderQuery(self):
        results = self.querybuilder(query=self.query)
        self.assertEqual(results[0].Title(), "Collectionstestpage")

    def testQueryBuilderHTML(self):
        results = self.querybuilder.html_results(self.query)
        self.assertTrue("Collectionstestpage" in results)

    def testGettingConfiguration(self):
        res = self.folder.restrictedTraverse("@@querybuildernumberofresults")
        res(self.query)

    def testQueryBuilderNumberOfResults(self):
        results = self.querybuilder.number_of_results(self.query)
        numeric = int(results.split(" ")[0])
        self.assertEqual(numeric, 1)

    def testQueryBuilderNumberOfResultsView(self):
        res = self.folder.restrictedTraverse("@@querybuildernumberofresults")
        length_of_results = res.browserDefault(None)[0](self.query)
        # apparently browser traversal is different from the traversal we get
        # from restrictedTraverse. This did hurt a bit.
        numeric = int(length_of_results.split(" ")[0])
        self.assertEqual(numeric, 1)

    def testMakeQuery(self):
        results = self.querybuilder._makequery(query=self.query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), "http://nohost/plone/collectionstestpage")

    def testQueryStringIs(self):
        query = [
            {
                "i": "sortable_title",
                "o": "plone.app.querystring.operation.string.is",
                "v": "collectionstestpage",
            }
        ]

        # Test normal, without custom_query.
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].Title(), "Collectionstestpage")

    def testQueryStringIsNot(self):
        query = [
            {
                "i": "portal_type",
                "o": "plone.app.querystring.operation.selection.none",
                "v": "Plone Site",
            },
            {
                "i": "sortable_title",
                "o": "plone.app.querystring.operation.string.isNot",
                "v": "collectionstestpage",
            },
        ]

        # Test normal, without custom_query.
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].Title(), "Test Folder")

    def testMakeQueryWithSubject(self):
        self.testpage.setSubject(["Lorem"])
        self.testpage.reindexObject()
        query = [
            {
                "i": "Subject",
                "o": "plone.app.querystring.operation.selection.any",
                "v": "Lorem",
            }
        ]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), "http://nohost/plone/collectionstestpage")

    def testMakeQueryWithSubjectNot(self):
        self.folder.setSubject(["Ipsum"])
        self.folder.reindexObject()
        self.testpage.setSubject(["Lorem"])
        self.testpage.reindexObject()
        query = [
            {
                "i": "Subject",
                "o": "plone.app.querystring.operation.selection.none",
                "v": "Lorem",
            }
        ]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), "http://nohost/plone/testfolder")

    def testMakeQueryWithMultipleSubject(self):
        self.testpage.setSubject(["Lorem"])
        self.testpage.reindexObject()
        query = [
            {
                "i": "Subject",
                "o": "plone.app.querystring.operation.selection.any",
                "v": ["Lorem", "Ipsum"],
            }
        ]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), "http://nohost/plone/collectionstestpage")

    def testMakeQueryWithMultipleSubjectNot(self):
        self.folder.setSubject(["Ipsum"])
        self.folder.reindexObject()
        self.testpage.setSubject(["Lorem"])
        self.testpage.reindexObject()
        query = [
            {
                "i": "Subject",
                "o": "plone.app.querystring.operation.selection.none",
                "v": ["Lorem", "Dolor"],
            }
        ]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), "http://nohost/plone/testfolder")

    def testMakeQueryWithSubjectWithSpecialCharacters(self):
        self.testpage.setSubject(["Äüö"])
        self.testpage.reindexObject()
        query = [
            {
                "i": "Subject",
                "o": "plone.app.querystring.operation.selection.any",
                "v": "Äüö",
            }
        ]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), "http://nohost/plone/collectionstestpage")
        self.assertEqual(results[0].getObject().Subject(), ("Äüö",))

    def testMakeQueryWithUnicodeSubjectWithSpecialCharacters(self):
        self.testpage.setSubject(["Äüö"])
        self.testpage.reindexObject()
        query = [
            {
                "i": "Subject",
                "o": "plone.app.querystring.operation.selection.any",
                "v": "Äüö",
            }
        ]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), "http://nohost/plone/collectionstestpage")
        self.assertEqual(results[0].getObject().Subject(), ("Äüö",))

    def testMakeQueryWithUnicodeSubjectWithMultipleSubjects(self):
        self.testpage.setSubject(["Äüö"])
        self.testpage.reindexObject()
        query = [
            {
                "i": "Subject",
                "o": "plone.app.querystring.operation.selection.any",
                "v": ["Äüö", "Üöß"],
            }
        ]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), "http://nohost/plone/collectionstestpage")
        self.assertEqual(results[0].getObject().Subject(), ("Äüö",))

    def testMakeQueryWithSearchableText(self):
        query = [
            {
                "i": "SearchableText",
                "o": "plone.app.querystring.operation.string.contains",
                "v": "Test",
            }
        ]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), "http://nohost/plone/testfolder")

    def testMakeQueryWithSearchableTextSpecialWordsAnd(self):
        self.testpage.description = "This and that is the description"
        self.testpage.reindexObject()
        query = [
            {
                "i": "SearchableText",
                "o": "plone.app.querystring.operation.string.contains",
                "v": "This and that",
            }
        ]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), "http://nohost/plone/collectionstestpage")

    def testMakeQueryWithSearchableTextSpecialWordsOr(self):
        self.testpage.description = "This or that is the description"
        self.testpage.reindexObject()
        query = [
            {
                "i": "SearchableText",
                "o": "plone.app.querystring.operation.string.contains",
                "v": "This or that",
            }
        ]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), "http://nohost/plone/collectionstestpage")

    def testQueryBuilderCustomQuery(self):
        """Test, if custom queries are respected when getting the results."""

        # It would be slightly nicer to compare directly against the changed
        # query. But instead we have to test for changed results, as _makequery
        # returns the results but not the query.

        query = [
            {
                "i": "Title",
                "o": "plone.app.querystring.operation.string.is",
                "v": "Collectionstestpage",
            }
        ]

        # Test normal, without custom_query.
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].Title(), "Collectionstestpage")

        # Test with changed ``Title`` query, overwriting original query.
        results = self.querybuilder._makequery(
            query=query, custom_query={"Title": {"query": "Test Folder"}}
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].Title(), "Test Folder")

        # Test with changed ``portal_type``, but other ``Title`` query.
        results = self.querybuilder._makequery(
            query=query, custom_query={"portal_type": {"query": "Folder"}}
        )
        self.assertEqual(len(results), 0)

        # Test with changed ``portal_type`` and changed ``Title``.
        results = self.querybuilder._makequery(
            query=query,
            custom_query={
                "Title": {"query": "Test Folder"},
                "portal_type": {"query": "Folder"},
            },
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].Title(), "Test Folder")

    def testQueryBuilderCustomQueryDoNotOverrideValues(self):
        """Test if custom queries do not override values if they are dicts"""
        self.portal.invokeFactory(
            "Document", "collectionstestpage-2", title="Collectionstestpage 2"
        )
        testpage2 = self.portal["collectionstestpage-2"]
        query = [
            {
                "i": "UID",
                "o": "plone.app.querystring.operation.string.is",
                "v": [self.testpage.UID(), testpage2.UID()],
            }
        ]

        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].Title(), "Collectionstestpage")
        self.assertEqual(results[1].Title(), "Collectionstestpage 2")

        # if we add new values to the query, they should not be overwritten
        results = self.querybuilder._makequery(
            query=query, custom_query={"UID": {"not": testpage2.UID()}}
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].Title(), "Collectionstestpage")

        # if we add the same values to the query, they should be overwritten
        results = self.querybuilder._makequery(
            query=query, custom_query={"UID": {"query": testpage2.UID()}}
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].Title(), "Collectionstestpage 2")

        # add simple custom query
        results = self.querybuilder._makequery(
            query=query, custom_query={"UID": testpage2.UID()}
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].Title(), "Collectionstestpage 2")


class TestQuerybuilderResultTypes(unittest.TestCase):
    layer = TEST_PROFILE_PLONEAPPQUERYSTRING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = TestRequest()
        self.querybuilder = getMultiAdapter(
            (self.portal, self.request), name="querybuilderresults"
        )
        self.query = [
            {
                "i": "Title",
                "o": "plone.app.querystring.operation.string.is",
                "v": "Non-existent",
            }
        ]

    def testQueryBuilderEmptyQueryContentListing(self):
        results = self.querybuilder(query={})
        self.assertEqual(len(results), 0)
        self.assertEqual(type(results).__name__, "ContentListing")

    def testQueryBuilderEmptyQueryBrains(self):
        results = self.querybuilder(query={}, brains=True)
        self.assertEqual(len(results), 0)
        self.assertEqual(results, [])

    def testQueryBuilderEmptyQueryBatch(self):
        results = self.querybuilder(query={}, batch=True)
        self.assertEqual(len(results), 0)
        self.assertEqual(type(results).__name__, "BaseBatch")

    def testQueryBuilderNonEmptyQueryContentListing(self):
        results = self.querybuilder(query=self.query)
        self.assertEqual(len(results), 0)
        self.assertEqual(type(results).__name__, "ContentListing")

    def testQueryBuilderNonEmptyQueryBrains(self):
        results = self.querybuilder(query=self.query, brains=True)
        self.assertEqual(len(results), 0)
        self.assertEqual(type(results).__name__, "LazyCat")

    def testQueryBuilderNonEmptyQueryBatch(self):
        results = self.querybuilder(query=self.query, batch=True)
        self.assertEqual(len(results), 0)
        self.assertEqual(type(results).__name__, "BaseBatch")

    def testQueryBuilderNonEmptyContentListingCustomQuery(self):
        results = self.querybuilder(
            query={}, custom_query={"portal_type": "NonExistent"}
        )
        self.assertEqual(len(results), 0)
        self.assertEqual(type(results).__name__, "ContentListing")


class TestConfigurationFetcher(unittest.TestCase):
    layer = TEST_PROFILE_PLONEAPPQUERYSTRING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.portal.invokeFactory("Folder", "testfolder", title="Test Folder")
        self.folder = self.portal.testfolder

    def testGettingJSONConfiguration(self):
        self.folder.restrictedTraverse("@@querybuilderjsonconfig")()
