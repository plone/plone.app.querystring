Changelog
=========

1.4 (2016-08-18)
----------------

New features:

- Refactor addition of criteria to stick inside ``INavigationRoot`` in querybuilder.
  Added a simple ``IQueryModifier`` interfaces expecting a query and returning a query.
  Iterates over all sorted utilities providing such an interfaces and calls it right before the query is parsed.
  Code to add the ``INavigationRoot`` stickyness was moved to such a query modifier.
  [jensens]

Bug fixes:

- Use zope.interface decorator.
  [gforcada]


1.3.15 (2016-05-25)
-------------------

Fixes:

- Add missing _referenceIs query parser
  [vangheem]


1.3.14 (2016-02-19)
-------------------

Fixes:

- Set path to navigation root by default to have the same results
  in Collection preview and view.
  [Gagaro]


1.3.13 (2016-02-14)
-------------------

New:

- Be able to parse more date string types
  [vangheem]


1.3.12 (2015-11-26)
-------------------

Fixes:

- Again upgrade collections with ``selection.is`` to
  ``selection.any``, because the standard events and news collections
  may have been wrongly created in a new site.
  Issue https://github.com/plone/Products.CMFPlone/issues/1040
  [maurits]

- In tests, use ``selection.any`` in querystrings.
  Issue https://github.com/plone/Products.CMFPlone/issues/1040
  [maurits]

- Added upgrade step to replace ``selection.is`` with
  ``selection.any`` operations in querystrings also for objects using
  the Collection behavior.
  [thet]


1.3.11 (2015-10-30)
-------------------

Fixes:

- Rerelease as something went wrong during upload of the package.
  [maurits]


1.3.10 (2015-10-30)
-------------------

Fixes:

- Added missing ',' for subject upgrade.
  [ezvirtual]


1.3.9 (2015-10-30)
------------------

Fixes:

- Fixed flake8 warnings.
  [maurits]

- Updated compatibility information in README.
  [maurits]

- Fixed resultview icons.
  https://github.com/plone/Products.CMFPlone/issues/1151
  [fgrcon]

- Added upgrade step to fix Subject index for existing collections.
  [ezvirtual]


1.3.8 (2015-09-21)
------------------

- Fixed problems introduced by merge.
  [jensens]

- Add "before/after N days" functionality
  [petschki]

- Fixed Sortable Indexes to not return ZCTextIndex type indexes.
  [winstonf88]


1.3.7 (2015-09-11)
------------------

- Fix vocabularies sorting
  [ebrehault]


1.3.6 (2015-08-24)
------------------

- Fix migration from Plone 4 to Plone 5.
  [pbauer]


1.3.5 (2015-08-22)
------------------

- Creator criteria: pur currentUser on top.
  [mvanrees]

- Migrate Creator string.is to selection.any.
  [mvanrees]

- add user vocabulary to plone.app.querystring.field.Creator.
  [vangheem]

- do not need "is" when there is an "any" operator.
  [vangheem]


1.3.4 (2015-08-21)
------------------

- Hide upgrade-profiles when creating a new site.
  [pbauer]

- Replace selection.is with selection.any for portal_types and review_state
  operations, and add selection.any for Creator operation.
  [frapell]

- Actually convert the value to a datetime for the DateIndex query modifier.
  [frapell]

- Do not fail if the 'Between' operation is called with an empty value, and
  instead return a list with 2 empty values.
  [frapell]

- Fixed possible problem with ``custom_query`` parameter where
  theoretically a second invocation could inadvertently be using the
  value from the first invocation.
  [maurits]


1.3.3 (2015-07-18)
------------------

- Fix getObjPositionInParent be sortable by default
  [datakurre]

- Add operators selection.any and selection.all to Subject.
  [MrTango]


1.3.2 (2015-05-04)
------------------

- Implement ``is``, ``lessThan`` and ``largerThan`` operators for integer fields (fixes `#32`_).
  [rodfersou]


1.3.1 (2015-03-12)
------------------

- No need to install plone.app.querystring as z2 products in tests.
  [timo]

- Fix path-queries using UID.
  [pbauer]


1.3 (2015-01-22)
----------------

- Path criteria can be defined either absolute to ``IPloneSiteRoot``, absolute
  to ``INavigationRoot`` or relative to current context.
  [rnixx]

- Relative path parent breaks on ``IPloneSiteRoot`` rather than
  ``INavigationRoot``.
  [rnixx]


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
