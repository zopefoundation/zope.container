In Subversion, this directory used to have these svn:externals that provided
the headers needed to compile _zope_container_contained.c:

persistent     -r 71248 svn://svn.zope.org/repos/main/ZODB/branches/3.7/src/persistent
zope.proxy              svn://svn.zope.org/repos/main/zope.proxy/trunk/src/zope/proxy

Sounds like in git the obvious fix is to add the necessary header files to the
repository.  Maybe some hackery in setup.py might urlretrieve the right files
from github, or something along these lines.

The header files came from the following svn revisions:

  proxy.h: r128784
  cPersistence.h: r71248

Note that this package also contains a *copy* of _zope_proxy_proxy.c that needs
to ge sync'ed with the zope.proxy version.
