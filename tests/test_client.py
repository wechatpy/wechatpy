# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import unittest
import six
from httmock import urlmatch, HTTMock, response

from wechatpy import WeChatClient
from wechatpy._compat import json


_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_FIXTURE_PATH = os.path.join(_TESTS_PATH, 'fixtures')


@urlmatch(netloc=r'(.*\.)?api\.weixin\.qq\.com$')
def wechat_api_mock(url, request):
    path = url.path.replace('/cgi-bin/', '').replace('/', '_')
    res_file = os.path.join(_FIXTURE_PATH, '%s.json' % path)
    content = {
        'errcode': 99999,
        'errmsg': 'can not find fixture'
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        with open(res_file) as f:
            content = json.loads(f.read())
    except (IOError, OSError):
        pass
    return response(200, content, headers, request=request)


class WeChatClientTestCase(unittest.TestCase):

    app_id = '123456'
    secret = '123456'

    def setUp(self):
        self.client = WeChatClient(self.app_id, self.secret)

    def test_fetch_access_token(self):
        with HTTMock(wechat_api_mock):
            token = self.client.fetch_access_token()
            self.assertEqual('1234567890', token['access_token'])
            self.assertEqual(7200, token['expires_in'])
            self.assertEqual('1234567890', self.client.access_token)

    def test_upload_media(self):
        media_file = six.StringIO('nothing')
        with HTTMock(wechat_api_mock):
            media = self.client.upload_media('image', media_file)
            self.assertEqual('image', media['type'])
            self.assertEqual('12345678', media['media_id'])

    def test_create_group(self):
        with HTTMock(wechat_api_mock):
            group = self.client.create_group('test')
            self.assertEqual(1, group['group']['id'])
            self.assertEqual('test', group['group']['name'])
