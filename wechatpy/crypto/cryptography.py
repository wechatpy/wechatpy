# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


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
