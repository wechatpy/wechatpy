# -*- coding: utf-8 -*-

from wechatpy.utils import to_binary


class PKCS7Encoder:
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
        padding = decrypted[-1]
        if padding < 1 or padding > 32:
            padding = 0
        return decrypted[:-padding]
