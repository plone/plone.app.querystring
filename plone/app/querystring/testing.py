# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing.layers import IntegrationTesting
from plone.testing import z2
from zope.configuration import xmlconfig


class PloneAppQuerystringTestProfileLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.querystring.tests
        self.loadZCML('configure.zcml', package=plone.app.querystring.tests)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.querystring.tests:registry')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.acl_users.userFolderAddUser('admin',
                                           'secret',
                                           ['Manager'],
                                           [])
        portal.portal_workflow.setChainForPortalTypes(
            ('Document',), 'plone_workflow'
        )


TEST_PROFILE_PLONEAPPQUERYSTRING_FIXTURE = \
    PloneAppQuerystringTestProfileLayer()


class PloneAppQuerystringLayer(PloneAppQuerystringTestProfileLayer):

    def setUpZope(self, app, configurationContext):
        super(PloneAppQuerystringLayer, self).setUpZope(
            app, configurationContext)
        import plone.app.querystring
        xmlconfig.file(
            'configure.zcml',
            plone.app.querystring,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        super(PloneAppQuerystringLayer, self).setUpPloneSite(portal)
        applyProfile(portal, 'plone.app.querystring:default')

PLONEAPPQUERYSTRING_FIXTURE = PloneAppQuerystringLayer()


PLONEAPPQUERYSTRING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEAPPQUERYSTRING_FIXTURE,),
    name="PloneAppQuerystringLayer:Integration")

TEST_PROFILE_PLONEAPPQUERYSTRING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TEST_PROFILE_PLONEAPPQUERYSTRING_FIXTURE,),
    name="PloneAppQuerystringTestProfileLayer:Integration")

NOT_INSTALLED_PLONEAPPQUERYSTRING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PloneSandboxLayer(),),
    name="UninstalledPloneAppQuerystringLayer:Integration")
