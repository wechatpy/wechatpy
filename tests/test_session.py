# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import os
import platform
import unittest

from httmock import urlmatch, HTTMock, response

from wechatpy import WeChatClient
from wechatpy.utils import json


_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_FIXTURE_PATH = os.path.join(_TESTS_PATH, 'fixtures')


@urlmatch(netloc=r'(.*\.)?api\.weixin\.qq\.com$')
def wechat_api_mock(url, request):
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
        print(e)
    return response(200, content, headers, request=request)


class WeChatSessionTestCase(unittest.TestCase):

    app_id = '123456'
    secret = '123456'

    def test_memory_session_storage_init(self):
        from wechatpy.session.memorystorage import MemoryStorage

        client = WeChatClient(self.app_id, self.secret)
        self.assertTrue(isinstance(client.session, MemoryStorage))

    def test_memory_session_storage_access_token(self):
        client = WeChatClient(self.app_id, self.secret)
        with HTTMock(wechat_api_mock):
            token = client.fetch_access_token()
            self.assertEqual('1234567890', token['access_token'])
            self.assertEqual(7200, token['expires_in'])
            self.assertEqual('1234567890', client.access_token)

    def test_redis_session_storage_init(self):
        from redis import Redis
        from wechatpy.session.redisstorage import RedisStorage

        redis = Redis()
        session = RedisStorage(redis)
        client = WeChatClient(self.app_id, self.secret, session=session)
        self.assertTrue(isinstance(client.session, RedisStorage))

    def test_redis_session_storage_access_token(self):
        from redis import Redis
        from wechatpy.session.redisstorage import RedisStorage

        redis = Redis()
        session = RedisStorage(redis)
        client = WeChatClient(self.app_id, self.secret, session=session)
        with HTTMock(wechat_api_mock):
            token = client.fetch_access_token()
            self.assertEqual('1234567890', token['access_token'])
            self.assertEqual(7200, token['expires_in'])
            self.assertEqual('1234567890', client.access_token)

    def test_memcached_storage_init(self):
        if platform.system() == 'Windows':
            return

        from pymemcache.client import Client
        from wechatpy.session.memcachedstorage import MemcachedStorage

        servers = ("127.0.0.1", 11211)
        memcached = Client(servers)
        session = MemcachedStorage(memcached)
        client = WeChatClient(self.app_id, self.secret, session=session)
        self.assertTrue(isinstance(client.session, MemcachedStorage))

    def test_memcached_storage_access_token(self):
        if platform.system() == 'Windows':
            return

        from pymemcache.client import Client
        from wechatpy.session.memcachedstorage import MemcachedStorage

        servers = ("127.0.0.1", 11211)
        memcached = Client(servers)
        session = MemcachedStorage(memcached)
        client = WeChatClient(self.app_id, self.secret, session=session)
        with HTTMock(wechat_api_mock):
            token = client.fetch_access_token()
            self.assertEqual('1234567890', token['access_token'])
            self.assertEqual(7200, token['expires_in'])
            self.assertEqual('1234567890', client.access_token)

    def test_shove_storage_init(self):
        from wechatpy.session.shovestorage import ShoveStorage

        uri = 'memory://'
        client = WeChatClient(self.app_id, self.secret, session=uri)
        self.assertTrue(isinstance(client.session, ShoveStorage))
        self.assertEqual('wechatpy', client.session.prefix)

    def test_shove_storage_init_with_prefix(self):
        from wechatpy.session.shovestorage import ShoveStorage

        uri = 'memory://?prefix=custom_prefix'
        client = WeChatClient(self.app_id, self.secret, session=uri)
        self.assertTrue(isinstance(client.session, ShoveStorage))
        self.assertEqual('custom_prefix', client.session.prefix)

    def test_shove_storage_access_token(self):
        uri = 'memory://'
        client = WeChatClient(self.app_id, self.secret, session=uri)
        with HTTMock(wechat_api_mock):
            token = client.fetch_access_token()
            self.assertEqual('1234567890', token['access_token'])
            self.assertEqual(7200, token['expires_in'])
            self.assertEqual('1234567890', client.access_token)
