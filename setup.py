##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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
"""Setup for zope.app.container package

$Id$
"""

import os

try:
    from setuptools import setup, Extension
except ImportError, e:
    from distutils.core import setup, Extension

setup(name='zope.app.container',
      version='3.4-dev',
      url='http://svn.zope.org/zope.app.container',
      license='ZPL 2.1',
      description='Zope container',
      author='Zope Corporation and Contributors',
      author_email='zope3-dev@zope.org',
      long_description="This package define interfaces of"
                       "container components, and provides"
                       "sample container implementations.",

      packages=['zope', 'zope.app', 'zope.app.container',
                'zope.app.container.tests',
                'zope.app.container.ftests',
                'zope.app.container.browser',
                'zope.app.container.browser.tests',
                'zope.app.container.browser.ftests'
                ],
      package_dir = {'': 'src'},

      ext_modules=[Extension("zope.app.container._zope_app_container_contained",
                             [os.path.join("src", "zope", "app", "container",
                                           "_zope_app_container_contained.c")
                              ], include_dirs=['include']),
                   ],

      namespace_packages=['zope', 'zope.app'],
      tests_require = ['zope.testing'],
      install_requires=['zope.interface',
                        'zope.cachedescriptors',
                        'zope.dottedname',
                        'zope.schema',
                        'zope.component',
                        'zope.event',
                        'zope.location',
                        'zope.exceptions',
                        'zope.security',
                        'zope.lifecycleevent',
                        'zope.i18nmessageid',
                        'zope.filerepresentation',
                        'zope.size',
                        'zope.traversing',
                        'zope.publisher',
                        'zope.dublincore',
                        'zope.copypastemove',
                        ],
      include_package_data = True,

      zip_safe = False,
      )
