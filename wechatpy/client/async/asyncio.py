# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
import asyncio
import aiohttp

from wechatpy.client import WeChatClient


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

        # 群发消息上传视频接口地址 HTTPS 证书错误，暂时忽略证书验证
        if url.startswith('https://file.api.weixin.qq.com'):
            kwargs['verify'] = False

        if 'params' not in kwargs:
            kwargs['params'] = {}
        if isinstance(kwargs['params'], dict) and \
                'access_token' not in kwargs['params']:
            kwargs['params']['access_token'] = self.access_token

        data = kwargs.get('data')
        files = kwargs.get('files')
        if files:
            # data must be dict
            assert isinstance(data, dict), 'data must be a dict'
            data.update(files)
        else:
            if isinstance(data, dict):
                body = json.dumps(kwargs['data'], ensure_ascii=False)
            else:
                body = data
            kwargs['data'] = body

        # kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        result_processor = kwargs.pop('result_processor', None)
        res = yield from aiohttp.request(
            method=method,
            url=url,
            **kwargs
        )
        # TODO Exception handling
        result = yield from self._handle_result(
            res, method, url, result_processor, **kwargs
        )
        return result

    def _decode_result(self, res):
        try:
            result = yield from res.json()
        except (TypeError, ValueError):
            # Return origin response object if we can not decode it as JSON
            return res
        return result


class AsyncWeChatClient(AsyncClientMixin, WeChatClient):
    pass
