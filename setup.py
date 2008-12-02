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

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='zope.app.container',
      version = '3.7.0dev',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description='Zope Container',
      long_description=(
          read('README.txt')
          + '\n\n' +
          'Detailed Documentation\n'
          '**********************\n'
          + '\n\n' +
          read('src', 'zope', 'app', 'container', 'constraints.txt')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      keywords = "zope3 container",
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='http://cheeseshop.python.org/pypi/zope.app.container',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope', 'zope.app'],
      ext_modules=[Extension("zope.app.container._zope_app_container_contained",
                             [os.path.join("src", "zope", "app", "container",
                                           "_zope_app_container_contained.c")
                              ], include_dirs=['include']),
                   ],

      extras_require=dict(test=['zope.app.testing',
                                'zope.app.securitypolicy',
                                'zope.app.zcmlfiles',
                                'zope.app.file']),
      install_requires=['setuptools',
                        'zope.interface',
                        'zope.app.publisher',
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
                        'zope.i18n',
                        ],
      include_package_data = True,
      zip_safe = False,
      )
