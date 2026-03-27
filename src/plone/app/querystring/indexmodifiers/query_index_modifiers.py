from dateutil.parser import parse
from plone.app.querystring.interfaces import IParsedQueryIndexModifier
from zope.interface import implementer


@implementer(IParsedQueryIndexModifier)
class base:
    """DateIndex query modifier
    see Products.PluginIndexes.DateIndex.DateIndex.DateIndex._convert function
    """

    def __call__(self, value):
        def _normalize(val):
            """Encode value, parse dates."""

            if isinstance(val, str):
                try:
                    val = parse(val)
                except (ValueError, AttributeError):
                    pass

            return val

        query = value["query"]
        query = _normalize(query)

        if isinstance(query, list):
            aux = list()
            for item in query:
                aux.append(_normalize(item))
            query = aux

        value["query"] = query
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
