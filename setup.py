# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '1.5.0'

long_description = open("README.rst").read() + "\n"
long_description += open("CHANGES.rst").read()

setup(
    name='plone.app.querystring',
    version=version,
    description=(
        "A queryparser, querybuilder and extra helper tools, to "
        "parse stored queries to actual results, used in "
        "new style Plone collections"),
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords='collection queries',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://github.com/plone/plone.app.querystring',
    license='GPL version 2',
    packages=find_packages(),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'DateTime',
        'Products.CMFCore',
        'Products.CMFPlone',
        'plone.app.contentlisting',
        'plone.app.layout',
        'plone.app.registry>=1.1',
        'plone.batching',
        'plone.registry',
        'python-dateutil',
        'setuptools',
        'six',
        'zope.component',
        'zope.dottedname',
        'zope.globalrequest',
        'zope.i18n',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.publisher',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
