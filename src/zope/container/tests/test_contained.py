##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""Contained Tests
"""

import doctest
import gc
import unittest

from persistent import Persistent

import zope.interface
import zope.component

from zope.container.contained import ContainedProxy, NameChooser
from zope.container.sample import SampleContainer
from zope.container import testing
from zope.container.interfaces import NameReserved, IContainer, IReservedNames

class MyOb(Persistent):
    pass

def test_basic_proxy_attribute_management_and_picklability():
    """Contained-object proxy

    This is a picklable proxy that can be put around objects that
    don't implement IContained.

    >>> l = [1, 2, 3]
    >>> p = ContainedProxy(l)
    >>> p.__parent__ = 'Dad'
    >>> p.__name__ = 'p'
    >>> p
    [1, 2, 3]
    >>> p.__parent__
    'Dad'
    >>> p.__name__
    'p'

    >>> import pickle
    >>> p2 = pickle.loads(pickle.dumps(p))
    >>> p2
    [1, 2, 3]
    >>> p2.__parent__
    'Dad'
    >>> p2.__name__
    'p'
    """

def test_declarations_on_ContainedProxy():
    r"""

    It is possible to make declarations on ContainedProxy objects.

      >>> class I1(zope.interface.Interface):
      ...     pass
      >>> @zope.interface.implementer(I1)
      ... class C(object):
      ...     pass

      >>> c = C()
      >>> p = ContainedProxy(c)

    ContainedProxy provides no interfaces on it's own:

      >>> tuple(zope.interface.providedBy(ContainedProxy))
      ()

    It implements IContained and IPersistent:

      >>> tuple(zope.interface.implementedBy(ContainedProxy))
      (<InterfaceClass zope.location.interfaces.IContained>,
       <InterfaceClass persistent.interfaces.IPersistent>)

    A proxied object has IContainer, in addition to what the unproxied
    object has:

      >>> tuple(zope.interface.providedBy(p))
      (<InterfaceClass zope.container.tests.test_contained.I1>,
       <InterfaceClass zope.location.interfaces.IContained>,
       <InterfaceClass persistent.interfaces.IPersistent>)

      >>> class I2(zope.interface.Interface):
      ...     pass
      >>> zope.interface.directlyProvides(c, I2)
      >>> tuple(zope.interface.providedBy(p))
      (<InterfaceClass zope.container.tests.test_contained.I2>,
       <InterfaceClass zope.container.tests.test_contained.I1>,
       <InterfaceClass zope.location.interfaces.IContained>,
       <InterfaceClass persistent.interfaces.IPersistent>)

    We can declare interfaces through the proxy:

      >>> class I3(zope.interface.Interface):
      ...     pass
      >>> zope.interface.directlyProvides(p, I3)
      >>> tuple(zope.interface.providedBy(p))
      (<InterfaceClass zope.container.tests.test_contained.I3>,
       <InterfaceClass zope.container.tests.test_contained.I1>,
       <InterfaceClass zope.location.interfaces.IContained>,
       <InterfaceClass persistent.interfaces.IPersistent>)

    """


def test_ContainedProxy_instances_have_no_instance_dictionaries():
    """Make sure that proxies don't introduce extra instance dictionaries

    >>> from zope.container.contained import ContainedProxy
    >>> class C:
    ...     pass

    >>> c = C()
    >>> c.x = 1
    >>> c.__dict__
    {'x': 1}

    >>> p = ContainedProxy(c)
    >>> p.__dict__
    {'x': 1}
    >>> p.y = 3
    >>> sorted(p.__dict__.items())
    [('x', 1), ('y', 3)]
    >>> sorted(c.__dict__.items())
    [('x', 1), ('y', 3)]

    >>> p.__dict__ is c.__dict__
    True

    """


class TestNameChooser(unittest.TestCase):
    def test_checkName(self):
        container = SampleContainer()
        container['foo'] = 'bar'
        checkName = NameChooser(container).checkName

        # invalid type for the name
        self.assertRaises(TypeError, checkName, 2, object())
        self.assertRaises(TypeError, checkName, [], object())
        self.assertRaises(TypeError, checkName, None, object())
        self.assertRaises(TypeError, checkName, None, None)

        # invalid names
        self.assertRaises(ValueError, checkName, '+foo', object())
        self.assertRaises(ValueError, checkName, '@foo', object())
        self.assertRaises(ValueError, checkName, 'f/oo', object())
        self.assertRaises(ValueError, checkName, '', object())

        # existing names
        self.assertRaises(KeyError, checkName, 'foo', object())
        self.assertRaises(KeyError, checkName, u'foo', object())

        # correct names
        self.assertEqual(True, checkName('2', object()))
        self.assertEqual(True, checkName(u'2', object()))
        self.assertEqual(True, checkName('other', object()))
        self.assertEqual(True, checkName(u'reserved', object()))
        self.assertEqual(True, checkName(u'r\xe9served', object()))

        # reserved names
        @zope.component.adapter(IContainer)
        @zope.interface.implementer(IReservedNames)
        class ReservedNames(object):
            def __init__(self, context):
                self.reservedNames = set(('reserved', 'other'))
        zope.component.getSiteManager().registerAdapter(ReservedNames)

        self.assertRaises(NameReserved, checkName, 'reserved', object())
        self.assertRaises(NameReserved, checkName, 'other', object())
        self.assertRaises(NameReserved, checkName, u'reserved', object())
        self.assertRaises(NameReserved, checkName, u'other', object())

    def test_chooseName(self):
        container = SampleContainer()
        container['foo.old.rst'] = 'rst doc'
        nc = NameChooser(container)

        # correct name without changes
        self.assertEqual(nc.chooseName('foobar.rst', None),
                         u'foobar.rst')
        self.assertEqual(nc.chooseName(u'\xe9', None),
                         u'\xe9')

        # automatically modified named
        self.assertEqual(nc.chooseName('foo.old.rst', None),
                         u'foo.old-2.rst')
        self.assertEqual(nc.chooseName('+@+@foo.old.rst', None),
                         u'foo.old-2.rst')
        self.assertEqual(nc.chooseName('+@+@foo/foo+@', None),
                         u'foo-foo+@')

        # empty name
        self.assertEqual(nc.chooseName('', None), u'NoneType')
        self.assertEqual(nc.chooseName('@+@', []), u'list')

        # if the name is not a string it is converted
        self.assertEqual(nc.chooseName(None, None), u'None')
        self.assertEqual(nc.chooseName(2, None), u'2')
        self.assertEqual(nc.chooseName([], None), u'[]')
        container['None'] = 'something'
        self.assertEqual(nc.chooseName(None, None), u'None-2')
        container['None-2'] = 'something'
        self.assertEqual(nc.chooseName(None, None), u'None-3')

        # even if the given name cannot be converted to unicode
        class BadBoy:
            def __unicode__(self):
                raise Exception
            # Py3: Support
            __str__ = __unicode__

        self.assertEqual(nc.chooseName(BadBoy(), set()), u'set')


def test_suite():
    suite = unittest.TestSuite((
            unittest.makeSuite(TestNameChooser),
            ))
    suite.addTest(doctest.DocTestSuite(
            'zope.container.contained',
            setUp=testing.setUp, tearDown=testing.tearDown,
            checker=testing.checker))
    suite.addTest(doctest.DocTestSuite(
        optionflags=doctest.NORMALIZE_WHITESPACE,
        checker=testing.checker))
    return suite
