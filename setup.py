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
import platform

from setuptools import setup, find_packages, Extension

def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()

def alltests():
    import sys
    import unittest
    # use the zope.testrunner machinery to find all the
    # test suites we've put under ourselves
    import zope.testrunner.find
    import zope.testrunner.options
    here = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
    args = sys.argv[:]
    defaults = ["--test-path", here]
    options = zope.testrunner.options.get_options(args, defaults)
    suites = list(zope.testrunner.find.find_suites(options))
    return unittest.TestSuite(suites)

# PyPy cannot correctly build the C optimizations, and even if it
# could they would be anti-optimizations (the C extension
# compatibility layer is known-slow, and defeats JIT opportunities).
py_impl = getattr(platform, 'python_implementation', lambda: None)
pure_python = os.environ.get('PURE_PYTHON', False)
is_pypy = py_impl() == 'PyPy'

if pure_python or is_pypy:
    ext_modules = []
else:
    ext_modules = [Extension("zope.container._zope_container_contained",
                             [os.path.join("src", "zope", "container",
                                           "_zope_container_contained.c")
                             ], include_dirs=['include']),
    ]

install_requires = [
    'setuptools',
    'six',
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
    'zope.traversing>=4.0.0a1',
    'zope.publisher',
    'zope.proxy>=4.1.5',
    'persistent>=4.1.0',
    'BTrees'
]


setup(name='zope.container',
      version=read('version.txt').strip(),
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      description='Zope Container',
      long_description=(
          read('README.rst')
          + '\n\n' +
          read('CHANGES.rst')
      ),
      keywords="zope container",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3',
      ],
      url='http://github.com/zopefoundation/zope.container',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['zope'],
      ext_modules=ext_modules,
      extras_require={
          'docs': [
              'Sphinx',
              'repoze.sphinx.autointerface',
          ],
          'test': [
              'zope.testing',
              'zope.testrunner',
          ],
          'zcml': [
              'zope.component[zcml]',
              'zope.configuration',
              'zope.security[zcml]>=4.0.0a3',
          ],
          'zodb': [
              'ZODB>=3.10',
          ],
      },
      install_requires=install_requires,
      tests_require=[
          'zope.testing',
          'zope.testrunner',
      ],
      test_suite='__main__.alltests',
      include_package_data=True,
      zip_safe=False,
)
