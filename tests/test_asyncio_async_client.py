# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import os
import sys

import pytest
import six
from six import StringIO
from six.moves.urllib.parse import urlparse
from httmock import urlmatch, HTTMock, response
from wechatpy._compat import json


pytestmark = pytest.mark.skipif(
    sys.version_info < (3, 4),
    reason='Python 3.4+ required'
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


def wechat_api_mock(client, method, url, *args, **kwargs):
    import asyncio
    import unittest.mock as mock
    from aiohttp.client_reqrep import ClientResponse

    def side_effect(*args, **kwargs):
        path = urlparse(url).path.replace('/cgi-bin/', '').replace('/', '_')
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
                content = f.read()
        except (IOError, ValueError) as e:
            content['errmsg'] = 'Loads fixture {0} failed, error: {1}'.format(
                res_file,
                e
            )
            content = json.dumps(content)
        if isinstance(content, six.text_type):
            content = content.encode('utf-8')

        future = asyncio.Future(loop=asyncio.get_event_loop())
        future.set_result(content)
        return future

    loop = asyncio.get_event_loop()

    connection = mock.Mock()
    resp = ClientResponse(method, url)
    resp.headers = {
        'CONTENT-TYPE': 'application/json;charset=utf-8'
    }
    resp._post_init(loop)
    resp._setup_connection(connection)

    content_mock = resp.content = mock.Mock()
    content_mock.read.side_effect = side_effect
    return resp


@pytest.fixture(autouse=True)
def map_request_to_json_file(monkeypatch):
    import asyncio
    from aiohttp.client import ClientSession

    monkeypatch.setattr(
        ClientSession,
        '_request',
        asyncio.coroutine(wechat_api_mock)
    )


@pytest.fixture()
def client():
    from wechatpy.client.async.asyncio import AsyncWeChatClient

    return AsyncWeChatClient(APPID, SECRET)


@pytest.mark.asyncio
def test_user_get_group_id(client):
    with HTTMock(access_token_mock):
        group_id = yield from client.user.get_group_id('123456')
    assert 102 == group_id


@pytest.mark.asyncio
def test_user_get(client):
    with HTTMock(access_token_mock):
        openid = 'o6_bmjrPTlm6_2sgVt7hMZOPfL2M'
        user = yield from client.user.get(openid)
    assert 'Band' == user['nickname']


@pytest.mark.asyncio
def test_upload_media(client):
    media_file = StringIO('nothing')
    with HTTMock(access_token_mock):
        media = yield from client.media.upload('image', media_file)
    assert 'image' == media['type']
    assert '12345678' == media['media_id']
