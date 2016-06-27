Changelog
=========

1.2.10 (2016-06-27)
-------------------

Fixes:

- Hide profiles associated with upgrade steps.
  [hvelarde]


1.2.9 (2015-10-30)
------------------

Fixes:

- Fixed flake8 warnings.
  [maurits]

- Updated compatibility information in README.
  [maurits]


1.2.8 (2015-09-24)
------------------

- Fixed Sortable Indexes to not return ZCTextIndex type indexes.
  [winstonf88]


1.2.7 (2015-08-13)
------------------

- Fixed possible problem with ``custom_query`` parameter where
  theoretically a second invocation could inadvertently be using the
  value from the first invocation.
  [maurits]


1.2.6 (2015-05-31)
------------------

- Fix path-queries using UID (backported from master).
  [pbauer]


1.2.5 (2015-04-28)
------------------

- 1.2.4 was a brown-bag release.
  [timo]


1.2.4 (2015-04-28)
------------------

- Implement ``is``, ``lessThan`` and ``largerThan`` operators for integer fields (fixes `#32`_).
  [rodfersou]


1.2.3 (2014-10-20)
------------------

- Fixed build DateIndex query.
  [kroman0]


1.2.2 (2014-08-05)
------------------

- Fix wrong query field vocabulary declaration of the show_inactive field from
  ``AllRoles`` to ``Roles``.
  [thet]

- Add a ``custom_query`` parameter to the ``QueryBuilder._makequery`` method,
  which allows for run time customization of the stored query, e.g. by request
  parameters.
  [thet]

- Added support for depth in relativePath operator.
  [djay]


1.2.1 (2014-05-14)
------------------

- Fixed upgrade_1_to_2 upgrade step in case the registry doesn't contain the
  named value
  [ichim-david]

- Added show inactive operation which uses the roles vocabulary in order
  to assign permission to show or hide the inactive objects of the given query
  [ichim-david]

- Migrate tests to plone.app.testing.
  [sdelcourt]

- Fix querybuilder code if results object does not provide an
  actual_results_count attribute. This regression has been introduced in
  release 1.1.1 (fixed broken handling of limit and batch size).
  [timo]


1.2.0 (2014-04-05)
------------------

- bugfix for #22: Names not matching for operations getObjPositionInParent
  plus test
  [jensens]

- Implement multipath queries:
  - Parsing a path returns always a list.
  - Special handling for paths in parseFormquery.
  [maethu]

- Fixes https://dev.plone.org/ticket/13251
  [mathias.leimgruber]

- querybuilder results can now be manipulated using
  ``IParsedQueryIndexModifier`` named utilities.
  [keul]


1.1.1 (2014-01-27)
------------------

- fixed broken handling of limit and batch size.
  [bosim]

- pep8 fixes
  [bosim]


1.1.0 (2013-11-14)
------------------

- be able to include a depth value onto path query string
  [vangheem]

- Use plone.batching.
  [khink]

1.0.8 (2013-03-14)
------------------

- Fix UnicodeDecodeError on utf8-encoded Subject strings.
  [tisto]


1.0.7 (2013-01-01)
------------------

- getVocabularyValues now checks if the vocabulary utility is missing,
  if it is the utility is just ignored. This makes the module tollarant to
  missing vocabulary utilities.
  [bosim]


1.0.6 (2012-10-03)
------------------

- _relativePath handler can now walk through the site structure (not only upwards)
  _path handler respects absolute paths without leading nav_root path
  [petschki]


1.0.5 (2012-06-29)
------------------

- Date ranges now use the _betweenDates handler, which is much more forgiving
  of empty field values, defaulting to an all-encompassing date range if neither
  value is provided, an "everything after" range if only the start date is
  provided, and a min/max range if both are provided.

  Fixes http://dev.plone.org/ticket/12965
  [esteele]


1.0.4 (2012-05-07)
------------------

- Fixed i18n of "Before today" operator and
  "x items matching your search terms.".
  [vincentfretin]


1.0.3 (2012-04-15)
------------------

* Add an optional 'brains' parameter to the query builder to obtain
  results not wrapped as an IContentListing.
  [davisagli]

* Declare all dependencies in setup.py to resolve a dependeny problem in
  test setups, where the Plone stack isn't fully loaded.
  [thet]

* Add a "today" date operator
  [esteele]

* Internationalize strings in the registry.
  [davisagli]

* Change relative date searching to be "N days" string based rather than
  datetime based.
  [esteele]

* Handle empty values on relative date fields.
  [esteele]

1.0.2 (2012-02-10)
------------------

* Change the Creator field to use the correct query operation for filtering
  on the current logged in user.
  This fixes https://dev.plone.org/ticket/12052
  [jcerjak]

* Limit number of items that show up in the preview of the edit view to 25.
  If we do not limit these results all items in the query will be rendered in
  the preview which leads to problems when the collection contains > 10k
  results.
  [timo]


1.0.1 (2011-10-17)
------------------

* Ensure inactive content is only shown to users with the appropriate
  permission.


1.0 (2011-07-19)
----------------

* Initial release

.. _`#32`: https://github.com/plone/plone.app.querystring/issues/32
