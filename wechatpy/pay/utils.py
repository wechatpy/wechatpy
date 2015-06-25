# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import hashlib

from wechatpy.utils import to_binary


def format_url(params, api_key=None):
    data = [b'{0}={1}'.format(to_binary(k), to_binary(params[k]))
            for k in sorted(params)]
    if api_key:
        data.append('key={0}'.format(to_binary(api_key)))
    return b"&".join(data)


def calculate_signature(params, api_key):
    url = format_url(params, api_key)
    return hashlib.md5(url).hexdigest().upper()
