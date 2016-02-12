from datetime import datetime
from plone.app.querystring.indexmodifiers import query_index_modifiers

import unittest2 as unittest


class TestIndexModifiers(unittest.TestCase):

    def test_subject_encoded(self):
        self.assertEqual(
            query_index_modifiers.Subject()({'query': u'foobar'}),
            ('Subject', {'query': u'foobar'}))

    def test_date_modifier(self):
        modifier = query_index_modifiers.start()
        self.assertTrue(
            isinstance(modifier({'query': '2010-01-01'})[1]['query'], datetime)
        )
        self.assertTrue(
            isinstance(modifier({'query': '01/01/2010'})[1]['query'], datetime)
        )

    def test_date_modifier_list(self):
        modifier = query_index_modifiers.start()
        query = {'query': ['01/01/2010', '01/01/2010']}
        self.assertTrue(
            isinstance(modifier(query)[1]['query'][0], datetime)
        )

    def test_invalid_date(self):
        modifier = query_index_modifiers.start()
        query = {'query': 'foobar'}
        self.assertEquals(
            modifier(query)[1]['query'], 'foobar'
        )
