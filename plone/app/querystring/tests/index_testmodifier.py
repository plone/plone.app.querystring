# -*- coding: utf8 -*-

from zope.interface import implementer
from plone.app.querystring.interfaces import IParsedQueryIndexModifier


@implementer(IParsedQueryIndexModifier)
class SimpleFooIndexModifier(object):
    """Test simple index modifier that do nothing"""

    def __call__(self, value):
        raise Exception("SimpleFooIndexModifier has been called!")


@implementer(IParsedQueryIndexModifier)
class TitleFooIndexModifier(object):
    """Test index modifier that check always Foo"""

    def __call__(self, value):
        return ('Title', 'Foo')


@implementer(IParsedQueryIndexModifier)
class AbstractToDescriptionIndexModifier(object):
    """
    Test index modifier that translate "Abstract" to Description index
    but where value do not count letter "e"
    """

    def __call__(self, value):
        value['query'] = value['query'].replace('e', '')
        return ('Description', value)
