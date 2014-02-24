from zope.component import queryUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


class RolesVocabulary(object):
    """Vocabulary factory for roles found in the portal plus the Anonymous Role
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        voc = queryUtility(IVocabularyFactory, 'plone.app.vocabularies.Roles')
        if not voc:
            voc = SimpleVocabulary([])
        voc = voc(context)
        anon = "Anonymous"
        voc._terms.append(voc.createTerm(anon, anon, anon))
        return SimpleVocabulary(voc._terms)

RolesVocabularyFactory = RolesVocabulary()
