# -*- coding: utf-8 -*-

import struct
import socket
import base64

from wechatpy.utils import to_text, to_binary, random_string
from wechatpy.crypto.pkcs7 import PKCS7Encoder

try:
    from wechatpy.crypto.cryptography import WeChatCipher, AesEcbCipher
except ImportError:
    try:
        from wechatpy.crypto.pycrypto import WeChatCipher, AesEcbCipher
    except ImportError:
        raise Exception("You must install either cryptography or pycryptodome!")


class BasePrpCrypto:
    def __init__(self, key):
        self.cipher = WeChatCipher(key)

    def get_random_string(self):
        return random_string(16)

    def _encrypt(self, text, _id):
        text = to_binary(text)
        tmp_list = []
        tmp_list.append(to_binary(self.get_random_string()))
        length = struct.pack(b"I", socket.htonl(len(text)))
        tmp_list.append(length)
        tmp_list.append(text)
        tmp_list.append(to_binary(_id))

        text = b"".join(tmp_list)
        text = PKCS7Encoder.encode(text)

        ciphertext = to_binary(self.cipher.encrypt(text))
        return base64.b64encode(ciphertext)

    def _decrypt(self, text, _id, exception=None):
        text = to_binary(text)
        plain_text = self.cipher.decrypt(base64.b64decode(text))
        padding = plain_text[-1]
        content = plain_text[16:-padding]
        xml_length = socket.ntohl(struct.unpack(b"I", content[:4])[0])
        xml_content = to_text(content[4 : xml_length + 4])
        from_id = to_text(content[xml_length + 4 :])
        if from_id != _id:
            exception = exception or Exception
            raise exception()
        return xml_content


class BaseRefundCrypto:
    def __init__(self, key):
        self.cipher = AesEcbCipher(key)

    def _encrypt(self, text):
        text = to_binary(text)
        text = PKCS7Encoder.encode(text)

        ciphertext = to_binary(self.cipher.encrypt(text))
        return base64.b64encode(ciphertext)

    def _decrypt(self, text, exception=None):
        text = to_binary(text)
        plain_text = self.cipher.decrypt(base64.b64decode(text))
        padding = plain_text[-1]
        content = plain_text[:-padding]
        return content
