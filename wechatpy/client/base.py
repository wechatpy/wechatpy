# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import time
import requests

from .._compat import json
from ..exceptions import WeChatClientException, APILimitedException


class BaseWeChatClient(object):

    API_BASE_URL = ''

    def __init__(self, access_token=None):
        self._access_token = access_token
        self.expires_at = None

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            url = '{base}{endpoint}'.format(
                base=self.API_BASE_URL,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        if 'params' not in kwargs:
            kwargs['params'] = {}
        if 'access_token' not in kwargs['params']:
            kwargs['params']['access_token'] = self.access_token
        if isinstance(kwargs.get('data', ''), dict):
            body = json.dumps(kwargs['data'], ensure_ascii=False)
            body = body.encode('utf-8')
            kwargs['data'] = body

        res = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        res.raise_for_status()
        result = res.json()

        if 'errcode' in result and result['errcode'] != 0:
            errcode = result['errcode']
            errmsg = result['errmsg']
            if errcode == 42001:
                # access_token expired, fetch a new one and retry request
                self.fetch_access_token()
                return self._request(
                    method=method,
                    url=url,
                    **kwargs
                )
            elif errcode == 45009:
                # api freq out of limit
                raise APILimitedException(errcode, errmsg)
            else:
                raise WeChatClientException(errcode, errmsg)

        return result

    def _get(self, url, **kwargs):
        return self._request(
            method='get',
            url_or_endpoint=url,
            **kwargs
        )

    def _post(self, url, **kwargs):
        return self._request(
            method='post',
            url_or_endpoint=url,
            **kwargs
        )

    def _fetch_access_token(self, url, params):
        """ The real fetch access token """
        res = requests.get(
            url=url,
            params=params
        )
        result = res.json()
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatClientException(result['errcode'], result['errmsg'])

        self._access_token = result['access_token']
        expires_in = 7200
        if 'expires_in' in result:
            expires_in = result['expires_in']
        self.expires_at = int(time.time()) + expires_in
        return result

    def fetch_access_token(self):
        raise NotImplementedError()

    @property
    def access_token(self):
        """ WeChat access token """
        if self._access_token:
            if not self.expires_at:
                # user provided access_token, just return it
                return self._access_token

            timestamp = time.time()
            if self.expires_at - timestamp > 60:
                return self._access_token

        self.fetch_access_token()
        return self._access_token
