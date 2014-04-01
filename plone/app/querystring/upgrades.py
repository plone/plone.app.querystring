from Products.CMFCore.utils import getToolByName

def upgrade_1_to_2_typo_in_registry(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(
        'profile-plone.app.querystring:upgrade_1_to_2',
        'registry'
    )
