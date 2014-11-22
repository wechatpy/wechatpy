# -*- coding: utf-8 -*-
"""
    wechatpy.crypto
    ~~~~~~~~~~~~~~~~

    This module provides some crypto tools for WeChat and WeChat enterprise

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import time
import string
import random
import struct
import socket
import base64

import six
# pycrypto
from Crypto.Cipher import AES

from .utils import to_text, to_binary, WeChatSigner
from ._compat import byte2int
from .exceptions import InvalidAppIdException, InvalidSignatureException


def _get_signature(token, timestamp, nonce, encrypt):
    signer = WeChatSigner()
    signer.add_data(token, timestamp, nonce, encrypt)
    return signer.signature


class PKCS7Encoder(object):
    block_size = 32

    @classmethod
    def encode(cls, text):
        length = len(text)
        padding_count = cls.block_size - length % cls.block_size
        if padding_count == 0:
            padding_count = cls.block_size
        padding = to_binary(chr(padding_count))
        return text + padding * padding_count

    @classmethod
    def decode(cls, decrypted):
        padding = byte2int(decrypted, -1)
        if padding < 1 or padding > 32:
            padding = 0
        return decrypted[:-padding]


class BasePrpCrypto(object):

    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    def get_random_string(self):
        rule = string.ascii_letters + string.digits
        rand_list = random.sample(rule, 16)
        return ''.join(rand_list)

    def _encrypt(self, text, _id):
        text = to_binary(text)
        tmp_list = []
        tmp_list.append(to_binary(self.get_random_string()))
        length = struct.pack(b'I', socket.htonl(len(text)))
        tmp_list.append(length)
        tmp_list.append(text)
        tmp_list.append(to_binary(_id))

        text = b''.join(tmp_list)
        text = PKCS7Encoder.encode(text)

        cryptor = AES.new(self.key, self.mode, self.key[:16])
        ciphertext = to_binary(cryptor.encrypt(text))
        return base64.b64encode(ciphertext)

    def _decrypt(self, text, _id, exception=None):
        text = to_binary(text)
        cryptor = AES.new(self.key, self.mode, self.key[:16])
        plain_text = cryptor.decrypt(base64.b64decode(text))
        padding = byte2int(plain_text, -1)
        content = plain_text[16:-padding]
        xml_length = socket.ntohl(struct.unpack(b'I', content[:4])[0])
        xml_content = to_text(content[4:xml_length + 4])
        from_id = to_text(content[xml_length + 4:])
        if from_id != _id:
            exception = exception or Exception
            raise exception()
        return xml_content


class PrpCrypto(BasePrpCrypto):

    def encrypt(self, text, app_id):
        return self._encrypt(text, app_id)

    def decrypt(self, text, app_id):
        return self._decrypt(text, app_id, InvalidAppIdException)


class BaseWeChatCrypto(object):

    def __init__(self, token, encoding_aes_key, _id):
        encoding_aes_key = to_binary(encoding_aes_key + '=')
        self.key = base64.b64decode(encoding_aes_key)
        assert len(self.key) == 32
        self.token = token
        self._id = _id

    def _check_signature(self,
                         signature,
                         timestamp,
                         nonce,
                         echo_str,
                         crypto_class=None):
        _signature = _get_signature(self.token, timestamp, nonce, echo_str)
        if _signature != signature:
            raise InvalidSignatureException()
        pc = crypto_class(self.key)
        return pc.decrypt(echo_str, self._id)

    def _encrypt_message(self,
                         msg,
                         nonce,
                         timestamp=None,
                         crypto_class=None):
        from .replies import BaseReply

        xml = """<xml>
<Encrypt><![CDATA[{encrypt}]]></Encrypt>
<MsgSignature><![CDATA[{signature}]]></MsgSignature>
<TimeStamp>{timestamp}</TimeStamp>
<Nonce><![CDATA[{nonce}]]></Nonce>
</xml>"""
        if isinstance(msg, BaseReply):
            msg = msg.render()
        timestamp = timestamp or to_binary(int(time.time()))
        pc = crypto_class(self.key)
        encrypt = to_text(pc.encrypt(msg, self._id))
        signature = _get_signature(self.token, timestamp, nonce, encrypt)
        return to_text(xml.format(
            encrypt=encrypt,
            signature=signature,
            timestamp=timestamp,
            nonce=nonce
        ))

    def _decrypt_message(self,
                         msg,
                         signature,
                         timestamp,
                         nonce,
                         crypto_class=None):
        if isinstance(msg, six.string_types):
            import xmltodict

            msg = xmltodict.parse(to_text(msg))['xml']

        encrypt = msg['Encrypt']
        _signature = _get_signature(self.token, timestamp, nonce, encrypt)
        if _signature != signature:
            raise InvalidSignatureException()
        pc = crypto_class(self.key)
        return pc.decrypt(encrypt, self._id)


class WeChatCrypto(BaseWeChatCrypto):

    def __init__(self, token, encoding_aes_key, app_id):
        super(WeChatCrypto, self).__init__(token, encoding_aes_key, app_id)
        self.app_id = app_id

    def encrypt_message(self, msg, nonce, timestamp=None):
        return self._encrypt_message(msg, nonce, timestamp, PrpCrypto)

    def decrypt_message(self, msg, signature, timestamp, nonce):
        return self._decrypt_message(
            msg,
            signature,
            timestamp,
            nonce,
            PrpCrypto
        )
