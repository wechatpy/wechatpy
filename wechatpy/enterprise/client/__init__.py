# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from wechatpy.client.base import BaseWeChatClient
from wechatpy.enterprise.client import api


class WeChatClient(BaseWeChatClient):

    API_BASE_URL = 'https://qyapi.weixin.qq.com/cgi-bin/'

    user = api.WeChatUser()
    department = api.WeChatDepartment()
    menu = api.WeChatMenu()
    message = api.WeChatMessage()
    tag = api.WeChatTag()
    media = api.WeChatMedia()
    misc = api.WeChatMisc()
    agent = api.WeChatAgent()
    batch = api.WeChatBatch()
    jsapi = api.WeChatJSAPI()
    material = api.WeChatMaterial()
    oauth = api.WeChatOAuth()
    shakearound = api.WeChatShakeAround()
    service = api.WeChatService()
    chat = api.WeChatChat()

    def __init__(self, corp_id, secret, access_token=None,
                 session=None, timeout=None, auto_retry=True):
        super(WeChatClient, self).__init__(
            corp_id, access_token, session, timeout, auto_retry
        )
        self.corp_id = corp_id
        self.secret = secret

    @property
    def access_token_key(self):
        return '{0}_{1}_access_token'.format(self.corp_id, self.secret[:10])

    def fetch_access_token(self):
        """ Fetch access token"""
        return self._fetch_access_token(
            url='https://qyapi.weixin.qq.com/cgi-bin/gettoken',
            params={
                'corpid': self.corp_id,
                'corpsecret': self.secret
            }
        )
