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

from setuptools import setup, find_packages, Extension

setup(name='zope.app.container',
      version = '3.5.0a1',
      url='http://svn.zope.org/zope.app.container',
      license='ZPL 2.1',
      description='Zope container',
      author='Zope Corporation and Contributors',
      author_email='zope3-dev@zope.org',
      long_description=open('README.txt').read(),

      packages=find_packages('src'),
      package_dir = {'': 'src'},

      ext_modules=[Extension("zope.app.container._zope_app_container_contained",
                             [os.path.join("src", "zope", "app", "container",
                                           "_zope_app_container_contained.c")
                              ], include_dirs=['include']),
                   ],

      extras_require=dict(test=['zope.app.testing',
                                'zope.app.securitypolicy',
                                'zope.app.zcmlfiles',
                                'zope.app.file']),
      namespace_packages=['zope', 'zope.app'],
      install_requires=['setuptools',
                        'zope.interface',
                        'zope.deprecation',
                        'zope.app.publisher',
                        'zope.app.zapi',
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
                        'zope.app.broken',
                        'zope.copypastemove',
                        'ZODB3',
                        ],
      include_package_data = True,

      zip_safe = False,
      )
