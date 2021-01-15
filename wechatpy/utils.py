# -*- coding: utf-8 -*-
"""
    wechatpy.utils
    ~~~~~~~~~~~~~~~

    This module provides some useful utilities.

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""

import string
import random
import hashlib


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access."""

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


class WeChatSigner:
    """WeChat data signer"""

    def __init__(self, delimiter=b""):
        self._data = []
        self._delimiter = to_binary(delimiter)

    def add_data(self, *args):
        """Add data to signer"""
        for data in args:
            self._data.append(to_binary(data))

    @property
    def signature(self):
        """Get data signature"""
        self._data.sort()
        str_to_sign = self._delimiter.join(self._data)
        return hashlib.sha1(str_to_sign).hexdigest()


def check_signature(token, signature, timestamp, nonce):
    """Check WeChat callback signature, raises InvalidSignatureException
    if check failed.

    :param token: WeChat callback token
    :param signature: WeChat callback signature sent by WeChat server
    :param timestamp: WeChat callback timestamp sent by WeChat server
    :param nonce: WeChat callback nonce sent by WeChat sever
    """
    signer = WeChatSigner()
    signer.add_data(token, timestamp, nonce)
    if signer.signature != signature:
        from wechatpy.exceptions import InvalidSignatureException

        raise InvalidSignatureException()


def check_wxa_signature(session_key, raw_data, client_signature):
    """校验前端传来的rawData签名正确
    详情请参考
    https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/signature.html # noqa

    :param session_key: code换取的session_key
    :param raw_data: 前端拿到的rawData
    :param client_signature: 前端拿到的signature
    :raises: InvalidSignatureException
    :return: 返回数据dict
    """
    str2sign = (raw_data + session_key).encode("utf-8")
    signature = hashlib.sha1(str2sign).hexdigest()
    if signature != client_signature:
        from wechatpy.exceptions import InvalidSignatureException

        raise InvalidSignatureException()


def to_text(value, encoding="utf-8"):
    """Convert value to unicode, default encoding is utf-8

    :param value: Value to be converted
    :param encoding: Desired encoding
    """
    if not value:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.decode(encoding)
    return str(value)


def to_binary(value, encoding="utf-8"):
    """Convert value to binary string, default encoding is utf-8

    :param value: Value to be converted
    :param encoding: Desired encoding
    """
    if not value:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode(encoding)
    return to_text(value).encode(encoding)


def timezone(zone):
    """Try to get timezone using pytz or python-dateutil

    :param zone: timezone str
    :return: timezone tzinfo or None
    """
    try:
        import pytz

        return pytz.timezone(zone)
    except ImportError:
        pass
    try:
        from dateutil.tz import gettz

        return gettz(zone)
    except ImportError:
        return None


def random_string(length=16):
    rule = string.ascii_letters + string.digits
    rand_list = random.sample(rule, length)
    return "".join(rand_list)
