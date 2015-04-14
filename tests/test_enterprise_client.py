# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import unittest

from httmock import urlmatch, HTTMock, response

from wechatpy.enterprise import WeChatClient
from wechatpy._compat import json


_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_FIXTURE_PATH = os.path.join(_TESTS_PATH, 'fixtures', 'enterprise')


@urlmatch(netloc=r'(.*\.)?qyapi\.weixin\.qq\.com$')
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
    except (IOError, ValueError):
        pass
    return response(200, content, headers, request=request)


class WeChatClientTestCase(unittest.TestCase):
    corp_id = '123456'
    secret = '123456'

    def setUp(self):
        self.client = WeChatClient(self.corp_id, self.secret)

    def test_fetch_access_token(self):
        with HTTMock(wechat_api_mock):
            token = self.client.fetch_access_token()
            self.assertEqual('1234567890', token['access_token'])
            self.assertEqual(7200, token['expires_in'])
            self.assertEqual('1234567890', self.client.access_token)

    def test_get_wechat_ips(self):
        with HTTMock(wechat_api_mock):
            res = self.client.misc.get_wechat_ips()
            self.assertEqual(['127.0.0.1'], res)

    def test_department_create(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.create('Test')
            self.assertEqual(2, res['id'])

    def test_department_update(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.update(2, 'Test 1')
            self.assertEqual(0, res['errcode'])

    def test_department_delete(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.delete(2)
            self.assertEqual(0, res['errcode'])

    def test_department_get(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.get()
            self.assertEqual(2, len(res))

    def test_department_get_users(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.get_users(2)
            self.assertEqual(1, len(res))

    def test_tag_create(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.create('test')
            self.assertEqual('1', res['tagid'])

    def test_tag_update(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.update(1, 'test')
            self.assertEqual(0, res['errcode'])

    def test_tag_delete(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.delete(1)
            self.assertEqual(0, res['errcode'])

    def test_tag_get_users(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.get_users(1)
            self.assertEqual(1, len(res['userlist']))
            self.assertEqual(1, len(res['partylist']))

    def test_tag_add_users(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.add_users(1, [1, 2, 3])
            self.assertEqual(0, res['errcode'])

    def test_tag_delete_users(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.delete_users(1, [1, 2, 3])
            self.assertEqual(0, res['errcode'])

    def test_tag_list(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.list()
            self.assertEqual(2, len(res))

    def test_batch_invite_user(self):
        with HTTMock(wechat_api_mock):
            res = self.client.batch.invite_user(
                'http://example.com',
                '123456',
                '123456',
                '123|456',
                [123, 456],
                (12, 34),
                ''
            )
            self.assertEqual(0, res['errcode'])

    def test_batch_sync_user(self):
        with HTTMock(wechat_api_mock):
            res = self.client.batch.sync_user(
                'http://example.com',
                '123456',
                '123456',
                '12345678'
            )
            self.assertEqual(0, res['errcode'])

    def test_batch_replace_user(self):
        with HTTMock(wechat_api_mock):
            res = self.client.batch.replace_user(
                'http://example.com',
                '123456',
                '123456',
                '12345678'
            )
            self.assertEqual(0, res['errcode'])

    def test_batch_replace_party(self):
        with HTTMock(wechat_api_mock):
            res = self.client.batch.replace_party(
                'http://example.com',
                '123456',
                '123456',
                '12345678'
            )
            self.assertEqual(0, res['errcode'])

    def test_batch_get_result(self):
        with HTTMock(wechat_api_mock):
            res = self.client.batch.get_result('123456')
            self.assertEqual(0, res['errcode'])
            self.assertEqual(1, res['status'])
