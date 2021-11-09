# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class BaseWeChatCipher(object):

    def __init__(self, cipher):
        self.cipher = cipher

    def encrypt(self, plaintext):
        encryptor = self.cipher.encryptor()
        return encryptor.update(plaintext) + encryptor.finalize()

    def decrypt(self, ciphertext):
        decryptor = self.cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()


class WeChatCipher(BaseWeChatCipher):

    def __init__(self, key, iv=None):
        iv = iv or key[:16]
        super(WeChatCipher, self).__init__(
            Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
            )
        )


class AesEcbCipher(BaseWeChatCipher):

    def __init__(self, key):
        super(AesEcbCipher, self).__init__(
            Cipher(
                algorithms.AES(key),
                modes.ECB(),
            )
        )
