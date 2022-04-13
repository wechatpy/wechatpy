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
    email = api.WeChatEMail()
    export = api.WeChatExport()
    external_contact = api.WeChatExternalContact()
    external_contact_group_chat = api.WeChatExternalContactGroupChat()
    invoice = api.WeChatInvoice()
    jsapi = api.WeChatJSAPI()
    kf = api.WeChatKF()
    kf_message = api.WeChatKFMessage()
    media = api.WeChatMedia()
    menu = api.WeChatMenu()
    message = api.WeChatMessage()
    misc = api.WeChatMisc()
    oa = api.WeChatOA()
    oauth = api.WeChatOAuth()
    schedule = api.WeChatSchedule()
    service = api.WeChatService()
    tag = api.WeChatTag()
    user = api.WeChatUser()
    living = api.WeChatLiving()

    def __init__(
        self,
        corp_id,
        secret,
        access_token=None,
        session=None,
        timeout=None,
        auto_retry=True,
    ):
        self.corp_id = corp_id
        self.secret = secret
        super().__init__(corp_id, access_token, session, timeout, auto_retry)

    @property
    def access_token_key(self):
        return f"{self.corp_id}_{self.secret[:10]}_access_token"

    def fetch_access_token(self):
        """Fetch access token"""
        return self._fetch_access_token(
            url="https://qyapi.weixin.qq.com/cgi-bin/gettoken",
            params={"corpid": self.corp_id, "corpsecret": self.secret},
        )
