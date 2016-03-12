# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
try:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)
except ImportError:
    from pkg_resources import declare_namespace
    declare_namespace(__name__)

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
    scan = api.WeChatScan()

    def __init__(self, appid, secret, access_token=None,
                 session=None, timeout=None):
        super(WeChatClient, self).__init__(
            appid, access_token, session, timeout
        )
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

    def __init__(self, appid, component, access_token=None,
                 refresh_token=None, session=None, timeout=None):
        # 未用到secret，所以这里没有
        super(WeChatComponentClient, self).__init__(
            appid, '', access_token, session, timeout
        )
        self.appid = appid
        self.component = component
        # 如果公众号是刚授权，外部还没有缓存access_token和refresh_token
        # 可以传入这两个值，session 会缓存起来。
        # 如果外部已经缓存，这里只需要传入 appid，component和session即可
        if access_token:
            self.session.set(self.access_token_key, access_token, 7200)
        if refresh_token:
            self.session.set(self.refresh_token_key, refresh_token, 7200)

    @property
    def access_token_key(self):
        return '{0}_access_token'.format(self.appid)

    @property
    def refresh_token_key(self):
        return '{0}_refresh_token'.format(self.appid)

    @property
    def access_token(self):
        access_token = self.session.get(self.access_token_key)
        if not access_token:
            self.fetch_access_token()
            access_token = self.session.get(self.access_token_key)
        return access_token

    @property
    def refresh_token(self):
        return self.session.get(self.refresh_token_key)

    def fetch_access_token(self):
        """
        获取 access token
        详情请参考 https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list\
        &t=resource/res_list&verify=1&id=open1419318587&token=&lang=zh_CN

        这是内部刷新机制。请不要完全依赖！
        因为有可能在缓存期间没有对此公众号的操作，造成refresh_token失效。

        :return: 返回的 JSON 数据包
        """
        expires_in = 7200
        result = self.component.refresh_authorizer_token(
            self.appid, self.refresh_token)
        if 'expires_in' in result:
            expires_in = result['expires_in']
        self.session.set(
            self.access_token_key,
            result['authorizer_access_token'],
            expires_in
        )
        self.session.set(
            self.refresh_token_key,
            result['authorizer_refresh_token'],
            expires_in
        )
        self.expires_at = int(time.time()) + expires_in
        return result
