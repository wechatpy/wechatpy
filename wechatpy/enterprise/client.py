from __future__ import absolute_import, unicode_literals
import time
import requests

from .._compat import json
from ..exceptions import WeChatClientException


class WeChatClient(object):

    API_BASE_URL = 'https://qyapi.weixin.qq.com/cgi-bin/'

    def __init__(self, corp_id, secret, access_token=None):
        self.corp_id = corp_id
        self.secret = secret
        self.access_token = access_token
        self.expires_at = None

    def _request(self, method, url_or_endpoint, **kwargs):
        if not (url_or_endpoint.startswith('http://') or
                url_or_endpoint.startswith('https://')):
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
            if result['errcode'] == 42001:
                # access_token expired, fetch a new one and retry request
                _token = self.fetch_access_token()
                self._access_token = _token['access_token']
                self.expires_at = int(time.time()) + _token['expires_in']
                return self._request(
                    method=method,
                    url=url,
                    **kwargs
                )
            else:
                raise WeChatClientException(
                    result['errcode'],
                    result['errmsg']
                )

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

    def fetch_access_token(self):
        """ Fetch access token"""
        res = requests.get(
            url='https://qyapi.weixin.qq.com/cgi-bin/gettoken',
            params={
                'corpid': self.corp_id,
                'corpsecret': self.secret
            }
        )
        result = res.json()
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatClientException(result['errcode'], result['errmsg'])
        return result

    @property
    def access_token(self):
        if self._access_token:
            if not self.expires_at:
                # user provided access_token, just return it
                return self._access_token

            timestamp = time.time()
            if self.expires_at - timestamp > 60:
                return self._access_token

        result = self.fetch_access_token()
        self._access_token = result['access_token']
        self.expires_at = int(time.time()) + 7200
        return self._access_token

    def create_department(self, name, parent_id=1):
        return self._post(
            'department/create',
            data={
                'name': name,
                'parentid': parent_id
            }
        )

    def update_department(self, id, name):
        return self._post(
            'department/update',
            data={
                'id': id,
                'name': name
            }
        )

    def delete_department(self, id):
        return self._get(
            'department/delete',
            params={
                'id': id
            }
        )

    def get_departments(self):
        return self._get('department/list')

    def upload_media(self, media_type, media_file):
        return self._post(
            'media/upload',
            params={
                'type': media_type
            },
            files={
                'media': media_file
            }
        )

    def download_media(self, media_id):
        return self._get(
            'media/get',
            params={
                'media_id': media_id
            }
        )

    def verify_user(self, user_id):
        return self._get(
            'user/authsucc',
            params={
                'userid': user_id
            }
        )
