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

    def __init__(self, corp_id, secret, access_token=None):
        self.corp_id = corp_id
        self.secret = secret
        self._access_token = access_token
        self.expires_at = None

    def fetch_access_token(self):
        """ Fetch access token"""
        return self._fetch_access_token(
            url='https://qyapi.weixin.qq.com/cgi-bin/gettoken',
            params={
                'corpid': self.corp_id,
                'corpsecret': self.secret
            }
        )
