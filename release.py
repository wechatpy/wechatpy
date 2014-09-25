#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, with_statement
import os
import sys

try:
    import pandoc
except ImportError:
    print('Please install pyandoc first, run pip install pyandoc.')
    sys.exit()

pandoc_path = os.popen('which pandoc').read().strip()
if not pandoc_path:
    print('Cannot find pandoc executable file, you should install pandoc.')
    sys.exit()

pandoc.core.PANDOC_PATH = pandoc_path

doc = pandoc.Document()
with open('README.md') as f:
    doc.markdown = f.read()
with open('README.rst', 'w+') as f:
    f.write(doc.rst)
os.system("python setup.py release")
os.remove('README.rst')
