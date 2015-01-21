# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from .base import BaseWeChatClient
from . import api


class WeChatClient(BaseWeChatClient):
    """
    微信 API 操作类
    通过这个类可以操作微信 API，发送主动消息、群发消息和创建自定义菜单等。
    """

    API_BASE_URL = 'https://api.weixin.qq.com/cgi-bin/'

    def __init__(self, appid, secret, access_token=None):
        self.appid = appid
        self.secret = secret
        self._access_token = access_token
        self.expires_at = None

        # APIs
        self.menu = api.WeChatMenu(self)
        self.user = api.WeChatUser(self)
        self.group = api.WeChatGroup(self)
        self.media = api.WeChatMedia(self)
        self.card = api.WeChatCard(self)
        self.qrcode = api.WeChatQRCode(self)
        self.message = api.WeChatMessage(self)
        self.misc = api.WeChatMisc(self)
        self.merchant = api.WeChatMerchant(self)
        self.customservice = api.WeChatCustomService(self)
        self.datacube = api.WeChatDataCube(self)

    def fetch_access_token(self):
        """
        获取 access token
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=通用接口文档

        :return: 返回的 JSON 数据包
        """
        return self._fetch_access_token(
            url='https://api.weixin.qq.com/cgi-bin/token',
            params={
                'grant_type': 'client_credential',
                'appid': self.appid,
                'secret': self.secret
            }
        )
