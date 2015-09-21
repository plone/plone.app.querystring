# -*- coding: utf-8 -*-
from collections import OrderedDict
from plone.app.querystring.interfaces import IQuerystringRegistryReader
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone.utils import safe_unicode
from Products.ZCTextIndex.interfaces import IZCTextIndex
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.i18nmessageid import Message
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
import logging

logger = logging.getLogger("plone.app.querystring")


class DottedDict(dict):
    """A dictionary where you can access nested dicts with dotted names"""

    def get(self, k, default=None):
        if '.' not in k:
            return super(DottedDict, self).get(k, default)
        val = self
        for x in k.split('.'):
            val = val[x]
        return val


@implementer(IQuerystringRegistryReader)
class QuerystringRegistryReader(object):
    """Adapts a registry object to parse the querystring data."""

    prefix = "plone.app.querystring"

    def __init__(self, context, request=None):
        if request is None:
            request = getRequest()

        self.context = context
        self.request = request

    def parseRegistry(self):
        """Make a dictionary structure for the values in the registry"""

        result = DottedDict()

        for record in self.context.records:
            if not record.startswith(self.prefix):
                continue

            splitted = record.split('.')
            current = result
            for x in splitted[:-1]:
                # create the key if it's not there
                if x not in current:
                    current[x] = {}
                current = current[x]

            # store actual key/value
            key = splitted[-1]
            value = self.context.records[record].value
            if isinstance(value, Message):
                value = translate(value, context=self.request)
            current[key] = value

        return result

    def getVocabularyValues(self, values):
        """Get all vocabulary values if a vocabulary is defined"""

        for field in values.get(self.prefix + '.field').values():
            field['values'] = OrderedDict()
            vocabulary = field.get('vocabulary', [])
            if not vocabulary:
                continue
            utility = queryUtility(IVocabularyFactory, vocabulary)
            if utility is None:
                logger.info("%s is missing, ignored." % vocabulary)
                continue
            translated = []
            for item in utility(self.context):
                if isinstance(item.title, Message):
                    title = translate(item.title, context=self.request)
                else:
                    title = item.title
                translated.append((title, item.value))
            translated = sorted(
                translated,
                key=lambda x: normalizeString(safe_unicode(x[0]))
            )
            for (title, value) in translated:
                field['values'][value] = {'title': title}

        return values

    def mapOperations(self, values):
        """Get the operations from the registry and put them in the key
           'operators' with the short name as key
        """
        for field in values.get(self.prefix + '.field').values():
            fieldoperations = field.get('operations', [])
            field['operators'] = {}
            for operation_key in fieldoperations:
                try:
                    field['operators'][operation_key] = \
                        values.get(operation_key)
                except KeyError:
                    # invalid operation, probably doesn't exist, pass for now
                    pass
        return values

    def mapSortableIndexes(self, values):
        """Map sortable indexes"""
        catalog = getToolByName(getSite(), 'portal_catalog')._catalog
        sortables = {}
        for key, field in values.get('%s.field' % self.prefix).iteritems():
            if (
                field['sortable']
                and key in catalog.indexes
                and not IZCTextIndex.providedBy(catalog.getIndex(key))
            ):
                sortables[key] = values.get('%s.field.%s' % (self.prefix, key))
        values['sortable'] = sortables
        return values

    def __call__(self):
        """Return the registry configuration in JSON format"""

        indexes = self.parseRegistry()
        indexes = self.getVocabularyValues(indexes)
        indexes = self.mapOperations(indexes)
        indexes = self.mapSortableIndexes(indexes)
        return {
            'indexes': indexes.get('%s.field' % self.prefix),
            'sortable_indexes': indexes.get('sortable'),
        }
