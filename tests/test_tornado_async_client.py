# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import os
import sys

import pytest
from six import StringIO
from six.moves.urllib.parse import urlparse
from httmock import urlmatch, HTTMock, response
from wechatpy._compat import json


pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7),
    reason='requires Python 2.7'
)

_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_FIXTURE_PATH = os.path.join(_TESTS_PATH, 'fixtures')
APPID = '123456'
SECRET = '123456'


@urlmatch(netloc=r'(.*\.)?api\.weixin\.qq\.com$')
def access_token_mock(url, request):
    path = url.path.replace('/cgi-bin/', '').replace('/', '_')
    if path.startswith('_'):
        path = path[1:]
    res_file = os.path.join(_FIXTURE_PATH, '%s.json' % path)
    content = {
        'errcode': 99999,
        'errmsg': 'can not find fixture %s' % res_file,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        with open(res_file, 'rb') as f:
            content = json.loads(f.read().decode('utf-8'))
    except (IOError, ValueError) as e:
        content['errmsg'] = 'Loads fixture {0} failed, error: {1}'.format(
            res_file,
            e
        )
    return response(200, content, headers, request=request)


def wechat_api_mock(client, request, *args, **kwargs):
    from tornado.concurrent import Future
    from tornado.httpclient import HTTPResponse

    url = urlparse(request.url)
    path = url.path.replace('/cgi-bin/', '').replace('/', '_')
    if path.startswith('_'):
        path = path[1:]
    res_file = os.path.join(_FIXTURE_PATH, '%s.json' % path)
    content = {
        'errcode': 99999,
        'errmsg': 'can not find fixture %s' % res_file,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        with open(res_file, 'rb') as f:
            content = f.read().decode('utf-8')
    except (IOError, ValueError) as e:
        content['errmsg'] = 'Loads fixture {0} failed, error: {1}'.format(
            res_file,
            e
        )
        content = json.dumps(content)

    buffer = StringIO(content)
    resp = HTTPResponse(
        request,
        200,
        headers=headers,
        buffer=buffer,
    )
    future = Future()
    future.set_result(resp)
    return future


@pytest.fixture(autouse=True)
def map_request_to_json_file(monkeypatch):
    from tornado.httpclient import AsyncHTTPClient

    monkeypatch.setattr(AsyncHTTPClient, 'fetch', wechat_api_mock)


from wechatpy.client.async.tornado import AsyncWeChatClient


@pytest.mark.gen_test
def test_user_get_group_id(io_loop):
    with HTTMock(access_token_mock):
        client = AsyncWeChatClient(APPID, SECRET)
        group_id = yield client.user.get_group_id('123456')
        assert 102 == group_id
