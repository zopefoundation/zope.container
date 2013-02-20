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
"""Container constraint tests
"""
from __future__ import print_function
import doctest
import unittest
from zope.testing import module
from zope.container import testing

def setUp(test):
    test.globs['print_function'] = print_function
    module.setUp(test, 'zope.container.constraints_txt')

def tearDown(test):
    module.tearDown(test, 'zope.container.constraints_txt')

def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite(
                'zope.container.constraints', checker=testing.checker),
        doctest.DocFileSuite(
                '../constraints.txt',
                setUp=setUp, tearDown=tearDown, checker=testing.checker),
        ))

if __name__ == '__main__': unittest.main()
