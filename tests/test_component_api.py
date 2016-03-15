# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import unittest

from httmock import urlmatch, HTTMock, response

from wechatpy.component import WeChatComponent
from wechatpy.utils import json


_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_FIXTURE_PATH = os.path.join(_TESTS_PATH, 'fixtures', 'component')


@urlmatch(netloc=r'(.*\.)?api\.weixin\.qq\.com$')
def wechat_api_mock(url, request):
    path = url.path.replace('/cgi-bin/component/', '').replace('/', '_')
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
    except (IOError, ValueError):
        pass
    return response(200, content, headers, request=request)


class WeChatComponentTestCase(unittest.TestCase):
    app_id = '123456'
    app_secret = '123456'
    token = 'sdfusfsssdc'
    encoding_aes_key = 'yguy3495y79o34vod7843933902h9gb2834hgpB90rg'

    def setUp(self):
        self.client = WeChatComponent(
            self.app_id, self.app_secret, self.token, self.encoding_aes_key)

    def test_fetch_access_token(self):
        with HTTMock(wechat_api_mock):
            token = self.client.fetch_access_token()
            self.assertEqual('1234567890', token['component_access_token'])
            self.assertEqual(7200, token['expires_in'])
            self.assertEqual('1234567890', self.client.access_token)

    def test_create_preauthcode(self):
        with HTTMock(wechat_api_mock):
            result = self.client.create_preauthcode()
            self.assertEqual('1234567890', result['pre_auth_code'])
            self.assertEqual(600, result['expires_in'])

    def test_query_auth(self):
        authorization_code = '1234567890'
        with HTTMock(wechat_api_mock):
            result = self.client.query_auth(authorization_code)
            self.assertEqual(
                'wxf8b4f85f3a794e77',
                result['authorization_info']['authorizer_appid']
            )

    def test_refresh_authorizer_token(self):
        appid = 'appid'
        refresh_token = 'refresh_token'
        with HTTMock(wechat_api_mock):
            result = self.client.refresh_authorizer_token(appid, refresh_token)
            self.assertEqual('1234567890', result['authorizer_access_token'])
            self.assertEqual('123456789', result['authorizer_refresh_token'])
            self.assertEqual(7200, result['expires_in'])

    def test_get_authorizer_info(self):
        authorizer_appid = 'wxf8b4f85f3a794e77'
        with HTTMock(wechat_api_mock):
            result = self.client.get_authorizer_info(authorizer_appid)
            self.assertEqual('paytest01', result['authorizer_info']['alias'])

    def test_get_authorizer_option(self):
        with HTTMock(wechat_api_mock):
            appid = 'wxf8b4f85f3a794e77'
            result = self.client.get_authorizer_option(appid, 'voice_recognize')
            self.assertEqual('voice_recognize', result['option_name'])
            self.assertEqual('1', result['option_value'])

    def test_set_authorizer_option(self):
        with HTTMock(wechat_api_mock):
            appid = 'wxf8b4f85f3a794e77'
            result = self.client.set_authorizer_option(
                appid, 'voice_recognize', '0'
            )
            self.assertEqual(0, result['errcode'])
