# -*- coding: utf-8 -*-
"""
    wechatpy.exceptions
    ~~~~~~~~~~~~~~~~~~~~

    Basic exceptions definition.

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""


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
        s = f"Error code: {self.errcode}, message: {self.errmsg}"
        return s

    def __repr__(self):
        _repr = f"{self.__class__.__name__}({self.errcode}, {self.errmsg})"
        return _repr


class WeChatClientException(WeChatException):
    """WeChat API client exception class"""

    def __init__(self, errcode, errmsg, client=None, request=None, response=None):
        super().__init__(errcode, errmsg)
        self.client = client
        self.request = request
        self.response = response


class InvalidSignatureException(WeChatException):
    """Invalid signature exception class"""

    def __init__(self, errcode=-40001, errmsg="Invalid signature"):
        super().__init__(errcode, errmsg)


class APILimitedException(WeChatClientException):
    """WeChat API call limited exception class"""

    pass


class InvalidAppIdException(WeChatException):
    """Invalid app_id exception class"""

    def __init__(self, errcode=-40005, errmsg="Invalid AppId"):
        super().__init__(errcode, errmsg)


class InvalidMchIdException(WeChatException):
    """Invalid mch_id exception class"""

    def __init__(self, errcode=-40006, errmsg="Invalid MchId"):
        super().__init__(errcode, errmsg)


class WeChatOAuthException(WeChatClientException):
    """WeChat OAuth API exception class"""

    pass


class WeChatComponentOAuthException(WeChatClientException):
    """WeChat Component OAuth API exception class"""

    pass


class WeChatPayException(WeChatClientException):
    """WeChat Pay API exception class"""

    def __init__(
        self,
        return_code,
        result_code=None,
        return_msg=None,
        errcode=None,
        errmsg=None,
        client=None,
        request=None,
        response=None,
    ):
        """
        :param return_code: 返回状态码
        :param result_code: 业务结果
        :param return_msg: 返回信息
        :param errcode: 错误代码
        :param errmsg: 错误代码描述
        """
        super().__init__(errcode, errmsg, client, request, response)
        self.return_code = return_code
        self.result_code = result_code
        self.return_msg = return_msg

    def __str__(self):
        _str = f"Error code: {self.return_code}, message: {self.return_msg}. Pay Error code: {self.errcode}, message: {self.errmsg}"
        return _str

    def __repr__(self):
        _repr = f"{self.__class__.__name__}({self.return_code}, {self.return_msg}). Pay({self.errcode}, {self.errmsg})"
        return _repr
