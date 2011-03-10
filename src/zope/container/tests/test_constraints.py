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

import doctest
import unittest
from zope.testing import module

def setUp(test):
    module.setUp(test, 'zope.container.constraints_txt')

def tearDown(test):
    module.tearDown(test, 'zope.container.constraints_txt')

def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite('zope.container.constraints'),
        doctest.DocFileSuite('../constraints.txt',
                             setUp=setUp, tearDown=tearDown),
        ))

if __name__ == '__main__': unittest.main()
