from plone.app.vocabularies.tests.test_vocabularies import vocabSetUp
from plone.app.vocabularies.tests.test_vocabularies import vocabTearDown

import doctest
import unittest


def test_suite():
    optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    return unittest.TestSuite(
        (
            doctest.DocTestSuite(
                "plone.app.vocabularies.catalog",
                setUp=vocabSetUp,
                tearDown=vocabTearDown,
                optionflags=optionflags,
            ),
        )
    )
