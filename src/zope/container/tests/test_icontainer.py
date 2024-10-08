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
"""Test the IContainer interface.
"""
from unittest import TestCase

from zope.interface.verify import verifyObject

from zope.container import testing
from zope.container.interfaces import IContainer


def DefaultTestData():
    return [('3', '0'), ('2', '1'), ('4', '2'), ('6', '3'), ('0', '4'),
            ('5', '5'), ('1', '6'), ('8', '7'), ('7', '8'), ('9', '9')]


class BaseTestIContainer(testing.ContainerPlacelessSetup):
    """Base test cases for containers.

    Subclasses must define a makeTestObject that takes no
    arguments and that returns a new empty test container,
    and a makeTestData that also takes no arguments and returns
    a sequence of (key, value) pairs that may be stored in
    the test container.  The list must be at least ten items long.
    'NoSuchKey' may not be used as a key value in the returned list.
    """
    __container = None
    __data = None

    def __setUp(self):
        self.__container = container = self.makeTestObject()
        self.__data = data = self.makeTestData()
        for k, v in data:
            container[k] = v
        return container, data

    ############################################################
    # Interface-driven tests:

    def testIContainerVerify(self):
        verifyObject(IContainer, self.makeTestObject())

    def test_keys(self):
        # See interface IReadContainer
        container = self.makeTestObject()
        keys = container.keys()
        self.assertEqual(list(keys), [])

        container, data = self.__setUp()
        keys = container.keys()
        keys = sorted(keys)  # convert to sorted list
        ikeys = sorted([k for k, _v in data])  # sort input keys
        self.assertEqual(keys, ikeys)

    def test_get(self):
        # See interface IReadContainer
        default = object()
        data = self.makeTestData()
        container = self.makeTestObject()
        self.assertRaises(KeyError, container.__getitem__, data[0][0])
        self.assertEqual(container.get(data[0][0], default), default)

        container, data = self.__setUp()
        self.assertRaises(KeyError, container.__getitem__,
                          self.getUnknownKey())
        self.assertEqual(container.get(self.getUnknownKey(), default), default)
        for i in (1, 8, 7, 3, 4):
            self.assertEqual(container.get(data[i][0], default), data[i][1])
            self.assertEqual(container.get(data[i][0]), data[i][1])

    def test_values(self):
        # See interface IReadContainer
        container = self.makeTestObject()
        values = container.values()
        self.assertEqual(list(values), [])

        container, data = self.__setUp()
        values = list(container.values())
        for _k, v in data:
            values.remove(v)

        self.assertEqual(values, [])

    def test_len(self):
        # See interface IReadContainer
        container = self.makeTestObject()
        self.assertEqual(len(container), 0)

        container, data = self.__setUp()
        self.assertEqual(len(container), len(data))

    def test_iter(self):
        container = self.makeTestObject()
        self.assertEqual(list(container), [])

        container, data = self.__setUp()
        self.assertEqual(len(list(container)), len(data))

    def test_items(self):
        # See interface IReadContainer
        container = self.makeTestObject()
        items = container.items()
        self.assertEqual(list(items), [])

        container, data = self.__setUp()
        items = container.items()
        items = sorted(items)  # convert to sorted list
        data.sort()  # sort input data
        self.assertEqual(items, data)

    def test___contains__(self):
        # See interface IReadContainer
        container = self.makeTestObject()
        data = self.makeTestData()
        self.assertNotIn(data[6][0], container)

        container, data = self.__setUp()
        self.assertIn(data[6][0], container)
        for i in (1, 8, 7, 3, 4):
            self.assertIn(data[i][0], container)

    def test_delObject(self):
        # See interface IWriteContainer
        default = object()
        data = self.makeTestData()
        container = self.makeTestObject()
        self.assertRaises(KeyError, container.__delitem__, data[0][0])

        container, data = self.__setUp()
        self.assertRaises(KeyError, container.__delitem__,
                          self.getUnknownKey())
        for i in (1, 8, 7, 3, 4):
            del container[data[i][0]]
        for i in (1, 8, 7, 3, 4):
            self.assertRaises(KeyError, container.__getitem__, data[i][0])
            self.assertEqual(container.get(data[i][0], default), default)
        for i in (0, 2, 9, 6, 5):
            self.assertEqual(container[data[i][0]], data[i][1])

    def test_bytes_keys_converted_to_unicode(self):
        # https://github.com/zopefoundation/zope.container/issues/17
        container = self.makeTestObject()
        container[b'abc'] = 1
        self.assertIn('abc', container)
        del container['abc']
        self.assertNotIn('abc', container)

    def test_exception_in_subscriber_leaves_item_in_place(self):
        # Now register an event subscriber to object added events that
        # throws an error.
        # https://github.com/zopefoundation/zope.container/issues/18

        import zope.component
        from zope.lifecycleevent.interfaces import IObjectAddedEvent

        class MyException(Exception):
            pass

        @zope.component.adapter(IObjectAddedEvent)
        def raiseException(event):
            raise MyException()

        zope.component.provideHandler(raiseException)

        # Now we are adding an object to the container.

        container = self.makeTestObject()
        with self.assertRaises(MyException):
            container['foo'] = 'FOO'

        # The key 'foo' should still be present
        self.assertIn('foo', container.keys())
        self.assertEqual(list(iter(container)), ['foo'])
        self.assertIn('foo', container)

    ############################################################
    # Tests from Folder

    def testEmpty(self):
        folder = self.makeTestObject()
        data = self.makeTestData()
        self.assertFalse(folder.keys())
        self.assertFalse(folder.values())
        self.assertFalse(folder.items())
        self.assertFalse(len(folder))
        self.assertNotIn(data[6][0], folder)

        self.assertEqual(folder.get(data[6][0], None), None)
        self.assertRaises(KeyError, folder.__getitem__, data[6][0])

        self.assertRaises(KeyError, folder.__delitem__, data[6][0])

    def testBadKeyTypes(self):
        folder = self.makeTestObject()
        data = self.makeTestData()
        value = data[1][1]
        for name in self.getBadKeyTypes():
            self.assertRaises(TypeError, folder.__setitem__, name, value)

    def testOneItem(self):
        folder = self.makeTestObject()
        data = self.makeTestData()

        foo = data[0][1]
        name = data[0][0]
        folder[name] = foo

        self.assertEqual(len(folder.keys()), 1)
        self.assertEqual(list(folder.keys())[0], name)
        self.assertEqual(len(folder.values()), 1)
        self.assertEqual(list(folder.values())[0], foo)
        self.assertEqual(len(folder.items()), 1)
        self.assertEqual(list(folder.items())[0], (name, foo))
        self.assertEqual(len(folder), 1)

        self.assertIn(name, folder)
        # Use an arbitrary id frpm the data set; don;t just use any id, since
        # there might be restrictions on their form
        self.assertNotIn(data[6][0], folder)

        self.assertEqual(folder.get(name, None), foo)
        self.assertEqual(folder[name], foo)

        self.assertRaises(KeyError, folder.__getitem__, data[6][0])

        foo2 = data[1][1]

        name2 = data[1][0]
        folder[name2] = foo2

        self.assertEqual(len(folder.keys()), 2)
        self.assertIn(name2, folder.keys())
        self.assertEqual(len(folder.values()), 2)
        self.assertIn(foo2, folder.values())
        self.assertEqual(len(folder.items()), 2)
        self.assertIn((name2, foo2), folder.items())
        self.assertEqual(len(folder), 2)

        del folder[name]
        del folder[name2]

        self.assertFalse(folder.keys())
        self.assertFalse(folder.values())
        self.assertFalse(folder.items())
        self.assertFalse(len(folder))
        self.assertNotIn(name, folder)

        self.assertRaises(KeyError, folder.__getitem__, name)
        self.assertEqual(folder.get(name, None), None)
        self.assertRaises(KeyError, folder.__delitem__, name)

    def testManyItems(self):
        folder = self.makeTestObject()
        data = self.makeTestData()
        objects = [data[i][1] for i in range(4)]
        name0 = data[0][0]
        name1 = data[1][0]
        name2 = data[2][0]
        name3 = data[3][0]
        folder[name0] = objects[0]
        folder[name1] = objects[1]
        folder[name2] = objects[2]
        folder[name3] = objects[3]

        self.assertEqual(len(folder.keys()), len(objects))
        self.assertIn(name0, folder.keys())
        self.assertIn(name1, folder.keys())
        self.assertIn(name2, folder.keys())
        self.assertIn(name3, folder.keys())

        self.assertEqual(len(folder.values()), len(objects))
        self.assertIn(objects[0], folder.values())
        self.assertIn(objects[1], folder.values())
        self.assertIn(objects[2], folder.values())
        self.assertIn(objects[3], folder.values())

        self.assertEqual(len(folder.items()), len(objects))
        self.assertIn((name0, objects[0]), folder.items())
        self.assertIn((name1, objects[1]), folder.items())
        self.assertIn((name2, objects[2]), folder.items())
        self.assertIn((name3, objects[3]), folder.items())

        self.assertEqual(len(folder), len(objects))

        self.assertIn(name0, folder)
        self.assertIn(name1, folder)
        self.assertIn(name2, folder)
        self.assertIn(name3, folder)
        self.assertNotIn(data[5][0], folder)

        self.assertEqual(folder.get(name0, None), objects[0])
        self.assertEqual(folder[name0], objects[0])
        self.assertEqual(folder.get(name1, None), objects[1])
        self.assertEqual(folder[name1], objects[1])
        self.assertEqual(folder.get(name2, None), objects[2])
        self.assertEqual(folder[name2], objects[2])
        self.assertEqual(folder.get(name3, None), objects[3])
        self.assertEqual(folder[name3], objects[3])

        self.assertEqual(folder.get(data[5][0], None), None)
        self.assertRaises(KeyError, folder.__getitem__, data[5][0])

        del folder[name0]
        self.assertEqual(len(folder), len(objects) - 1)
        self.assertNotIn(name0, folder)
        self.assertNotIn(name0, folder.keys())

        self.assertNotIn(objects[0], folder.values())
        self.assertNotIn((name0, objects[0]), folder.items())

        self.assertEqual(folder.get(name0, None), None)
        self.assertRaises(KeyError, folder.__getitem__, name0)

        self.assertRaises(KeyError, folder.__delitem__, name0)

        del folder[name1]
        del folder[name2]
        del folder[name3]

        self.assertFalse(folder.keys())
        self.assertFalse(folder.values())
        self.assertFalse(folder.items())
        self.assertFalse(len(folder))
        self.assertNotIn(name0, folder)
        self.assertNotIn(name1, folder)
        self.assertNotIn(name2, folder)
        self.assertNotIn(name3, folder)


class TestSampleContainer(BaseTestIContainer, TestCase):

    def makeTestObject(self):
        from zope.container.sample import SampleContainer
        return SampleContainer()

    def makeTestData(self):
        return DefaultTestData()

    def getUnknownKey(self):
        return '10'

    def getBadKeyTypes(self):
        return [None, [b'foo'], 1, b'\xf3abc']
