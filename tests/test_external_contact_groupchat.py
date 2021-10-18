# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import unittest

from httmock import urlmatch, HTTMock, response
from wechatpy.enterprise import WeChatClient
from wechatpy.utils import json

_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_FIXTURE_PATH = os.path.join(_TESTS_PATH, 'fixtures', 'enterprise')


@urlmatch(netloc=r'(.*\.)?qyapi\.weixin\.qq\.com$')
def wechat_api_mock(url, request):
    path = url.path.replace('/cgi-bin/', '').replace('/', '_')
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


class WeChatClientTestCase(unittest.TestCase):
    app_id = '123456'
    secret = '123456'

    def setUp(self):
        self.client = WeChatClient(self.app_id, self.secret)

    def test_ec_group_chat_list_all(self):
        with HTTMock(wechat_api_mock):
            groups = list(self.client.external_contact_group_chat.list_all())
            self.assertEqual(2, len(groups))

    def test_ec_group_chat_get(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact_group_chat.get('wrOgQhDgAAMYQiS5ol9G7gK9JVAAAA')

        self.assertEqual(0, res['errcode'])

    def test_ec_group_chat_statistic(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact_group_chat.statistic(
                1600272000,
                1600444800,
                owner_userid_list=["zhangsan"]
            )

        self.assertEqual(0, res['errcode'])
