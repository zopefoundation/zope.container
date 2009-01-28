##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
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
"""Test the CheckDependency event subscriber.

$Id$
"""
import unittest

from zope.interface import implements
from zope.app.dependable.interfaces import IDependable, DependencyError
from zope.app.container.contained import ObjectRemovedEvent
from zope.app.container.dependency import CheckDependency
from zope.traversing.interfaces import IPhysicallyLocatable

class DummyObject(object):

    implements(IDependable, IPhysicallyLocatable)

    def dependents(self):
        return ['dependency1', 'dependency2']

    def getPath(self):
        return '/dummy-object'


class Test(unittest.TestCase):

    def testCheckDependency(self):
        obj = DummyObject()
        parent = object()
        event = ObjectRemovedEvent(obj, parent, 'oldName')
        self.assertRaises(DependencyError, CheckDependency, event)


def test_suite():
    return unittest.TestSuite((
            unittest.makeSuite(Test),
            ))

if __name__=='__main__':
    unittest.main()
