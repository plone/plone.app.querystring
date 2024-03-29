from plone.app.querystring.interfaces import IQuerystringRegistryReader
from plone.app.querystring.registryreader import DottedDict
from plone.app.querystring.testing import PLONEAPPQUERYSTRING_INTEGRATION_TESTING
from plone.app.querystring.tests import registry_testdata as td
from plone.registry import Registry
from plone.registry.interfaces import IRegistry
from zope.component import getGlobalSiteManager
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

import unittest


@implementer(IVocabularyFactory)
class TestVocabulary:
    def __call__(self, context):
        term = "subsite term" if getattr(context, "id", None) == "subsite" else "term"
        return SimpleVocabulary([SimpleVocabulary.createTerm(term, term, term)])


class TestRegistryReader(unittest.TestCase):
    layer = PLONEAPPQUERYSTRING_INTEGRATION_TESTING

    def setUp(self):
        gsm = getGlobalSiteManager()
        gsm.registerUtility(
            TestVocabulary(),
            IVocabularyFactory,
            "plone.app.querystring.tests.testvocabulary",
        )

    def getLogger(self, value):
        return "plone.app.querystring"

    def shouldPurge(self):
        return False

    def createRegistry(self, xml):
        """Create a registry from a minimal set of fields and operators"""
        from plone.app.registry.exportimport.handler import RegistryImporter

        gsm = getGlobalSiteManager()
        self.registry = Registry()
        gsm.registerUtility(self.registry, IRegistry)

        importer = RegistryImporter(self.registry, self)
        if isinstance(xml, str):
            # String can work, but not when it has an encoding declaration.
            # It would give a ValueError:
            # "Unicode strings with encoding declaration are not supported.
            # Please use bytes input or XML fragments without declaration."

            xml = xml.encode("utf-8")
        importer.importDocument(xml)
        return self.registry

    def test_dotted_dict(self):
        """test the dotted dict type which is used by the registry reader to
        access dicts in dicts by dotted names. (eg field.created.operations)
        it should raise a keyerror when an invalid key is used
        TODO : DottedDict should be in a separate package
        """
        dd = DottedDict({"my": {"dotted": {"name": "value"}}})
        self.assertEqual(dd.get("my.dotted.name"), "value")
        self.assertRaises(KeyError, dd.get, "my.dotted.wrongname")
        dd = DottedDict({"my": "value"})
        self.assertEqual(dd.get("my"), "value")

    def test_parse_registry(self):
        """tests if the parsed registry data is correct"""
        registry = self.createRegistry(td.minimal_correct_xml)
        reader = IQuerystringRegistryReader(registry)
        result = reader.parseRegistry()
        self.assertEqual(result, td.parsed_correct)

    def test_get_vocabularies(self):
        """tests if getVocabularyValues is returning the correct vocabulary
        values in the correct format
        """
        registry = self.createRegistry(td.test_vocabulary_xml)
        reader = IQuerystringRegistryReader(registry)
        result = reader.parseRegistry()
        result = reader.getVocabularyValues(result)
        vocabulary_result = result.get("plone.app.querystring.field.reviewState.values")
        self.assertEqual(vocabulary_result, {"term": {"title": "term"}})

    def test_get_vocabularies_in_context(self):
        portal = self.layer["portal"]
        subsite = portal[portal.invokeFactory("Document", "subsite", title="Subsite")]

        registry = self.createRegistry(td.test_vocabulary_xml)
        reader = IQuerystringRegistryReader(registry)
        reader.vocab_context = subsite
        result = reader.parseRegistry()
        result = reader.getVocabularyValues(result)
        vocabulary_result = result.get("plone.app.querystring.field.reviewState.values")
        self.assertEqual(vocabulary_result, {"subsite term": {"title": "subsite term"}})

    def test_map_operations_clean(self):
        """tests if mapOperations is getting all operators correctly"""
        registry = self.createRegistry(td.minimal_correct_xml)
        reader = IQuerystringRegistryReader(registry)
        result = reader.parseRegistry()
        result = reader.mapOperations(result)
        operations = result.get("plone.app.querystring.field.created.operations")
        operators = result.get("plone.app.querystring.field.created.operators")
        for operation in operations:
            self.assertTrue(operation in operators)

    def test_map_operations_missing(self):
        """tests if nonexisting referenced operations are properly skipped"""
        registry = self.createRegistry(td.test_missing_operator_xml)
        reader = IQuerystringRegistryReader(registry)
        result = reader.parseRegistry()
        result = reader.mapOperations(result)
        operators = result.get("plone.app.querystring.field.created.operators").keys()
        self.assertTrue("plone.app.querystring.operation.date.lessThan" in operators)
        self.assertFalse("plone.app.querystring.operation.date.largerThan" in operators)

    def test_sortable_indexes(self):
        """tests if sortable indexes from the registry will be available in
        the parsed registry
        """
        registry = self.createRegistry(td.minimal_correct_xml)
        reader = IQuerystringRegistryReader(registry)
        result = reader.parseRegistry()
        result = reader.mapOperations(result)
        result = reader.mapSortableIndexes(result)
        sortables = result["sortable"]

        # there should be one sortable index
        self.assertEqual(len(sortables), 1)

        # confirm that every sortable really is sortable
        for field in sortables.values():
            self.assertEqual(field["sortable"], True)

    def test_registry_adapter(self):
        """tests the __call__ method of the IQuerystringRegistryReader
        adapter
        """
        registry = self.createRegistry(td.minimal_correct_xml)
        reader = IQuerystringRegistryReader(registry)
        result = reader()
        self.assertEqual(
            sorted(list(result.keys())),
            ["indexes", "sortable_indexes"],
        )
