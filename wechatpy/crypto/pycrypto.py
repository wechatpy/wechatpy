# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from Crypto.Cipher import AES


class WeChatCipher(object):

    def __init__(self, key, iv=None):
        iv = iv or key[:16]
        self.cipher = AES.new(key, AES.MODE_CBC, iv)

    def encrypt(self, plaintext):
        return self.cipher.encrypt(plaintext)

    def decrypt(self, ciphertext):
        return self.cipher.decrypt(ciphertext)
