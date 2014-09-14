from __future__ import absolute_import, unicode_literals
import time
import requests
try:
    import simplejson as json
except ImportError:
    import json


class WeChatException(Exception):

    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg


class WeChatClient(object):

    BASE_URL = 'https://api.weixin.qq.com/cgi-bin'

    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret
        self._access_token = None
        self.expires_at = None

    def _request(self, method, url, **kwargs):
        if 'params' not in kwargs:
            kwargs['params'] = {'access_token': self.access_token}
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
            raise WeChatException(result['errcode'], result['errmsg'])

        return result

    def _get(self, url, **kwargs):
        return self._request(
            method='get',
            url=url,
            **kwargs
        )

    def _post(self, url, **kwargs):
        return self._request(
            method='post',
            url=url,
            **kwargs
        )

    def fetch_access_token(self):
        """ Fetch access token"""
        return self._get(
            url='https://api.weixin.qq.com/cgi-bin/token',
            params={
                'grant_type': 'client_credential',
                'appid': self.appid,
                'secret': self.secret
            }
        )

    @property
    def access_token(self):
        if self._access_token:
            timestamp = time.time()
            if self.expires_at - timestamp > 60:
                return self._access_token
        result = self.fetch_access_token()
        self._access_token = result['access_token']
        self.expires_at = int(time.time()) + result['expires_in']

    def send_text_message(self, user_id, content):
        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'text',
                'text': {'content': content}
            }
        )
