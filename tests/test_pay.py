# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest


class WeChatPayTestCase(unittest.TestCase):

    def test_calculate_signature(self):
        from wechatpy.pay import calculate_signature

        api_key = '192006250b4c09247ec02edce69f6a2d'
        params = {
            'test1': 'test1',
            'test2': 'test2',
        }
        expected = b'1E3A8D73B5A4AEE787C0F68B5DAB8520'
        sign = calculate_signature(params, api_key)
        self.assertEqual(expected, sign)
