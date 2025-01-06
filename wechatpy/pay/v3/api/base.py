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

    def _download_file(self, url, **kwargs):
        return self._client.download_file(url, **kwargs)

    @property
    def appid(self):
        return self._client.appid

    @property
    def mch_id(self):
        return self._client.mch_id

    def calculate_pay_params_signature_rsa(self, app_id, package, timestamp=None, nonce_str=None):
        return self._client.calculate_pay_params_signature_rsa(app_id, package, timestamp, nonce_str)
