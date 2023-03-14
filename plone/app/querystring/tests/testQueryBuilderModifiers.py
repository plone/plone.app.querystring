from . import index_testmodifier
from plone.app.querystring.interfaces import IParsedQueryIndexModifier
from plone.app.querystring.testing import PLONEAPPQUERYSTRING_INTEGRATION_TESTING
from zope.component import getGlobalSiteManager
from zope.component import getMultiAdapter
from zope.publisher.browser import TestRequest

import unittest


class TestQuerybuilderExtended(unittest.TestCase):
    """Testing the IParsedQueryIndexModifier registration feature"""

    layer = PLONEAPPQUERYSTRING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

        self.portal.invokeFactory(
            "Document", "collectionstestpage1", title="Collectionstestpage"
        )
        testpage1 = self.portal["collectionstestpage1"]
        self.portal.portal_workflow.doActionFor(testpage1, "publish")
        self.portal.invokeFactory(
            "Document",
            "collectionstestpage2",
            title="Foo",
            description="Collectionstestpage",
        )
        testpage2 = self.portal["collectionstestpage2"]
        self.portal.portal_workflow.doActionFor(testpage2, "publish")
        self.portal.invokeFactory(
            "Document",
            "collectionstestpage3",
            title="Bar",
            description="Collctionststpag",
        )
        testpage3 = self.portal["collectionstestpage3"]
        self.portal.portal_workflow.doActionFor(testpage3, "publish")
        self.request = TestRequest()
        self.querybuilder = getMultiAdapter(
            (self.portal, self.request), name="querybuilderresults"
        )

    def testModifierNotCalled(self):
        gsm = getGlobalSiteManager()
        gsm.registerUtility(index_testmodifier.SimpleFooIndexModifier(), name="Foo")
        query = [
            {
                "i": "Title",
                "o": "plone.app.querystring.operation.string.is",
                "v": "Collectionstestpage",
            }
        ]

        try:
            results = self.querybuilder(query=query)
        except Exception:
            self.fail("Unexpected: index modifier has been called")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].Title(), "Collectionstestpage")
        gsm.unregisterUtility(provided=IParsedQueryIndexModifier, name="Foo")

    def testModifierChangeQuery(self):
        gsm = getGlobalSiteManager()
        gsm.registerUtility(index_testmodifier.TitleFooIndexModifier(), name="Title")
        query = [
            {
                "i": "Title",
                "o": "plone.app.querystring.operation.string.is",
                "v": "Collectionstestpage",
            }
        ]

        results = self.querybuilder(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].Title(), "Foo")
        gsm.unregisterUtility(provided=IParsedQueryIndexModifier, name="Title")

    def testModifierChangeQueryAndIndex(self):
        gsm = getGlobalSiteManager()
        gsm.registerUtility(
            index_testmodifier.AbstractToDescriptionIndexModifier(), name="Abstract"
        )
        query = [
            {
                "i": "Abstract",
                "o": "plone.app.querystring.operation.string.is",
                "v": "Collectionstestpage",
            }
        ]

        results = self.querybuilder(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].Title(), "Bar")
        gsm.unregisterUtility(provided=IParsedQueryIndexModifier, name="Abstract")
