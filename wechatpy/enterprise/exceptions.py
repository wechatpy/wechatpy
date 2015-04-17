# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.exceptions import WeChatException


class InvalidCorpIdException(WeChatException):

    def __init__(self, errcode=-40005, errmsg='Invalid corp_id'):
        super(InvalidCorpIdException, self).__init__(errcode, errmsg)
