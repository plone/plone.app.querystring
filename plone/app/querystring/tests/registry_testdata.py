import os


parsed_correct = {
    "plone": {
        "app": {
            "querystring": {
                "field": {
                    "getId": {
                        "operations": ["plone.app.querystring.operation.string.is"],
                        "group": "Metadata",
                        "description": "The short name of an item " "(used in the url)",
                        "vocabulary": None,
                        "title": "Short Name",
                        "enabled": True,
                        "sortable": True,
                        "fetch_vocabulary": True,
                    },
                    "created": {
                        "operations": [
                            "plone.app.querystring.operation.date.lessThan",
                            "plone.app.querystring.operation.date.largerThan",
                        ],
                        "group": "Dates",
                        "description": "The time and date an item was " "created",
                        "vocabulary": None,
                        "title": "Creation Date",
                        "enabled": True,
                        "sortable": False,
                        "fetch_vocabulary": True,
                    },
                },
                "operation": {
                    "date": {
                        "largerThan": {
                            "widget": None,
                            "operation": "plone.app.querystring.queryparser"
                            "._largerThan",
                            "description": "Please use YYYY/MM/DD.",
                            "title": "after",
                        },
                        "lessThan": {
                            "widget": None,
                            "operation": "plone.app.querystring.queryparser."
                            "_lessThan",
                            "description": "Please use YYYY/MM/DD.",
                            "title": "before",
                        },
                    },
                    "string": {
                        "is": {
                            "widget": None,
                            "operation": "plone.app.querystring.queryparser._equal",
                            "description": "Tip: you can use * to autocomplete.",
                            "title": "equals",
                        }
                    },
                },
            }
        }
    }
}


def reg_load_xml(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as rx:
        return rx.read()


minimal_correct_xml = reg_load_xml("registry_minimal_correct.xml")
test_missing_operator_xml = reg_load_xml("registry_test_missing_operator.xml")
test_vocabulary_xml = reg_load_xml("registry_test_vocabulary.xml")
