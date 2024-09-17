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

from setuptools import Extension
from setuptools import find_packages
from setuptools import setup


version = '6.1'


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


ext_modules = [
    Extension(
        "zope.container._zope_container_contained",
        [os.path.join("src", "zope", "container",
                      "_zope_container_contained.c")],
        include_dirs=[os.path.join('include', 'persistent'),
                      os.path.join('include', 'zope.proxy')],
    ),
]


extras = {
    'docs': [
        'Sphinx',
        'repoze.sphinx.autointerface',
        'sphinx_rtd_theme',
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
}

extras['test'] += (extras['zodb'] + extras['zcml'])


setup(name='zope.container',
      version=version,
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
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope :: 3',
      ],
      url='https://github.com/zopefoundation/zope.container',
      project_urls={
          'Documentation': 'https://zopecontainer.readthedocs.io',
          'Issue Tracker': ('https://github.com/zopefoundation'
                            '/zope.container/issues'),
          'Sources': 'https://github.com/zopefoundation/zope.container',
      },
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['zope'],
      ext_modules=ext_modules,
      install_requires=[
          'BTrees',
          'persistent>=4.1.0',
          'zope.cachedescriptors',
          'zope.component',
          'zope.deferredimport',
          'zope.dottedname',
          'zope.event',
          'zope.filerepresentation',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.lifecycleevent>=3.5.2',
          'zope.location>=3.5.4',
          'zope.proxy>=4.1.5',
          'zope.publisher',
          'zope.schema',
          'zope.security',
          'zope.size',
          'zope.traversing>=4.0.0a1',
          'setuptools',
      ],
      extras_require=extras,
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.8',
      )
