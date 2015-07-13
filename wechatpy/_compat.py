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
import six.moves.urllib.parse as urlparse
try:
    """ Use simplejson if we can, fallback to json otherwise. """
    import simplejson as json
except ImportError:
    import json  # NOQA


def byte2int(s, index=0):
    """Get the ASCII int value of a character in a string.

    :param s: a string
    :param index: the position of desired character

    :return: ASCII int value
    """
    if six.PY2:
        return ord(s[index])
    return s[index]


def get_querystring(uri):
    parts = urlparse.urlsplit(uri)
    if sys.version_info[:2] == (2, 6):
        query = parts.path
        if query.startswith('?'):
            query = query[1:]
    else:
        query = parts.query
    return urlparse.parse_qs(query)
