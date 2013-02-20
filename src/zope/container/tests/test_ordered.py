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
"""Test the OrderedContainer.
"""
import unittest
from doctest import DocTestSuite

from zope.component.eventtesting import getEvents, clearEvents
from zope.container import testing


def test_order_events():
    """
    Prepare the setup::

      >>> from zope.container.sample import SampleContainer
      >>> root = SampleContainer()

    Prepare some objects::

        >>> from zope.container.ordered import OrderedContainer
        >>> oc = OrderedContainer()
        >>> oc['foo'] = 'bar'
        >>> oc['baz'] = 'quux'
        >>> oc['zork'] = 'grue'
        >>> oc.keys()
        ['foo', 'baz', 'zork']

    Now change the order::

        >>> clearEvents()
        >>> oc.updateOrder(['baz', 'foo', 'zork'])
        >>> oc.keys()
        ['baz', 'foo', 'zork']

    Check what events have been sent::

        >>> events = getEvents()
        >>> [event.__class__.__name__ for event in events]
        ['ContainerModifiedEvent']

    This is in fact a specialized modification event::

        >>> from zope.lifecycleevent.interfaces import IObjectModifiedEvent
        >>> IObjectModifiedEvent.providedBy(events[0])
        True

    """

def test_all_items_available_at_object_added_event():
    """
    Prepare the setup::

      >>> from zope.container.sample import SampleContainer
      >>> root = SampleContainer()

    Now register an event subscriber to object added events.

        >>> import zope.component
        >>> from zope.container import interfaces
        >>> from zope.lifecycleevent.interfaces import IObjectAddedEvent

        >>> @zope.component.adapter(IObjectAddedEvent)
        ... def printContainerKeys(event):
        ...     print(event.newParent.keys())

        >>> zope.component.provideHandler(printContainerKeys)

    Now we are adding an object to the container.

        >>> from zope.container.ordered import OrderedContainer
        >>> oc = OrderedContainer()
        >>> oc['foo'] = 'FOO'
        ['foo']

    """

def test_exception_causes_order_fix():
    """
    Prepare the setup::

      >>> from zope.container.sample import SampleContainer
      >>> root = SampleContainer()

    Now register an event subscriber to object added events that
    throws an error.

        >>> import zope.component
        >>> from zope.container import interfaces
        >>> from zope.lifecycleevent.interfaces import IObjectAddedEvent

        >>> @zope.component.adapter(IObjectAddedEvent)
        ... def raiseException(event):
        ...     raise Exception()

        >>> zope.component.provideHandler(raiseException)

    Now we are adding an object to the container.

        >>> from zope.container.ordered import OrderedContainer
        >>> oc = OrderedContainer()
        >>> oc['foo'] = 'FOO'
        Traceback (most recent call last):
        ...
        Exception

    The key 'foo' should not be around:

        >>> 'foo' in oc.keys()
        False

    """

def test_adding_none():
    """Test for OrderedContainer

    This is a regression test: adding None to an OrderedContainer
    used to corrupt its internal data structure (_order and _data
    wouldl get out of sync, causing KeyErrors when you tried to iterate).

        >>> from zope.container.ordered import OrderedContainer
        >>> oc = OrderedContainer()
        >>> oc['foo'] = None
        >>> oc.keys()
        ['foo']
        >>> oc.values()
        [None]
        >>> oc.items()
        [('foo', None)]
        >>> print(oc['foo'])
        None

    """

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(DocTestSuite("zope.container.ordered",
                               setUp=testing.setUp,
                               tearDown=testing.tearDown,
                               checker=testing.checker))
    suite.addTest(DocTestSuite(
            setUp=testing.ContainerPlacefulSetup().setUp,
            tearDown=testing.ContainerPlacefulSetup().tearDown,
            checker=testing.checker))
    return suite

if __name__ == '__main__':
    unittest.main()
