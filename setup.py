#!/usr/bin/env python
from __future__ import with_statement, print_function

try:
    # python setup.py test
    import multiprocessing  # NOQA
except ImportError:
    pass

import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


cmdclass = {}
cmdclass['test'] = PyTest

# patch bdist_wheel
try:
    from wheel.bdist_wheel import bdist_wheel

    REPLACE = (
        'macosx_10_6_intel.'
        'macosx_10_9_intel.'
        'macosx_10_9_x86_64.'
        'macosx_10_10_intel.'
        'macosx_10_10_x86_64'
    )

    class _bdist_wheel(bdist_wheel):
        def get_tag(self):
            tag = bdist_wheel.get_tag(self)
            if tag[2] == 'macosx_10_6_intel':
                tag = (tag[0], tag[1], REPLACE)
            return tag

    cmdclass['bdist_wheel'] = _bdist_wheel
except ImportError:
    pass

readme = 'README.md'
if os.path.exists('README.rst'):
    readme = 'README.rst'
with open(readme, 'rb') as f:
    long_description = f.read().decode('utf-8')

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

setup(
    name='wechatpy',
    version='1.4.1',
    author='messense',
    author_email='messense@icloud.com',
    url='https://github.com/messense/wechatpy',
    packages=find_packages(),
    keywords='WeChat, wexin, SDK',
    description='wechatpy: WeChat SDK for Python',
    long_description=long_description,
    install_requires=requirements,
    include_package_data=True,
    # namespace_packages=['wechatpy'],
    tests_require=[
        'pytest',
        'httmock',
        'redis',
        'pymemcache',
        'shove',
    ],
    cmdclass=cmdclass,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    extras_require={
        'cryptography': ['cryptography'],
        'pycrypto': ['pycrypto'],
    }
)
