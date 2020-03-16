# -*- coding: utf-8 -*-

from Crypto.Cipher import AES


class BaseWeChatCipher:
    def __init__(self, cipher):
        self.cipher = cipher

    def encrypt(self, plaintext):
        return self.cipher.encrypt(plaintext)

    def decrypt(self, ciphertext):
        return self.cipher.decrypt(ciphertext)


class WeChatCipher(BaseWeChatCipher):
    def __init__(self, key, iv=None):
        iv = iv or key[:16]
        super().__init__(AES.new(key, AES.MODE_CBC, iv))


class AesEcbCipher(BaseWeChatCipher):
    def __init__(self, key):
        super().__init__(AES.new(key, AES.MODE_ECB))
