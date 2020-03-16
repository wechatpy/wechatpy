# -*- coding: utf-8 -*-


from wechatpy.exceptions import WeChatException


class InvalidCorpIdException(WeChatException):
    def __init__(self, errcode=-40005, errmsg="Invalid corp_id"):
        super().__init__(errcode, errmsg)
