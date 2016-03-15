# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import struct
import socket
import base64

from wechatpy.utils import to_text, to_binary, random_string, byte2int
from wechatpy.crypto.pkcs7 import PKCS7Encoder
try:
    from wechatpy.crypto.cryptography import WeChatCipher
except ImportError:
    try:
        from wechatpy.crypto.pycrypto import WeChatCipher
    except ImportError:
        raise Exception('You must install either cryptography or PyCrypto!')


class BasePrpCrypto(object):

    def __init__(self, key):
        self.cipher = WeChatCipher(key)

    def get_random_string(self):
        return random_string(16)

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

        ciphertext = to_binary(self.cipher.encrypt(text))
        return base64.b64encode(ciphertext)

    def _decrypt(self, text, _id, exception=None):
        text = to_binary(text)
        plain_text = self.cipher.decrypt(base64.b64decode(text))
        padding = byte2int(plain_text[-1])
        content = plain_text[16:-padding]
        xml_length = socket.ntohl(struct.unpack(b'I', content[:4])[0])
        xml_content = to_text(content[4:xml_length + 4])
        from_id = to_text(content[xml_length + 4:])
        if from_id != _id:
            exception = exception or Exception
            raise exception()
        return xml_content
