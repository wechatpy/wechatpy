# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import json
import unittest

from httmock import urlmatch, HTTMock, response

from wechatpy import WeChatPay
from wechatpy.pay import dict_to_xml

_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_FIXTURE_PATH = os.path.join(_TESTS_PATH, 'fixtures', 'payment')


@urlmatch(netloc=r'(.*\.)?api\.mch\.weixin\.qq\.com$')
def wechat_api_mock(url, request):
    path = (url.path[1:] if url.path.startswith("/") else url.path).replace('/', '_')
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
    content_sign = content.pop("sign", "")
    content_xml = dict_to_xml(content, content_sign)
    return response(200, content_xml, headers, request=request)


class WeChatPayTestCase(unittest.TestCase):

    def setUp(self):
        self.client = WeChatPay(
            appid='abc1234',
            api_key='test123',
            mch_id='1192221',
            mch_cert='',
            mch_key='',
        )

    def test_apply_signing(self):
        response = self.client.withhold.apply_signing(
            plan_id='t1234',
            contract_code='w1111',
            contract_display_account='测试',
            notify_url=''
        )
        self.assertIn("base_url", response)
        self.assertIn("data", response)
        self.assertNotIn('nonce_str', response['data'])

    def test_query_signing(self):
        with HTTMock(wechat_api_mock):
            response = self.client.withhold.query_signing(
                contract_id='test1234'
            )
            self.assertEqual(response["result_code"], "SUCCESS")

    def test_apply_deduct(self):
        with HTTMock(wechat_api_mock):
            response = self.client.withhold.apply_deduct(
                body="测试商品",
                total_fee=999,
                contract_id='203',
                notify_url=''
            )
            self.assertEqual(response["result_code"], "SUCCESS")

    def test_query_order(self):
        with HTTMock(wechat_api_mock):
            response = self.client.withhold.query_order(
                out_trade_no='217752501201407033233368018'
            )
            self.assertEqual(response["result_code"], "SUCCESS")

    def test_apply_cancel_signing(self):
        with HTTMock(wechat_api_mock):
            response = self.client.withhold.apply_cancel_signing(
                plan_id='t1234',
                contract_code='w1111',
            )
            self.assertEqual(response["result_code"], "SUCCESS")
