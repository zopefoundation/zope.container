This package define interfaces of container components, and provides
sample container implementations such as a BTreeContainer and
OrderedContainer.

Changes
=======

3.5.0a1 (2007-06-29)
--------------------

* Updated bootstrap script to current version.

* Store length of BTreeContainer in its own Length object for faster
  __len__ implementation of huge containers.

3.4.0a1 (2007-04-22)
--------------------

Initial release as a separate project, corresponds to
zope.app.container from Zope 3.4.0a1
