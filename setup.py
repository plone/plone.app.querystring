from setuptools import setup, find_packages

version = '1.2.11'

long_description = open("README.rst").read() + "\n"
long_description += open("CHANGES.rst").read()

setup(
    name='plone.app.querystring',
    version=version,
    description="Tools for building collection queries",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='querybuilder queryparser collection',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='http://pypi.python.org/pypi/plone.app.querystring',
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'DateTime',
        'Products.CMFCore',
        'Products.CMFPlone',
        'plone.app.contentlisting',
        'plone.app.layout',
        'plone.app.registry>=1.1dev',
        'plone.app.upgrade',
        'plone.app.vocabularies',
        'plone.batching',
        'plone.registry',
        'setuptools',
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
