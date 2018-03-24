#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import sys

try:
    import pypandoc
except ImportError:
    print('Please install pypandoc first, run pip install pypandoc.')
    sys.exit()

rst = pypandoc.convert('README.md', 'rst')
with open('README.rst', 'wb') as f:
    f.write(rst.encode('utf-8'))
os.system("python setup.py release")
os.remove('README.rst')
