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
import sys

from setuptools import Extension
from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


def get_include_dirs():
    """
    Return additional include directories that might be needed to
    compile extensions. Specifically, we need the cPersistence.h from
    persistent, and the `_zope_proxy_proxy.c` from zope.proxy.

    This is done lazily, because ``setup_requires`` will not have made
    dependencies available at the time the Extension is defined, only when
    ``setup`` actually runs.
    """
    # setuptools will put the normal include directory for Python.h on the
    # include path automatically. We don't want to override that with
    # a different Python.h if we can avoid it: On older versions of Python,
    # that can cause issues with debug builds
    # (see https://github.com/gevent/gevent/issues/1461)
    # so order matters here.
    #
    # sysconfig.get_path('include') will return the path to the main include
    # directory. In a virtual environment, that's a symlink to the main
    # Python installation include directory:
    #
    #   sysconfig.get_path('include') -> /path/to/venv/include/python3.8
    #   /path/to/venv/include/python3.7 -> /pythondir/include/python3.8
    #
    # distutils.sysconfig.get_python_inc() returns the main Python installation
    # include directory:
    #   distutils.sysconfig.get_python_inc() -> /pythondir/include/python3.8
    #
    # Neither sysconfig dir is not enough if we're in a virtualenv; the proxy.h
    # header goes into a site/ subdir.
    # See https://github.com/pypa/pip/issues/4610
    import sysconfig
    from distutils import sysconfig as dist_sysconfig

    dist_inc_dir = os.path.abspath(dist_sysconfig.get_python_inc())  # 1
    sys_inc_dir = os.path.abspath(sysconfig.get_path("include"))  # 2

    def header_dirs_for_dep(distname, headername):  # 3 and 4

        venv_include_dir = os.path.join(
            sys.prefix, 'include', 'site',
            'python' + sysconfig.get_python_version(),
            distname,
        )
        venv_include_dir = os.path.abspath(venv_include_dir)

        # If we're installed via buildout, and buildout also installs
        # distname, we have *NO* access to its headers in a standard
        # way. So we rely on being able to import the distribution and
        # it including the needed file as package data.

        try:
            import pkg_resources
            if pkg_resources.resource_exists(distname, headername):
                resource_dir = os.path.dirname(
                    pkg_resources.resource_filename(distname, headername))
        except ImportError:
            resource_dir = None

        return venv_include_dir, resource_dir

    return [
        p
        for p in (
            (dist_inc_dir, sys_inc_dir)
            + header_dirs_for_dep('zope.proxy', '_zope_proxy_proxy.c')
            + header_dirs_for_dep('persistent', 'cPersistence.h')
        )
        if p is not None and os.path.exists(p)
    ]


class IncludeDirs(object):
    dirs = None

    def __getattribute__(self, name):
        if object.__getattribute__(self, 'dirs') is None:
            self.dirs = get_include_dirs()
        dirs = object.__getattribute__(self, 'dirs')
        if name == 'dirs':
            return dirs
        return getattr(dirs, name)

    def __iter__(self):
        return iter(self.dirs)


if str is bytes and hasattr(sys, 'pypy_version_info'):
    # zope.proxy, as of 4.3.5, cannot compile on PyPy2 7.3.0
    # because it uses cl_dict in a PyClassObject, which does not exist.
    ext_modules = []
else:
    ext_modules = [
        Extension(
            "zope.container._zope_container_contained",
            [os.path.join("src", "zope", "container",
                          "_zope_container_contained.c")],
            include_dirs=IncludeDirs(),
        ),
    ]

setup_requires = [
    'persistent >= 4.1.0',
    'zope.proxy >= 4.1.5',
]


install_requires = setup_requires + [
    'BTrees',
    'six',
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
    'zope.publisher',
    'zope.schema',
    'zope.security',
    'zope.size',
    'zope.traversing>=4.0.0a1',
    'setuptools',
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
      version='4.8',
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
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope :: 3',
      ],
      url='https://github.com/zopefoundation/zope.container',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['zope'],
      ext_modules=ext_modules,
      extras_require=extras,
      install_requires=install_requires,
      setup_requires=setup_requires,
      tests_require=extras['test'],
      include_package_data=True,
      zip_safe=False,
      python_requires=', '.join([
          '>=2.7',
          '!=3.0.*',
          '!=3.1.*',
          '!=3.2.*',
          '!=3.3.*',
          '!=3.4.*',
      ]),
      )
