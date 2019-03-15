# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from Crypto.Cipher import AES
import json


class WeChatCipher(object):

    def __init__(self, key):
        backend = default_backend()
        self.cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(key[:16]),
            backend=backend
        )

    def encrypt(self, plaintext):
        encryptor = self.cipher.encryptor()
        return encryptor.update(plaintext) + encryptor.finalize()

    def decrypt(self, ciphertext):
        decryptor = self.cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()


class WeChatWxaCipher(object):

    def __init__(self, key, iv):
        self.cipher = AES.new(key, AES.MODE_CBC, iv)

    def encrypt(self, plain_data):
        pass

    def decrypt(self, cipher_data):
        decrypted = json.loads(self._unpad(self.cipher.decrypt(cipher_data)))
        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]
