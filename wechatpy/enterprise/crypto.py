from __future__ import absolute_import, unicode_literals
import time
import string
import random
import hashlib
import base64
import struct
import socket

import six
# pycrypto
from Crypto.Cipher import AES

from ..utils import to_binary, to_text, XMLDict
from .._compat import byte2int
from ..exceptions import InvalidSignatureException
from .exceptions import InvalidCorpIdException


def get_sha1(token, timestamp, nonce, encrypt):
    sort_list = [token, timestamp, nonce, to_text(encrypt)]
    sort_list.sort()
    sort_str = to_binary(''.join(sort_list))
    sha1 = hashlib.sha1()
    sha1.update(sort_str)
    return sha1.hexdigest()


class PKCS7Encoder(object):
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
        padding = byte2int(decrypted, -1)
        if padding < 1 or padding > 32:
            padding = 0
        return decrypted[:-padding]


class PrpCrypto(object):

    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    def get_random_string(self):
        rule = string.ascii_letters + string.digits
        rand_list = random.sample(rule, 16)
        return ''.join(rand_list)

    def encrypt(self, text, corp_id):
        text = to_binary(text)
        tmp_list = []
        tmp_list.append(to_binary(self.get_random_string()))
        length = struct.pack(b'I', socket.htonl(len(text)))
        tmp_list.append(length)
        tmp_list.append(text)
        tmp_list.append(to_binary(corp_id))

        text = b''.join(tmp_list)
        text = PKCS7Encoder.encode(text)

        cryptor = AES.new(self.key, self.mode, self.key[:16])
        ciphertext = to_binary(cryptor.encrypt(text))
        return base64.b64encode(ciphertext)

    def decrypt(self, text, corp_id):
        text = to_binary(text)
        cryptor = AES.new(self.key, self.mode, self.key[:16])
        plain_text = cryptor.decrypt(base64.b64decode(text))
        padding = byte2int(plain_text, -1)
        content = plain_text[16:-padding]
        xml_length = socket.ntohl(struct.unpack(b'I', content[:4])[0])
        xml_content = to_text(content[4:xml_length + 4])
        from_corp_id = to_text(content[xml_length + 4:])
        if from_corp_id != corp_id:
            raise InvalidCorpIdException()
        return xml_content


class WeChatCrypto(object):

    def __init__(self, token, encoding_aes_key, corp_id):
        encoding_aes_key = to_binary(encoding_aes_key + '=')
        self.key = base64.b64decode(encoding_aes_key)
        assert len(self.key) == 32
        self.token = token
        self.corp_id = corp_id

    def check_signature(self, signature, timestamp, nonce, echo_str):
        _signature = get_sha1(self.token, timestamp, nonce, echo_str)
        if _signature != signature:
            raise InvalidSignatureException()
        pc = PrpCrypto(self.key)
        return pc.decrypt(echo_str, self.corp_id)

    def encrypt_message(self, msg, nonce, timestamp=None):
        from ..replies import BaseReply

        xml = """<xml>
<Encrypt><![CDATA[{encrypt}]]></Encrypt>
<MsgSignature><![CDATA[{signature}]]></MsgSignature>
<TimeStamp>{timestamp}</TimeStamp>
<Nonce><![CDATA[{nonce}]]></Nonce>
</xml>"""
        if isinstance(msg, BaseReply):
            msg = msg.render()
        timestamp = timestamp or to_binary(int(time.time()))
        pc = PrpCrypto(self.key)
        encrypt = to_text(pc.encrypt(msg, self.corp_id))
        signature = get_sha1(self.token, timestamp, nonce, encrypt)
        return to_text(xml.format(
            encrypt=encrypt,
            signature=signature,
            timestamp=timestamp,
            nonce=nonce
        ))

    def decrypt_message(self, msg, signature, timestamp, nonce):
        if isinstance(msg, six.string_types):
            from xml.etree import ElementTree

            parser = ElementTree.fromstring(to_text(msg).encode('utf-8'))
            msg = XMLDict(parser)
        encrypt = msg['Encrypt']
        _signature = get_sha1(self.token, timestamp, nonce, encrypt)
        if _signature != signature:
            raise InvalidSignatureException()
        pc = PrpCrypto(self.key)
        xml = pc.decrypt(encrypt, self.corp_id)
        parser = ElementTree.fromstring(to_text(xml).encode('utf-8'))
        message = dict((child.tag, to_text(child.text)) for child in parser)
        return message
