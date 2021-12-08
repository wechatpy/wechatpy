# -*- coding: utf-8 -*-


from wechatpy.client.base import BaseWeChatClient
from wechatpy.iot.client import api


class IotClient(BaseWeChatClient):
    API_BASE_URL = "https://api.weixin.qq.com/ilink/api/"

    def __init__(
        self,
        app_id,
        secret,
        access_token=None,
        session=None,
        timeout=None,
        auto_retry=True,
    ):
        self.app_id = app_id
        self.secret = secret
        super().__init__(app_id, access_token, session, timeout, auto_retry)

    @property
    def access_token_key(self):
        return f"{self.app_id}_{self.secret[:10]}_access_token"

    def fetch_access_token(self):
        """Fetch access token"""
        return self._fetch_access_token(
            url="https://api.weixin.qq.com/cgi-bin/token",
            params={"grant_type": "client_credential", "appid": self.app_id, "secret": self.secret},
        )
