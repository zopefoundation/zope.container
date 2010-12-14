##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
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
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.container package
"""
import os
from setuptools import setup, find_packages, Extension

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='zope.container',
      version = '3.12.1dev',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      description='Zope Container',
      long_description=(
          read('README.txt')
          + '\n\n' +
          '.. contents::\n'
          + '\n\n' +
          read('src', 'zope', 'container', 'constraints.txt')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      keywords = "zope container",
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
      url='http://pypi.python.org/pypi/zope.container',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope'],
      ext_modules=[Extension("zope.container._zope_container_contained",
                             [os.path.join("src", "zope", "container",
                                           "_zope_container_contained.c")
                              ], include_dirs=['include']),
                   ],
      extras_require=dict(
          test=['zope.testing',
                ],
          zcml=[
                'zope.component[zcml]',
                'zope.configuration',
                'zope.security[zcml]>=3.8',
                ]),
      install_requires=['setuptools',
                        'zope.interface',
                        'zope.dottedname',
                        'zope.schema',
                        'zope.component',
                        'zope.event',
                        'zope.location>=3.5.4',
                        'zope.security',
                        'zope.lifecycleevent>=3.5.2',
                        'zope.i18nmessageid',
                        'zope.filerepresentation',
                        'zope.size',
                        'zope.traversing',
                        'zope.publisher',
                        'zope.broken',
                        'ZODB3',
                        ],
      include_package_data = True,
      zip_safe = False,
      )
