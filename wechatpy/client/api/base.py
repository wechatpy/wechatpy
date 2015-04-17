# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class BaseWeChatAPI(object):
    """ WeChat API base class """

    def __init__(self, client):
        """
        Init with WeChatClient object

        :param client: An instance of WeChatClient
        """
        self._client = client

    def _get(self, url, **kwargs):
        if getattr(self, 'API_BASE_URL', None):
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client._get(url, **kwargs)

    def _post(self, url, **kwargs):
        if getattr(self, 'API_BASE_URL', None):
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client._post(url, **kwargs)

    @property
    def access_token(self):
        return self._client.access_token
