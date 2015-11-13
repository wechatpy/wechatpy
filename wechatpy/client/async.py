# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from six.moves.urllib.parse import urlencode
from tornado.gen import coroutine, Return
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from wechatpy._compat import json
from wechatpy.utils import to_binary


class AsyncClientMixin(object):

    @coroutine
    def _request(self, method, url_or_endpoint, **kwargs):
        http_client = AsyncHTTPClient()
        if not url_or_endpoint.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = '{base}{endpoint}'.format(
                base=api_base_url,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        headers = {}
        params = kwargs.pop('params', {})
        if 'access_token' not in params:
            kwargs['params']['access_token'] = self.access_token

        params = urlencode(dict((k, to_binary(v)) for k, v in params.items()))
        url = '{0}?{1}'.format(url, params)

        data = kwargs.get('data')
        files = kwargs.get('files')
        if files:
            from requests.models import RequestEncodingMixin
            from requests.utils import super_len

            body, content_type = RequestEncodingMixin._encode_files(
                files,
                data
            )
            headers['Content-Type'] = content_type
            headers['Content-Length'] = super_len(body)
        else:
            if isinstance(data, dict):
                body = json.dumps(kwargs['data'], ensure_ascii=False)
                body = body.encode('utf-8')
            else:
                body = data

        req = HTTPRequest(
            url=url,
            method=method,
            headers=headers,
            body=body,
        )
        res = yield http_client.fetch(req)
        if res.error is not None:
            res.rethrow()

        result = self._handle_result(res, method, url, **kwargs)
        raise Return(result)

    def _decode_result(res, method, url, **kwargs):
        try:
            result = json.loads(res.body)
        except (TypeError, ValueError):
            # Return origin response object if we can not decode it as JSON
            return res
        return result
