# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatInvoice(BaseWeChatAPI):
    API_BASE_URL = 'https://api.weixin.qq.com/card/invoice/'

    pass
