Overview
========

This package provides a queryparser, querybuilder and extra helper tools,
to parse stored queries to actual results, used in new style collections.
It includes a registry reader which reads operators, values and criteria
from the Plone registry.


Filtering by the current item
-----------------------------

The ``plone.app.querystring.operation.string.currentUID`` operation
("Current item") compares an index with the UID of the item where the query
runs, for example the page that holds a listing block. It needs no value from
the editor.

No field uses this operation by default. It is meant for indexes that store
the UIDs of related items: a collection or listing placed on an item can then
show every item that points to it, such as "posts by this author". An add-on
enables it on the field for its own index in its ``registry.xml``::

    <records interface="plone.app.querystring.interfaces.IQueryField"
             prefix="plone.app.querystring.field.authors">
      <value key="title">Authors</value>
      <value key="enabled">True</value>
      <value key="sortable">False</value>
      <value key="operations">
        <element>plone.app.querystring.operation.string.currentUID</element>
      </value>
      <value key="group">Metadata</value>
    </records>


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
