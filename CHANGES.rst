Changes
=======

4.0.0 (2014-03-19)
------------------

- Added support for Python 3.4.

- Added support for PyPy.


4.0.0a3 (2013-02-28)
--------------------

- Restore ``Folder`` pickle forward/backward compatibility with
  version 3.12.0 after making it inherit from ``BTreeContainer.``


4.0.0a2 (2013-02-21)
--------------------

- Allow testing without checkouts of unreleased zope.publisher and ZODB.

- Added Python 3 Trove classifiers.


4.0.0a1 (2013-02-20)
--------------------

- Added support for Python 3.3.

- Made ``Folder`` class inherit from ``BTreeContainer`` class, so that the
  IContainer interface does not need to be re-implemented. Added a ``data``
  attribute for BBB.

- Replaced deprecated ``zope.component.adapts`` usage with equivalent
  ``zope.component.adapter`` decorator.

- Replaced deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Dropped support for Python 2.4 and 2.5.

- Send ``IContainerModifiedEvent`` *after* the container is modified
  (LP#705600).

- Preserve the original exception traceback in
  OrderedContainer.__setitem__.

- Handle Broken Objects more gracefully

- Fix a bug that made it impossible to store None values in containers
  (LP#1070719).


3.12.0 (2010-12-14)
-------------------

- Fix detection of moving folders into itself or a subfolder of itself.
  (#118088)

- Fixed ZCML-related tests and dependencies.

- Added ``zcml`` extra dependencies.

3.11.1 (2010-04-30)
-------------------

- Prefer the standard libraries doctest module to the one from zope.testing.

- Added compatibility with ZODB3 3.10 by importing the IBroken interface from
  it directly. Once we can rely on the new ZODB3 version exclusively, we can
  remove the dependency onto the zope.broken distribution.

- Never fail if the suggested name is in a wrong type (#227617)

- ``checkName`` first checks the parameter type before the emptiness.

3.11.0 (2009-12-31)
-------------------

- Copy two trivial classes from zope.cachedescriptors into this package, which
  allows us to remove that dependency. We didn't actually use any caching
  properties as the dependency suggested.

3.10.1 (2009-12-29)
-------------------

- Moved zope.copypastemove related tests into that package.

- Removed no longer used zcml prefix from the configure file.

- Stop importing DocTestSuite from zope.testing.doctestunit. Fixes
  compatibility problems with zope.testing 3.8.4.

3.10.0 (2009-12-15)
-------------------

- Break testing dependency on zope.app.testing.

- Break testing dependency on zope.app.dependable by moving the code and tests
  into that package.

- Import ISite from zope.component after it was moved there from
  zope.location.

3.9.1 (2009-10-18)
------------------

- Rerelease 3.9.0 as it had a broken Windows 2.6 egg.

- Marked as part of the ZTK.

3.9.0 (2009-08-28)
------------------

- Previous releases should be versioned 3.9.0 as they are not pure bugfix
  releases and worth a "feature" release, increasing feature version.

  Packages that depend on any changes introduced in version 3.8.2 or 3.8.3
  should depend on version 3.9 or greater.

3.8.3 (2009-08-27)
------------------

- Move IXMLRPCPublisher ZCML registrations for containers from
  zope.app.publisher.xmlrpc to zope.container for now.

3.8.2 (2009-05-17)
------------------

- Rid ourselves of ``IContained`` interface.  This interface was moved
  to ``zope.location.interfaces``.  A b/w compat import still exists
  to keep old code running.  Depend on ``zope.location``>=3.5.4.

- Rid ourselves of the implementations of ``IObjectMovedEvent``,
  ``IObjectAddedEvent``, ``IObjectRemovedEvent`` interfaces and
  ``ObjectMovedEvent``, ``ObjectAddedEvent`` and
  ``ObjectRemovedEvent`` classes.  B/w compat imports still exist.
  All of these were moved to ``zope.lifecycleevent``. Depend on
  ``zope.lifecycleevent``>=3.5.2.

- Fix a bug in OrderedContainer where trying to set the value for a
  key that already exists (duplication error) would actually delete the
  key from the order, leaving a dangling reference.

- Partially break dependency on ``zope.traversing`` by disusing
  zope.traversing.api.getPath in favor of using
  ILocationInfo(object).getPath().  The rest of the runtime
  dependencies on zope.traversing are currently interface
  dependencies.

- Break runtime dependency on ``zope.app.dependable`` by using a zcml
  condition on the qsubscriber ZCML directive that registers the
  CheckDependency handler for IObjectRemovedEvent.  If
  ``zope.app.dependable`` is not installed, this subscriber will never
  be registered.  ``zope.app.dependable`` is now a testing dependency
  only.

3.8.1 (2009-04-03)
------------------

- Fixed misspackaged 3.8.0


3.8.0 (2009-04-03)
------------------

- Change configure.zcml to not depend on zope.app.component.
  Fixes: https://bugs.launchpad.net/bugs/348329

- Moved the declaration of ``IOrderedContainer.updateOrder``  to a new, basic
  ``IOrdered`` interface and let ``IOrderedContainer`` inherit it. This allows
  easier reuse of the declaration.

3.7.2 (2009-03-12)
------------------

- Fix: added missing ComponentLookupError, missing since revision 95429 and
  missing in last release.

- Adapt to the move of IDefaultViewName from zope.component.interfaces
  to zope.publisher.interfaces.

- Add support for reserved names for containers. To specify reserved
  names for some container, you need to provide an adapter from the
  container to the ``zope.container.interfaces.IReservedNames`` interface.
  The default NameChooser is now also aware of reserved names.

3.7.1 (2009-02-05)
------------------

- Raise more "Pythonic" errors from ``__setitem__``, losing the dependency
  on ``zope.exceptions``:

  o ``zope.exceptions.DuplicationError`` -> ``KeyError``

  o ``zope.exceptions.UserError`` -> ``ValueError``

- Moved import of ``IBroken`` interface to use new ``zope.broken``
  package, which has no dependencies beyond ``zope.interface``.

- Made ``test`` part pull in the extra test requirements of this package.

- Split the ``z3c.recipe.compattest`` configuration out into a new file,
  ``compat.cfg``, to reduce the burden of doing standard unit tests.

- Stripped out bogus develop eggs from ``buildout.cfg``.

3.7.0 (2009-01-31)
------------------

- Split this package off ``zope.app.container``. This package is
  intended to have far less dependencies than ``zope.app.container``.

- This package also contains the container implementation that
  used to be in ``zope.app.folder``.