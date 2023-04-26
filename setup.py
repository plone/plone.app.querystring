from setuptools import find_packages
from setuptools import setup


version = "2.0.3"

long_description = open("README.rst").read() + "\n"
long_description += open("CHANGES.rst").read()

setup(
    name="plone.app.querystring",
    version=version,
    description=(
        "A queryparser, querybuilder and extra helper tools, to "
        "parse stored queries to actual results, used in "
        "new style Plone collections"
    ),
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="collection queries",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://github.com/plone/plone.app.querystring",
    license="GPL version 2",
    packages=find_packages(),
    namespace_packages=["plone", "plone.app"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "plone.app.contentlisting",
        "plone.app.registry>=1.1",
        "plone.base",
        "plone.batching",
        "plone.i18n",
        "plone.registry",
        "plone.uuid",
        "Products.GenericSetup",
        "Products.ZCatalog",
        "python-dateutil",
        "Zope",
        "zope.dottedname",
        "zope.globalrequest",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.app.contenttypes[test]",
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
