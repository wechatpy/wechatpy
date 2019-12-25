# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from wechatpy.client.base import BaseWeChatClient
from wechatpy.enterprise.client import api


class WeChatClient(BaseWeChatClient):
    API_BASE_URL = 'https://qyapi.weixin.qq.com/cgi-bin/'

    agent = api.WeChatAgent()
    appchat = api.WeChatAppChat()
    batch = api.WeChatBatch()
    chat = api.WeChatChat()
    department = api.WeChatDepartment()
    jsapi = api.WeChatJSAPI()
    material = api.WeChatMaterial()
    media = api.WeChatMedia()
    menu = api.WeChatMenu()
    message = api.WeChatMessage()
    misc = api.WeChatMisc()
    oauth = api.WeChatOAuth()
    service = api.WeChatService()
    shakearound = api.WeChatShakeAround()
    tag = api.WeChatTag()
    user = api.WeChatUser()
    external_contact = api.WeChatExternalContact()

    def __init__(self, corp_id, secret, contact_secret=None, access_token=None, contact_access_token=None,
                 session=None, timeout=None, auto_retry=True):
        super(WeChatClient, self).__init__(
            corp_id, access_token, contact_access_token, session, timeout, auto_retry
        )
        self.corp_id = corp_id
        self.secret = secret
        self.contact_secret = contact_secret

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

    @property
    def contact_access_token_key(self):
        return '{0}_{1}_contact_access_token'.format(self.corp_id, self.contact_secret[:10])

    def fetch_contact_access_token(self):
        """ Fetch access token"""
        return self._fetch_contact_access_token(
            url='https://qyapi.weixin.qq.com/cgi-bin/gettoken',
            params={
                'corpid': self.corp_id,
                'corpsecret': self.contact_secret
            }
        )
