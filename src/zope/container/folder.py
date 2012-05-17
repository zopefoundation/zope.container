##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""The standard Zope Folder.
"""
__docformat__ = 'restructuredtext'

from BTrees.OOBTree import OOBTree
from persistent import Persistent
from zope.container.interfaces import IContainer, IContentContainer
from zope.container.contained import Contained, setitem, uncontained
from zope.interface import implementer

# XXX This container implementation is really only used by 
# zope.site.folder.Folder. Please do not use it. 

# XXX Check whether this IContainer implementation cannot really
# be replaced by the BTreeContainer.

@implementer(IContentContainer)
class Folder(Persistent, Contained):
    """The standard Zope Folder implementation."""


    def __init__(self):
        self.data = OOBTree()

    def keys(self):
        """Return a sequence-like object containing the names
           associated with the objects that appear in the folder
        """
        return self.data.keys()

    def __iter__(self):
        return iter(self.data.keys())

    def values(self):
        """Return a sequence-like object containing the objects that
           appear in the folder.
        """
        return self.data.values()

    def items(self):
        """Return a sequence-like object containing tuples of the form
           (name, object) for the objects that appear in the folder.
        """
        return self.data.items()

    def __getitem__(self, name):
        """Return the named object, or raise ``KeyError`` if the object
           is not found.
        """
        return self.data[name]

    def get(self, name, default=None):
        """Return the named object, or the value of the `default`
           argument if the object is not found.
        """
        return self.data.get(name, default)

    def __contains__(self, name):
        """Return true if the named object appears in the folder."""
        return self.data.has_key(name)

    def __len__(self):
        """Return the number of objects in the folder."""
        return len(self.data)

    def __setitem__(self, name, object):
        """Add the given object to the folder under the given name."""

        if not (isinstance(name, str) or isinstance(name, unicode)):
            raise TypeError("Name must be a string rather than a %s" %
                            name.__class__.__name__)
        try:
            unicode(name)
        except UnicodeError:
            raise TypeError("Non-unicode names must be 7-bit-ascii only")
        if not name:
            raise TypeError("Name must not be empty")

        if name in self.data:
            raise KeyError("name, %s, is already in use" % name)

        setitem(self, self.data.__setitem__, name, object)

    def __delitem__(self, name):
        """Delete the named object from the folder. Raises a KeyError
           if the object is not found."""
        uncontained(self.data[name], self, name)
        del self.data[name]

