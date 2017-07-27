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
"""FS-based directory implementation tests for containers
"""

import doctest
import unittest

from zope.container import testing
import zope.container.directory


class Directory(object):
    pass

class Test(unittest.TestCase):

    def test_Cloner(self):
        d = Directory()
        d.a = 1
        clone = zope.container.directory.Cloner(d)('foo')
        self.assertTrue(clone != d)
        self.assertEqual(clone.__class__, d.__class__)

def test_suite():
    flags = doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromName(__name__),
        doctest.DocFileSuite("directory.rst",
                             setUp=testing.setUp, tearDown=testing.tearDown,
                             optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
