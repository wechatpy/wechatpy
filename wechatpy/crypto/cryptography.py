# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import string
import random
import struct
import socket
import base64

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from ..utils import to_text, to_binary
from .._compat import byte2int
from .pkcs7 import PKCS7Encoder


class BasePrpCrypto(object):

    def __init__(self, key):
        self.key = key
        self.mode = modes.CBC

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

        backend = default_backend()
        cipher = Cipher(
            algorithms.AES(self.key),
            self.mode(self.key[:16]),
            backend=backend
        )
        cryptor = cipher.encryptor()
        ct = cryptor.update(text) + cryptor.finalize()
        ciphertext = to_binary(ct)
        return base64.b64encode(ciphertext)

    def _decrypt(self, text, _id, exception=None):
        text = to_binary(text)
        backend = default_backend()
        cipher = Cipher(
            algorithms.AES(self.key),
            self.mode(self.key[:16]),
            backend=backend
        )
        cryptor = cipher.decryptor()
        decoded_text = base64.b64decode(text)
        plain_text = cryptor.update(decoded_text) + cryptor.finalize()
        padding = byte2int(plain_text, -1)
        content = plain_text[16:-padding]
        xml_length = socket.ntohl(struct.unpack(b'I', content[:4])[0])
        xml_content = to_text(content[4:xml_length + 4])
        from_id = to_text(content[xml_length + 4:])
        if from_id != _id:
            exception = exception or Exception
            raise exception()
        return xml_content
