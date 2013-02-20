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
from zope.interface import implementer
from zope.container import btree, interfaces

@implementer(interfaces.IContentContainer)
class Folder(btree.BTreeContainer):
    """The standard Zope Folder implementation."""

    # BBB: The data attribute used to be exposed. This should make it also
    # compatible with old pickles.
    @property
    def data(self):
        return self._SampleContainer__data

    @data.setter
    def data(self, value):
        self._SampleContainer__data = value
