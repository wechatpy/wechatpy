# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import time
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


class WeChatComponentClient(WeChatClient):

    """
    开放平台代公众号调用客户端
    """

    def __init__(
            self, appid, access_token, refresh_token, component, session=None):
        # 未用到secret，所以这里没有
        super(WeChatComponentClient, self).__init__(
            appid, '', access_token, session
        )
        self.appid = appid
        self.component = component
        self.session.set('{0}_refresh_token'.format(self.appid), refresh_token)

    @property
    def access_token(self):
        access_token = self.session.get('{0}_access_token'.format(self.appid))
        if not access_token:
            self.fetch_access_token()
            access_token = self.session.get(
                '{0}_access_token'.format(self.appid)
            )
        return access_token

    @property
    def refresh_token(self):
        return self.session.get('{0}_refresh_token'.format(self.appid))

    def fetch_access_token(self):
        """
        获取 access token
        详情请参考 https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list\
        &t=resource/res_list&verify=1&id=open1419318587&token=&lang=zh_CN

        :return: 返回的 JSON 数据包
        """
        expires_in = 7200
        result = self.component.refresh_authorizer_token(
            self.appid, self.refresh_token)
        if 'expires_in' in result:
            expires_in = result['expires_in']
        self.session.set(
            '{0}_access_token'.format(self.appid),
            result['authorizer_access_token'],
            expires_in
        )
        self.session.set(
            '{0}_refresh_token'.format(self.appid),
            result['authorizer_refresh_token'],
            expires_in
        )
        self.expires_at = int(time.time()) + expires_in
        return result
