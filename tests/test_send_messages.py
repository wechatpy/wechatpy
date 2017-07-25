# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import unittest

from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage


class SendMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.client = WeChatClient('wx1234567887654321', 'secret')
        self.message = WeChatMessage(self.client)

    def test_get_subscribe_authorize_url(self):
        scene = 42
        template_id = 'some_long_id'
        redirect_url = 'https://mp.weixin.qq.com'
        reserved = 'random_string'
        url = self.message.get_subscribe_authorize_url(scene, template_id, redirect_url, reserved)
        base_url = ('https://mp.weixin.qq.com/mp/subscribemsg?action=get_confirm&appid={}&scene={}&template_id={}'
                    '&redirect_url=https%3A%2F%2Fmp.weixin.qq.com&reserved={}#wechat_redirect')
        expected_url = base_url.format(self.client.appid, scene, template_id, reserved)
        self.assertEqual(expected_url, url)
