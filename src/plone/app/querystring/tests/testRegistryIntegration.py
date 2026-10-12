from plone.app.querystring.testing import PLONEAPPQUERYSTRING_INTEGRATION_TESTING
from plone.app.testing import applyProfile

import unittest


class TestOperationDefinitions(unittest.TestCase):
    layer = PLONEAPPQUERYSTRING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

    def test_string_equality(self):
        registry = self.portal.portal_registry

        prefix = "plone.app.querystring.operation.string.is"
        self.assertTrue(prefix + ".title" in registry)

        self.assertEqual(registry[prefix + ".title"], "Is")
        self.assertEqual(
            registry[prefix + ".description"], "Tip: you can use * to autocomplete."
        )
        self.assertEqual(
            registry[prefix + ".operation"], "plone.app.querystring.queryparser._equal"
        )

    def test_date_lessthan(self):
        registry = self.portal.portal_registry
        prefix = "plone.app.querystring.operation.date.lessThan"

        self.assertTrue(prefix + ".title" in registry)

        self.assertEqual(registry[prefix + ".title"], "Before date")
        self.assertEqual(registry[prefix + ".description"], "Please use YYYY/MM/DD.")
        self.assertEqual(
            registry[prefix + ".operation"],
            "plone.app.querystring.queryparser._dateLessThan",
        )

    def test_current_uid(self):
        registry = self.portal.portal_registry
        prefix = "plone.app.querystring.operation.string.currentUID"

        self.assertTrue(prefix + ".title" in registry)

        self.assertEqual(registry[prefix + ".title"], "Current item")
        self.assertEqual(
            registry[prefix + ".operation"],
            "plone.app.querystring.queryparser._currentUID",
        )
        self.assertIsNone(registry[prefix + ".widget"])


class TestFieldDefinitions(unittest.TestCase):
    layer = PLONEAPPQUERYSTRING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

    def test_getId(self):
        registry = self.portal.portal_registry
        prefix = "plone.app.querystring.field.getId"
        self.assertTrue(prefix + ".title" in registry)

        self.assertEqual(registry[prefix + ".title"], "Short name (id)")

        operations = registry[prefix + ".operations"]
        self.assertEqual(len(operations), 2)

        equal = "plone.app.querystring.operation.string.is"
        self.assertTrue(equal in operations)

        exclude = "plone.app.querystring.operation.string.isNot"
        self.assertTrue(exclude in operations)

        self.assertEqual(
            registry[prefix + ".description"],
            "The short name of an item (used in the url)",
        )
        self.assertEqual(registry[prefix + ".enabled"], True)
        self.assertEqual(registry[prefix + ".sortable"], True)
        self.assertEqual(registry[prefix + ".group"], "Metadata")

    def test_getobjpositioninparent_largerthan(self):
        """Bug reported as Issue #22

        Names not matching for operations getObjPositionInParent
        see also https://github.com/plone/plone.app.querystring/issues/22
        """
        key = "plone.app.querystring.field.getObjPositionInParent.operations"
        operation = "plone.app.querystring.operation.int.largerThan"
        registry = self.portal.portal_registry

        # check if operation is used for getObjPositionInParent
        operations = registry.get(key)
        self.assertTrue(operation in operations)

    def test_path_sortable(self):
        registry = self.portal.portal_registry
        self.assertEqual(registry["plone.app.querystring.field.path.sortable"], True)


class TestUpgradeTo16(unittest.TestCase):
    layer = PLONEAPPQUERYSTRING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        registry = self.portal.portal_registry
        # Bring the registry back to its state before version 16
        prefix = "plone.app.querystring.operation.string.currentUID."
        for key in [k for k in registry.records.keys() if k.startswith(prefix)]:
            del registry.records[key]
        registry["plone.app.querystring.field.path.sortable"] = False

    def test_upgrade(self):
        registry = self.portal.portal_registry
        prefix = "plone.app.querystring.operation.string.currentUID"
        self.assertFalse(prefix + ".title" in registry)

        applyProfile(self.portal, "plone.app.querystring:upgrade_to_16")

        self.assertEqual(registry[prefix + ".title"], "Current item")
        self.assertEqual(
            registry[prefix + ".operation"],
            "plone.app.querystring.queryparser._currentUID",
        )
        field = "plone.app.querystring.field.path"
        self.assertEqual(registry[field + ".sortable"], True)
        # The other values of the path field are kept
        self.assertEqual(registry[field + ".title"], "Location")
        self.assertEqual(len(registry[field + ".operations"]), 3)
