Overview
========

This package provides a queryparser, querybuilder and extra helper tools,
to parse stored queries to actual results, used in new style collections.
It includes a registry reader which reads operators, values and criteria
from the Plone registry.


Compatibility with Plone versions
---------------------------------

For each Plone release, its versions.cfg file at
http://dist.plone.org/release/ pins a version of plone.app.querystring
that works well with that Plone version.  It is wise not to pick
another version.

But for clarity, these are the correct relationships between the two
versions:

- On Plone 4.2 use 1.0.x.

- On Plone 4.3 use 1.2.x.

- On Plone 5.0 use 1.3.x.

Too new versions can cause problems.  For example, the 1.1.x and 1.2.x
series are intended for usage with Plone 4.3.  They depend on
plone.batching, which ships with Plone 4.3 but may cause problems_
with Plone 4.2.

.. _problems: https://dev.plone.org/ticket/12875
