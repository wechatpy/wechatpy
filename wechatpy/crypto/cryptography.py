# -*- coding: utf-8 -*-

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class BaseWeChatCipher:
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
        backend = default_backend()
        super().__init__(Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend))


class AesEcbCipher(BaseWeChatCipher):
    def __init__(self, key):
        backend = default_backend()
        super().__init__(Cipher(algorithms.AES(key), modes.ECB(), backend=backend))
