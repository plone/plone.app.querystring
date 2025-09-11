from zope.interface import Interface
from zope.schema import Bool
from zope.schema import DottedName
from zope.schema import List
from zope.schema import Text
from zope.schema import TextLine


class IQuerystringRegistryReader(Interface):
    """Adapts a registry object to parse the querystring data"""

    def __call__():
        """Return query string in dict-format."""


class IQueryOperation(Interface):
    title = TextLine(title="Title")
    description = Text(title="Description")
    operation = TextLine(title="Operation")
    widget = TextLine(title="Widget")


class IQueryField(Interface):
    title = TextLine(title="Title")
    description = Text(title="Description")
    enabled = Bool(title="Enabled")
    sortable = Bool(title="Sortable")
    fetch_vocabulary = Bool(title="Fetch vocabulary", default=True)
    operations = List(title="Operations", value_type=DottedName(title="Operation ID"))
    vocabulary = TextLine(title="Vocabulary")
    group = TextLine(title="Group")


class IParsedQueryIndexModifier(Interface):
    """Transform a parsed query index in something different"""

    def __call__(value):
        """
        Return a tuple with a new index name and a new value.
        if the index name returned is different from the native one, caller
        must replace treated index with the new ones.
        """


class IQueryModifier(Interface):
    """Modifies a query in order to inject specific or change given criteria."""

    def __call__(query):
        """
        modify the query and return an new one.
        """
