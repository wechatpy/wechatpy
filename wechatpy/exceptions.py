# -*- coding: utf-8 -*-
"""
    wechatpy.exceptions
    ~~~~~~~~~~~~~~~~~~~~

    Basic exceptions definition.

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import six

from wechatpy.utils import to_binary, to_text


class WeChatException(Exception):
    """Base exception for wechatpy"""

    def __init__(self, errcode, errmsg):
        """
        :param errcode: Error code
        :param errmsg: Error message
        """
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        if six.PY2:
            return to_binary('Error code: {code}, message: {msg}'.format(
                code=self.errcode,
                msg=self.errmsg
            ))
        else:
            return to_text('Error code: {code}, message: {msg}'.format(
                code=self.errcode,
                msg=self.errmsg
            ))


class WeChatClientException(WeChatException):
    """WeChat API client exception class"""
    pass


class InvalidSignatureException(WeChatException):
    """Invalid signature exception class"""

    def __init__(self, errcode=-40001, errmsg='Invalid signature'):
        super(InvalidSignatureException, self).__init__(errcode, errmsg)


class APILimitedException(WeChatException):
    """WeChat API call limited exception class"""

    def __init__(self, errcode=45009, errmsg='api freq out of limit'):
        super(APILimitedException, self).__init__(errcode, errmsg)


class InvalidAppIdException(WeChatException):
    """Invalid app_id exception class"""

    def __init__(self, errcode=-40005, errmsg='Invalid AppId'):
        super(InvalidAppIdException, self).__init__(errcode, errmsg)


class WeChatOAuthException(WeChatException):
    """WeChat OAuth API exception class"""
    pass


class WeChatPayException(WeChatException):
    """WeChat Pay API exception class"""
    def __init__(self, return_code, result_code=None, return_msg=None,
                 errcode=None, errmsg=None):
        """
        :param return_code: 返回状态码
        :param result_code: 业务结果
        :param return_msg: 返回信息
        :param errcode: 错误代码
        :param errmsg: 错误代码描述
        """
        super(WeChatPayException, self).__init__(errcode, errmsg)
        self.return_code = return_code
        self.result_code = result_code
        self.return_msg = return_msg
