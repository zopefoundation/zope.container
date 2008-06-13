##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""This module provides a sample container implementation.

This is primarily for testing purposes.

It might be useful as a mix-in for some classes, but many classes will
need a very different implementation.

$Id$
"""
__docformat__ = 'restructuredtext'

from persistent import Persistent
from BTrees.OOBTree import OOBTree
from BTrees.Length import Length

from zope.app.container.interfaces import IBTreeContainer
from zope.app.container.contained import Contained, setitem, uncontained
from zope.cachedescriptors.property import Lazy
from zope.interface import implements


class BTreeContainer(Contained, Persistent):

    implements(IBTreeContainer)

    def __init__(self):
        self.__data = self._newContainerData()
        self.__len = Length()

    def _newContainerData(self):
        """Construct an item-data container

        Subclasses should override this if they want different data.

        The value returned is a mapping object that also has get,
        has_key, keys, items, and values methods.
        The default implementation uses an OOBTree.
        """
        return OOBTree()

    def __contains__(self, key):
        '''See interface IReadContainer

        >>> c = BTreeContainer()
        >>> "a" in c
        False
        >>> c["a"] = 1
        >>> "a" in c
        True
        >>> "A" in c
        False
        '''
        return key in self.__data

    @Lazy
    def _BTreeContainer__len(self):
        l = Length()
        ol = len(self.__data)
        if ol > 0:
            l.change(ol)
        self._p_changed = True
        return l

    def __len__(self):
        return self.__len()

    def _setitemf(self, key, value):
        # make sure our lazy property gets set
        l = self.__len
        self.__data[key] = value
        l.change(1)

    def __iter__(self):
        return iter(self.__data)

    def __getitem__(self, key):
        '''See interface `IReadContainer`'''
        return self.__data[key]

    def get(self, key, default=None):
        '''See interface `IReadContainer`'''
        return self.__data.get(key, default)
        
    def __setitem__(self, key, value):
        setitem(self, self._setitemf, key, value)

    def __delitem__(self, key):
        # make sure our lazy property gets set
        l = self.__len
        uncontained(self.__data[key], self, key)
        del self.__data[key]
        l.change(-1)

    has_key = __contains__

    def items(self, key=None):
        return self.__data.items(key)

    def keys(self, key=None):
        return self.__data.keys(key)

    def values(self, key=None):
        return self.__data.values(key)

    # transparent backward compatibility
    # since BTreeContainer does not inherit from SampleContainer
    def _get__data(self):
        try:
            return self._BTreeContainer__data
        except:
            return self._SampleContainer__data
    def _set__data(self, value):
        try:
            self._BTreeContainer__data = value
        except:
            self._SampleContainer__data = value
    def _del_data(self):
        try:
            del self._BTreeContainer__data
        except:
            del self._SampleContainer__data
    __data = property(_get__data, _set__data, _del_data)



