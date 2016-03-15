# -*- coding: utf-8 -*-
"""
    wechatpy._compat
    ~~~~~~~~~~~~~~~~~

    This module makes it easy for wechatpy to run on both Python 2 and 3.

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import sys
import six
import warnings

warnings.warn("Module `wechatpy._compat` is deprecated, will be removed in 2.0"
              "use `wechatpy.utils` instead",
              DeprecationWarning, stacklevel=2)

from wechatpy.utils import get_querystring
from wechatpy.utils import json
