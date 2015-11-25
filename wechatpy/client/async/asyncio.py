# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
import asyncio

import aiohttp
from aiohttp.errors import ClientError

from wechatpy.client import WeChatClient
from wechatpy.exceptions import WeChatClientException


class AsyncClientMixin(object):
    """
    基于 asyncio 和 aiohttp 的异步主动调用客户端实现 mixin

    主要是替换了使用 ``requests`` 实现同步客户端的 ``_request`` 和
     `` _decode_result`` 方法以适应 aiohttp 和 requests 的不同。
    """
    @asyncio.coroutine
    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = '{base}{endpoint}'.format(
                base=api_base_url,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        if 'params' not in kwargs:
            kwargs['params'] = {}
        if isinstance(kwargs['params'], dict) and \
                'access_token' not in kwargs['params']:
            kwargs['params']['access_token'] = self.access_token

        data = kwargs.get('data', {})
        files = kwargs.pop('files', {})
        if files:
            # data must be dict
            assert isinstance(data, dict), 'data must be a dict'
            data.update(files)
        else:
            if isinstance(data, dict):
                body = json.dumps(data, ensure_ascii=False)
            else:
                body = data
            kwargs['data'] = body

        result_processor = kwargs.pop('result_processor', None)
        timeout = kwargs.pop('timeout', self.timeout)
        try:
            if timeout is None:
                res = yield from aiohttp.request(
                    method=method,
                    url=url,
                    **kwargs
                )
            else:
                res_future = aiohttp.request(
                    method=method,
                    url=url,
                    **kwargs
                )
                res = yield from asyncio.wait_for(res_future, timeout)
                # reset kwargs for later retrying
                kwargs['timeout'] = timeout
                kwargs['files'] = files
        except ClientError:
            raise WeChatClientException(
                errcode=None,
                errmsg=None,
                client=self,
            )
        # dirty hack
        res = yield from self._decode_result(res)
        return self._handle_result(
            res, method, url, result_processor, **kwargs
        )

    def _decode_result(self, res):
        if isinstance(res, dict):
            return res
        try:
            result = yield from res.json()
        except (TypeError, ValueError):
            # Return origin response object if we can not decode it as JSON
            return res
        return result


class AsyncWeChatClient(AsyncClientMixin, WeChatClient):
    pass
