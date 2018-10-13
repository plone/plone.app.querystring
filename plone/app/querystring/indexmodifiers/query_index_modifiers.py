# -*- coding: utf8 -*-
from dateutil.parser import parse
from plone.app.querystring.interfaces import IParsedQueryIndexModifier
from zope.interface import implementer


import six


@implementer(IParsedQueryIndexModifier)
class Subject(object):

    """
    The Subject field in Plone currently uses a utf-8 encoded string.
    When a catalog query tries to compare a unicode string from the
    parsedquery with existing utf-8 encoded string indexes unindexing
    will fail with a UnicodeDecodeError. To prevent this from happening
    we always encode the Subject query.

    XXX: As soon as Plone uses unicode for all indexes, this code can
    be removed.
    """

    def __call__(self, value):
        query = value['query']
        # query can be a unicode string or a list of unicode strings.
        if six.PY2 and isinstance(query, six.text_type):
            query = query.encode("utf-8")
        elif isinstance(query, list):
            # We do not want to change the collections' own query string,
            # therefore we create a new copy of the list.
            copy_of_query = list(query)
            # Iterate over all query items and encode them if they are
            # unicode strings
            i = 0
            for item in copy_of_query:
                if six.PY2 and isinstance(item, six.text_type):
                    copy_of_query[i] = item.encode("utf-8")
                i += 1
            query = copy_of_query
        else:
            pass
        value['query'] = query
        return ('Subject', value)


@implementer(IParsedQueryIndexModifier)
class base(object):
    """DateIndex query modifier
    see Products.PluginIndexes.DateIndex.DateIndex.DateIndex._convert function
    """

    def __call__(self, value):

        def _normalize(val):
            """Encode value, parse dates.
            """
            if six.PY2 and isinstance(val, six.text_type):
                val = val.encode("utf-8")

            if isinstance(val, six.string_types):
                try:
                    val = parse(val)
                except (ValueError, AttributeError):
                    pass

            return val

        query = value['query']
        query = _normalize(query)

        if isinstance(query, list):
            aux = list()
            for item in query:
                aux.append(_normalize(item))
            query = aux

        value['query'] = query
        return (self.__class__.__name__, value)


class Date(base):
    pass


class created(base):
    pass


class effective(base):
    pass


class end(base):
    pass


class expires(base):
    pass


class modified(base):
    pass


class start(base):
    pass
