# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import sys
import time
import inspect

import six
import requests
from wechatpy.utils import json, get_querystring
from wechatpy.session.memorystorage import MemoryStorage
from wechatpy.exceptions import WeChatClientException, APILimitedException
from wechatpy.client.api.base import BaseWeChatAPI


def _is_api_endpoint(obj):
    return isinstance(obj, BaseWeChatAPI)


class BaseWeChatClient(object):

    API_BASE_URL = ''

    def __new__(cls, *args, **kwargs):
        self = super(BaseWeChatClient, cls).__new__(cls)
        if sys.version_info[:2] == (2, 6):
            # Python 2.6 inspect.gemembers bug workaround
            # http://bugs.python.org/issue1785
            for _class in cls.__mro__:
                if issubclass(_class, BaseWeChatClient):
                    for name, api in _class.__dict__.items():
                        if isinstance(api, BaseWeChatAPI):
                            api_cls = type(api)
                            api = api_cls(self)
                            setattr(self, name, api)
        else:
            api_endpoints = inspect.getmembers(self, _is_api_endpoint)
            for name, api in api_endpoints:
                api_cls = type(api)
                api = api_cls(self)
                setattr(self, name, api)
        return self

    def __init__(self, appid, access_token=None, session=None, timeout=None):
        self.appid = appid
        self.expires_at = None
        self.session = session or MemoryStorage()
        self.timeout = timeout

        if isinstance(session, six.string_types):
            from shove import Shove
            from wechatpy.session.shovestorage import ShoveStorage

            querystring = get_querystring(session)
            prefix = querystring.get('prefix', ['wechatpy'])[0]

            shove = Shove(session)
            storage = ShoveStorage(shove, prefix)
            self.session = storage

        self.session.set(self.access_token_key, access_token)

    @property
    def access_token_key(self):
        return '{0}_access_token'.format(self.appid)

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = '{base}{endpoint}'.format(
                base=api_base_url,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        # 群发消息上传视频接口地址 HTTPS 证书错误，暂时忽略证书验证
        if url.startswith('https://file.api.weixin.qq.com'):
            kwargs['verify'] = False

        if 'params' not in kwargs:
            kwargs['params'] = {}
        if isinstance(kwargs['params'], dict) and \
                'access_token' not in kwargs['params']:
            kwargs['params']['access_token'] = self.access_token
        if isinstance(kwargs.get('data', ''), dict):
            body = json.dumps(kwargs['data'], ensure_ascii=False)
            body = body.encode('utf-8')
            kwargs['data'] = body

        kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        result_processor = kwargs.pop('result_processor', None)
        res = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise WeChatClientException(
                errcode=None,
                errmsg=None,
                client=self,
                request=reqe.request,
                response=reqe.response
            )

        return self._handle_result(
            res, method, url, result_processor, **kwargs
        )

    def _decode_result(self, res):
        res.encoding = 'utf-8'
        try:
            result = res.json()
        except (TypeError, ValueError):
            # Return origin response object if we can not decode it as JSON
            return res
        return result

    def _handle_result(self, res, method=None, url=None,
                       result_processor=None, **kwargs):
        if not isinstance(res, dict):
            # Dirty hack around asyncio based AsyncWeChatClient
            result = self._decode_result(res)
        else:
            result = res

        if not isinstance(result, dict):
            return result

        if 'base_resp' in result:
            # Different response in device APIs. Fuck tencent!
            result = result['base_resp']
        if 'errcode' in result:
            result['errcode'] = int(result['errcode'])

        if 'errcode' in result and result['errcode'] != 0:
            errcode = result['errcode']
            errmsg = result.get('errmsg', errcode)
            if errcode in (40001, 40014, 42001):
                # access_token expired, fetch a new one and retry request
                self.fetch_access_token()
                access_token = self.session.get(self.access_token_key)
                kwargs['params']['access_token'] = access_token
                return self._request(
                    method=method,
                    url_or_endpoint=url,
                    result_processor=result_processor,
                    **kwargs
                )
            elif errcode == 45009:
                # api freq out of limit
                raise APILimitedException(
                    errcode,
                    errmsg,
                    client=self,
                    request=res.request,
                    response=res
                )
            else:
                raise WeChatClientException(
                    errcode,
                    errmsg,
                    client=self,
                    request=res.request,
                    response=res
                )

        return result if not result_processor else result_processor(result)

    def get(self, url, **kwargs):
        return self._request(
            method='get',
            url_or_endpoint=url,
            **kwargs
        )

    _get = get

    def post(self, url, **kwargs):
        return self._request(
            method='post',
            url_or_endpoint=url,
            **kwargs
        )

    _post = post

    def _fetch_access_token(self, url, params):
        """ The real fetch access token """
        res = requests.get(
            url=url,
            params=params
        )
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise WeChatClientException(
                errcode=None,
                errmsg=None,
                client=self,
                request=reqe.request,
                response=reqe.response
            )
        result = res.json()
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatClientException(
                result['errcode'],
                result['errmsg'],
                client=self,
                request=res.request,
                response=res
            )

        expires_in = 7200
        if 'expires_in' in result:
            expires_in = result['expires_in']
        self.session.set(
            self.access_token_key,
            result['access_token'],
            expires_in
        )
        self.expires_at = int(time.time()) + expires_in
        return result

    def fetch_access_token(self):
        raise NotImplementedError()

    @property
    def access_token(self):
        """ WeChat access token """
        access_token = self.session.get(self.access_token_key)
        if access_token:
            if not self.expires_at:
                # user provided access_token, just return it
                return access_token

            timestamp = time.time()
            if self.expires_at - timestamp > 60:
                return access_token

        self.fetch_access_token()
        return self.session.get(self.access_token_key)
