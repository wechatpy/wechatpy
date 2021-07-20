# -*- coding: utf-8 -*-


class BaseWeChatPayAPI:
    """WeChat Pay API base class"""

    def __init__(self, client=None):
        self._client = client

    def _get(self, url, **kwargs):
        if getattr(self, "API_BASE_URL", None):
            kwargs["api_base_url"] = self.API_BASE_URL
        return self._client.get(url, **kwargs)

    def _post(self, url, **kwargs):
        if getattr(self, "API_BASE_URL", None):
            kwargs["api_base_url"] = self.API_BASE_URL
        return self._client.post(url, **kwargs)

    @property
    def appid(self):
        return self._client.appid

    @property
    def sub_appid(self):
        return self._client.sub_appid

    @property
    def mch_id(self):
        return self._client.mch_id

    @property
    def sub_mch_id(self):
        return self._client.sub_mch_id
