# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable as \
    INonInstallableProfiles
from zope.interface import implementer


@implementer(INonInstallableProfiles)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Returns a list of profiles that should not be available for
           installation at portal creation time.

           The usual use-case is to prevent extension profiles from showing up,
           that will be installed as part of the site creation anyways.
        """
        return [
            'plone.app.querystring:upgrade_to_3',
            'plone.app.querystring:upgrade_to_5',
            'plone.app.querystring:upgrade_to_6',
            'plone.app.querystring:upgrade_to_7',
            'plone.app.querystring:upgrade_to_8',
            'plone.app.querystring:upgrade_to_9',
            'plone.app.querystring:upgrade_to_10',
            'plone.app.querystring:upgrade_to_11',
        ]
