# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import sys

if sys.version_info[0] == 2 and sys.version_info[1] == 6:
    try:
        import unittest2 as unittest
    except ImportError:
        import unittest
else:
    import unittest  # NOQA
