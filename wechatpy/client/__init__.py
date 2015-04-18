# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import weakref

from wechatpy.client.base import BaseWeChatClient
from wechatpy.client import api


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

        weak_self = weakref.proxy(self)

        # APIs
        self.menu = api.WeChatMenu(weak_self)
        self.user = api.WeChatUser(weak_self)
        self.group = api.WeChatGroup(weak_self)
        self.media = api.WeChatMedia(weak_self)
        self.card = api.WeChatCard(weak_self)
        self.qrcode = api.WeChatQRCode(weak_self)
        self.message = api.WeChatMessage(weak_self)
        self.misc = api.WeChatMisc(weak_self)
        self.merchant = api.WeChatMerchant(weak_self)
        self.customservice = api.WeChatCustomService(weak_self)
        self.datacube = api.WeChatDataCube(weak_self)
        self.jsapi = api.WeChatJSAPI(weak_self)
        self.material = api.WeChatMaterial(weak_self)
        self.semantic = api.WeChatSemantic(weak_self)
        self.shakearound = api.WeChatShakeAround(weak_self)
        self.device = api.WeChatDevice(weak_self)

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
