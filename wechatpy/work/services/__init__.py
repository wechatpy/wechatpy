# -*- coding: utf-8 -*-

import time
import logging
import requests
from wechatpy.client.base import BaseWeChatClient
from wechatpy.exceptions import WeChatClientException
from wechatpy.work.services import api

logger = logging.getLogger(__name__)


class WeChatServiceClient(BaseWeChatClient):
    API_BASE_URL = "https://qyapi.weixin.qq.com/cgi-bin/"

    auth = api.WeChatAuth()

    def __init__(
        self,
        corp_id,
        suite_id,
        suite_secret,
        suite_ticket,
        access_token=None,
        session=None,
        timeout=None,
        auto_retry=True,
    ):
        self.corp_id = corp_id
        self.suite_id = suite_id
        self.suite_secret = suite_secret
        self.suite_ticket = suite_ticket
        super().__init__(corp_id, access_token, session, timeout, auto_retry)

    @property
    def access_token_key(self):
        return f"services_{self.corp_id}_{self.suite_id}_access_token"

    def _fetch_access_token(self, url, data):
        """The real fetch access token"""
        logger.info("Fetching access token")
        res = self._http.post(url=url, data=data)
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise WeChatClientException(
                errcode=None,
                errmsg=None,
                client=self,
                request=reqe.request,
                response=reqe.response,
            )
        result = res.json()
        if "errcode" in result and result["errcode"] != 0:
            raise WeChatClientException(
                result["errcode"],
                result["errmsg"],
                client=self,
                request=res.request,
                response=res,
            )

        expires_in = 7200
        if "expires_in" in result:
            expires_in = result["expires_in"]
        self.session.set(self.access_token_key, result["access_token"], expires_in)
        self.expires_at = int(time.time()) + expires_in
        return result

    def fetch_access_token(self):
        """Fetch access token"""
        return self._fetch_access_token(
            url="https://qyapi.weixin.qq.com/cgi-bin/service/get_suite_token",
            data={"suite_id": self.suite_id, "suite_secret": self.suite_secret, "suite_ticket": self.suite_ticket},
        )
