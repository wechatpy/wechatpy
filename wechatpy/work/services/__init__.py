# -*- coding: utf-8 -*-
import json
import time
import logging
import requests

from wechatpy.client.base import BaseWeChatClient
from wechatpy.exceptions import WeChatClientException
from wechatpy.work.services import api

logger = logging.getLogger(__name__)


class WeChatServiceClient(BaseWeChatClient):
    """
    注意：access_token在第三方应用变更为suite_access_token参数
    """

    API_BASE_URL = "https://qyapi.weixin.qq.com/cgi-bin/"

    auth = api.WeChatAuth()
    miniprogram = api.WeChatMiniProgram()

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

    def _fetch_access_token(self, url, params):
        """The real fetch access token"""
        logger.info("Fetching access token")
        res = self._http.post(url=url, json=params)
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
        self.session.set(self.access_token_key, result["suite_access_token"], expires_in)
        self.expires_at = int(time.time()) + expires_in
        return result

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(("http://", "https://")):
            api_base_url = kwargs.pop("api_base_url", self.API_BASE_URL)
            url = f"{api_base_url}{url_or_endpoint}"
        else:
            url = url_or_endpoint

        if "params" not in kwargs:
            kwargs["params"] = {}
        if isinstance(kwargs["params"], dict) and "suite_access_token" not in kwargs["params"]:
            kwargs["params"]["suite_access_token"] = self.access_token
        if isinstance(kwargs.get("data", ""), dict):
            body = json.dumps(kwargs["data"], ensure_ascii=False)
            body = body.encode("utf-8")
            kwargs["data"] = body

        kwargs["timeout"] = kwargs.get("timeout", self.timeout)
        result_processor = kwargs.pop("result_processor", None)
        res = self._http.request(method=method, url=url, **kwargs)
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

        return self._handle_result(res, method, url, result_processor, **kwargs)

    def fetch_access_token(self):
        """Fetch access token"""
        return self._fetch_access_token(
            url="https://qyapi.weixin.qq.com/cgi-bin/service/get_suite_token",
            params={"suite_id": self.suite_id, "suite_secret": self.suite_secret, "suite_ticket": self.suite_ticket},
        )
