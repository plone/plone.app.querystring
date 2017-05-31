# -*- coding: utf-8 -*-
from DateTime import DateTime
from datetime import datetime
from plone.app.querystring.indexmodifiers import query_index_modifiers

import unittest


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

    def test_date_modifier_list_DateTime(self):
        """Test a case with largerThanRelativeDate operatiors, where
        plone.app.querystring.querybuilder parses a querystring like this one:
        >>> query
        [{
            u'i': u'end',
            u'o': u'plone.app.querystring.operation.date.largerThanRelativeDate',  # noqa
            u'v': u'30'
        }]

        into something like this:
        >>> parsedquery
        {
            u'end': {
                'query': [
                    DateTime('2016/12/10 00:00:00 US/Central'),
                    DateTime('2017/01/09 23:59:59 US/Central')
                ],
                'range': 'minmax'
            },
        }
        """
        modifier = query_index_modifiers.start()
        query = {'query': [DateTime('01/01/2010'), DateTime('01/01/2010')]}
        self.assertTrue(
            isinstance(modifier(query)[1]['query'][0], DateTime)
        )

    def test_invalid_date(self):
        modifier = query_index_modifiers.start()
        query = {'query': 'foobar'}
        self.assertEquals(
            modifier(query)[1]['query'], 'foobar'
        )
