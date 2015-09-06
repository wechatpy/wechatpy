# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from wechatpy.client.base import BaseWeChatClient
from wechatpy.client import api


class WeChatClient(BaseWeChatClient):
    """
    微信 API 操作类
    通过这个类可以操作微信 API，发送主动消息、群发消息和创建自定义菜单等。
    """

    API_BASE_URL = 'https://api.weixin.qq.com/cgi-bin/'

    menu = api.WeChatMenu()
    user = api.WeChatUser()
    group = api.WeChatGroup()
    media = api.WeChatMedia()
    card = api.WeChatCard()
    qrcode = api.WeChatQRCode()
    message = api.WeChatMessage()
    misc = api.WeChatMisc()
    merchant = api.WeChatMerchant()
    customservice = api.WeChatCustomService()
    datacube = api.WeChatDataCube()
    jsapi = api.WeChatJSAPI()
    material = api.WeChatMaterial()
    semantic = api.WeChatSemantic()
    shakearound = api.WeChatShakeAround()
    device = api.WeChatDevice()
    template = api.WeChatTemplate()
    poi = api.WeChatPoi()
    wifi = api.WeChatWiFi()

    def __init__(self, appid, secret, access_token=None, session=None):
        super(WeChatClient, self).__init__(access_token, session)
        self.appid = appid
        self.secret = secret

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
