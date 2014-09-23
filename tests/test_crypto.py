# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest

from wechatpy.enterprise.crypto import WeChatCrypto


class CryptoTestCase(unittest.TestCase):

    token = '123456'
    encoding_aes_key = 'kWxPEV2UEDyxWpmPdKC3F4dgPDmOvfKX1HGnEUDS1aR'
    corp_id = 'wx49f0ab532d5d035a'

    def test_check_signature_should_ok(self):
        signature = 'dd6b9c95b495b3f7e2901bfbc76c664930ffdb96'
        timestamp = '1411443780'
        nonce = '437374425'
        echo_str = '4ByGGj+sVCYcvGeQYhaKIk1o0pQRNbRjxybjTGblXrBaXlTXeOo1+bXFXDQQb1o6co6Yh9Bv41n7hOchLF6p+Q=='  # NOQA

        crypto = WeChatCrypto(self.token, self.encoding_aes_key, self.corp_id)
        echo_str = crypto.check_signature(
            signature,
            timestamp,
            nonce,
            echo_str
        )

    def test_check_signature_should_fail(self):
        from wechatpy.exceptions import InvalidSignatureException

        signature = 'dd6b9c95b495b3f7e2901bfbc76c664930ffdb96'
        timestamp = '1411443780'
        nonce = '437374424'
        echo_str = '4ByGGj+sVCYcvGeQYhaKIk1o0pQRNbRjxybjTGblXrBaXlTXeOo1+bXFXDQQb1o6co6Yh9Bv41n7hOchLF6p+Q=='  # NOQA

        crypto = WeChatCrypto(self.token, self.encoding_aes_key, self.corp_id)
        self.assertRaises(
            InvalidSignatureException,
            crypto.check_signature,
            signature, timestamp, nonce, echo_str
        )
