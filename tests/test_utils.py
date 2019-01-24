# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import unittest

import os

import pytest

from wechatpy.utils import ObjectDict, check_signature

_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_CERTS_PATH = os.path.join(_TESTS_PATH, 'certs')


def skip_if_no_cryptography():
    try:
        import cryptography  # NOQA
        return False
    except ImportError:
        return True


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

    @pytest.mark.skipif(skip_if_no_cryptography(), reason='cryptography not installed')
    def test_rsa_encrypt_decrypt(self):
        from wechatpy.pay.utils import rsa_encrypt, rsa_decrypt
        target_string = 'hello world'
        with open(os.path.join(_CERTS_PATH, 'rsa_public_key.pem'), 'rb') as public_fp, \
                open(os.path.join(_CERTS_PATH, 'rsa_private_key.pem'), 'rb') as private_fp:
            encrypted_string = rsa_encrypt(target_string, public_fp.read(), b64_encode=False)
            self.assertEqual(rsa_decrypt(encrypted_string, private_fp.read()), target_string.encode('utf-8'))
