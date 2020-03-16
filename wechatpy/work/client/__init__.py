# -*- coding: utf-8 -*-


from wechatpy.client.base import BaseWeChatClient
from wechatpy.work.client import api


class WeChatClient(BaseWeChatClient):
    API_BASE_URL = "https://qyapi.weixin.qq.com/cgi-bin/"

    agent = api.WeChatAgent()
    appchat = api.WeChatAppChat()
    batch = api.WeChatBatch()
    calendar = api.WeChatCalendar()
    department = api.WeChatDepartment()
    external_contact = api.WeChatExternalContact()
    jsapi = api.WeChatJSAPI()
    media = api.WeChatMedia()
    menu = api.WeChatMenu()
    message = api.WeChatMessage()
    misc = api.WeChatMisc()
    oauth = api.WeChatOAuth()
    schedule = api.WeChatSchedule()
    service = api.WeChatService()
    tag = api.WeChatTag()
    user = api.WeChatUser()
    oa = api.WeChatOA()

    def __init__(
        self, corp_id, secret, access_token=None, session=None, timeout=None, auto_retry=True,
    ):
        self.corp_id = corp_id
        self.secret = secret
        super().__init__(corp_id, access_token, session, timeout, auto_retry)

    @property
    def access_token_key(self):
        return "{0}_{1}_access_token".format(self.corp_id, self.secret[:10])

    def fetch_access_token(self):
        """ Fetch access token"""
        return self._fetch_access_token(
            url="https://qyapi.weixin.qq.com/cgi-bin/gettoken",
            params={"corpid": self.corp_id, "corpsecret": self.secret},
        )
