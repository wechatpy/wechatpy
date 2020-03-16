# -*- coding: utf-8 -*-
"""
    wechatpy.crypto
    ~~~~~~~~~~~~~~~~

    This module provides some crypto tools for WeChat and WeChat work

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""

import json
import time
import base64
import hashlib

from wechatpy.utils import to_text, to_binary, WeChatSigner
from wechatpy.exceptions import (
    InvalidAppIdException,
    InvalidMchIdException,
    InvalidSignatureException,
)
from wechatpy.crypto.base import BasePrpCrypto, WeChatCipher, BaseRefundCrypto
from wechatpy.crypto.pkcs7 import PKCS7Encoder


def _get_signature(token, timestamp, nonce, encrypt):
    signer = WeChatSigner()
    signer.add_data(token, timestamp, nonce, encrypt)
    return signer.signature


class PrpCrypto(BasePrpCrypto):
    def encrypt(self, text, app_id):
        return self._encrypt(text, app_id)

    def decrypt(self, text, app_id):
        return self._decrypt(text, app_id, InvalidAppIdException)


class BaseWeChatCrypto:
    def __init__(self, token, encoding_aes_key, _id):
        encoding_aes_key = to_binary(encoding_aes_key + "=")
        self.key = base64.b64decode(encoding_aes_key)
        assert len(self.key) == 32
        self.token = token
        self._id = _id

    def _check_signature(self, signature, timestamp, nonce, echo_str, crypto_class=None):
        _signature = _get_signature(self.token, timestamp, nonce, echo_str)
        if _signature != signature:
            raise InvalidSignatureException()
        pc = crypto_class(self.key)
        return pc.decrypt(echo_str, self._id)

    def _encrypt_message(self, msg, nonce, timestamp=None, crypto_class=None):
        from wechatpy.replies import BaseReply

        xml = """<xml>
<Encrypt><![CDATA[{encrypt}]]></Encrypt>
<MsgSignature><![CDATA[{signature}]]></MsgSignature>
<TimeStamp>{timestamp}</TimeStamp>
<Nonce><![CDATA[{nonce}]]></Nonce>
</xml>"""
        if isinstance(msg, BaseReply):
            msg = msg.render()
        timestamp = timestamp or to_text(int(time.time()))
        pc = crypto_class(self.key)
        encrypt = to_text(pc.encrypt(msg, self._id))
        signature = _get_signature(self.token, timestamp, nonce, encrypt)
        return to_text(xml.format(encrypt=encrypt, signature=signature, timestamp=timestamp, nonce=nonce))

    def _decrypt_message(self, msg, signature, timestamp, nonce, crypto_class=None):
        if not isinstance(msg, dict):
            import xmltodict

            msg = xmltodict.parse(to_text(msg))["xml"]

        encrypt = msg["Encrypt"]
        _signature = _get_signature(self.token, timestamp, nonce, encrypt)
        if _signature != signature:
            raise InvalidSignatureException()
        pc = crypto_class(self.key)
        return pc.decrypt(encrypt, self._id)


class WeChatCrypto(BaseWeChatCrypto):
    def __init__(self, token, encoding_aes_key, app_id):
        super().__init__(token, encoding_aes_key, app_id)
        self.app_id = app_id

    def encrypt_message(self, msg, nonce, timestamp=None):
        return self._encrypt_message(msg, nonce, timestamp, PrpCrypto)

    def decrypt_message(self, msg, signature, timestamp, nonce):
        return self._decrypt_message(msg, signature, timestamp, nonce, PrpCrypto)


class WeChatWxaCrypto:
    def __init__(self, key, iv, app_id):
        self.cipher = WeChatCipher(base64.b64decode(key), base64.b64decode(iv))
        self.app_id = app_id

    def decrypt_message(self, msg):
        raw_data = base64.b64decode(msg)
        decrypted = self.cipher.decrypt(raw_data)
        plaintext = PKCS7Encoder.decode(decrypted)
        decrypted_msg = json.loads(to_text(plaintext))
        if decrypted_msg["watermark"]["appid"] != self.app_id:
            raise InvalidAppIdException()
        return decrypted_msg


class RefundCrypto(BaseRefundCrypto):
    def encrypt(self, text):
        return self._encrypt(text)

    def decrypt(self, text):
        return self._decrypt(text)


class WeChatRefundCrypto:
    def __init__(self, key):
        self.key = to_binary(hashlib.md5(to_binary(key)).hexdigest())
        assert len(self.key) == 32

    def _decrypt_message(self, msg, appid, mch_id, crypto_class=None):
        import xmltodict

        if not isinstance(msg, dict):
            msg = xmltodict.parse(to_text(msg))["xml"]

        req_info = msg["req_info"]
        if msg["appid"] != appid:
            raise InvalidAppIdException()
        if msg["mch_id"] != mch_id:
            raise InvalidMchIdException()
        pc = crypto_class(self.key)
        ret = pc.decrypt(req_info)
        return xmltodict.parse(to_text(ret))["root"]

    def decrypt_message(self, msg, appid, mch_id):
        return self._decrypt_message(msg, appid, mch_id, RefundCrypto)
