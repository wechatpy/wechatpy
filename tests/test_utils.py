# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest

from wechatpy.utils import ObjectDict, check_signature


class UtilityTestCase(unittest.TestCase):

    def test_object_dict(self):
        obj = ObjectDict()
        self.assertTrue(obj.xxx is None)
        obj.xxx = 1
        self.assertEqual(1, obj.xxx)

    def test_check_signature_should_ok(self):
        token = 'test'
        signature = 'f21891de399b4e33a1a93c9a7b8a8fffb5a443ff'
        timestamp = '1410685589'
        nonce = 'test'
        check_signature(token, signature, timestamp, nonce)

    def test_check_signature_should_fail(self):
        from wechatpy.exceptions import InvalidSignatureException

        token = 'test'
        signature = 'f21891de399b4e33a1a93c9a7b8a8fffb5a443fe'
        timestamp = '1410685589'
        nonce = 'test'
        self.assertRaises(
            InvalidSignatureException,
            check_signature,
            token, signature, timestamp, nonce
        )

    def test_wechat_card_signer(self):
        from wechatpy.utils import WeChatSigner

        signer = WeChatSigner()
        signer.add_data('789')
        signer.add_data('456')
        signer.add_data('123')
        signature = signer.signature

        self.assertEqual('f7c3bc1d808e04732adf679965ccc34ca7ae3441', signature)
