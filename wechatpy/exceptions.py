from __future__ import absolute_import, unicode_literals
import six

from .utils import to_binary, to_text


class WeChatException(Exception):

    def __init__(self, errcode, errmsg):
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
    pass


class InvalidSignatureException(WeChatException):

    def __init__(self, errcode=-40001, errmsg='Invalid signature'):
        super(InvalidSignatureException, self).__init__(errcode, errmsg)


class APILimitedException(WeChatException):

    def __init__(self, errcode=45009, errmsg='api freq out of limit'):
        super(APILimitedException, self).__init__(errcode, errmsg)


class InvalidAppIdException(WeChatException):

    def __init__(self, errcode=-40005, errmsg='Invalid AppId'):
        super(InvalidAppIdException, self).__init__(errcode, errmsg)
