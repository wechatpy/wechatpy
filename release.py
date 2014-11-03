#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, with_statement
import os
import sys

try:
    import pypandoc
except ImportError:
    print('Please install pypandoc first, run pip install pypandoc.')
    sys.exit()

rst = pypandoc.convert('README.md', 'rst')
with open('README.rst', 'w+') as f:
    f.write(rst.encode('utf-8'))
os.system("python setup.py release")
os.remove('README.rst')
