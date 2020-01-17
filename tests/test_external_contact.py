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

    def test_ec_addcorptag(self):
        tags = [{
            "name": "大鸟"
        },
            {
                "name": "小菜"
            }]
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.add_corp_tag(None, "开发1组", 1, tags=tags)
        self.assertEqual(0, res['errcode'])

    def test_ec_edit_corp_tag(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.edit_corp_tag('etm7wjCgAA-DYuu_JX8DrN0EUfa1ycDw', '开发2组', 1)
        self.assertEqual(0, res['errcode'])

    def test_ec_del_corp_tag(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.del_corp_tag(tag_id=['etm7wjCgAAADvErs_p_VhdNdN6-i2zAg'])
        self.assertEqual(0, res['errcode'])

    def test_ec_mark_tag(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.mark_tag('zm', 'wmm7wjCgAAkLAv_eiVt53eBokOC3_Tww',
                                                        add_tag=['etm7wjCgAAD5hhvyfhPUpBbCs0CYuQMg'])
        self.assertEqual(0, res['errcode'])
