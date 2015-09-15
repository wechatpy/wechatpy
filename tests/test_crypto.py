# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest

import xmltodict

from wechatpy.enterprise import crypto as _crypto
from wechatpy.enterprise.crypto import WeChatCrypto


class PrpCryptoMock(_crypto.PrpCrypto):

    def get_random_string(self):
        return '1234567890123456'


class CryptoTestCase(unittest.TestCase):

    token = '123456'
    encoding_aes_key = 'kWxPEV2UEDyxWpmPdKC3F4dgPDmOvfKX1HGnEUDS1aR'
    corp_id = 'wx49f0ab532d5d035a'

    def test_check_signature_should_ok(self):
        signature = 'dd6b9c95b495b3f7e2901bfbc76c664930ffdb96'
        timestamp = '1411443780'
        nonce = '437374425'
        echo_str = '4ByGGj+sVCYcvGeQYhaKIk1o0pQRNbRjxybjTGblXrBaXlTXeOo1+bXFXDQQb1o6co6Yh9Bv41n7hOchLF6p+Q=='  # NOQA

        crypto = WeChatCrypto(self.token, self.encoding_aes_key, self.corp_id)
        echo_str = crypto.check_signature(
            signature,
            timestamp,
            nonce,
            echo_str
        )

    def test_check_signature_should_fail(self):
        from wechatpy.exceptions import InvalidSignatureException

        signature = 'dd6b9c95b495b3f7e2901bfbc76c664930ffdb96'
        timestamp = '1411443780'
        nonce = '437374424'
        echo_str = '4ByGGj+sVCYcvGeQYhaKIk1o0pQRNbRjxybjTGblXrBaXlTXeOo1+bXFXDQQb1o6co6Yh9Bv41n7hOchLF6p+Q=='  # NOQA

        crypto = WeChatCrypto(self.token, self.encoding_aes_key, self.corp_id)
        self.assertRaises(
            InvalidSignatureException,
            crypto.check_signature,
            signature, timestamp, nonce, echo_str
        )

    def test_encrypt_message(self):
        origin_crypto = _crypto.PrpCrypto
        _crypto.PrpCrypto = PrpCryptoMock

        nonce = '461056294'
        timestamp = '1411525903'
        reply = """<xml>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[test]]></Content>
<FromUserName><![CDATA[wx49f0ab532d5d035a]]></FromUserName>
<ToUserName><![CDATA[messense]]></ToUserName>
<AgentID>1</AgentID>
<CreateTime>1411525903</CreateTime>
</xml>"""

        expected = """<xml>
<Encrypt><![CDATA[9s4gMv99m88kKTh/H8IdkOiMg6bisoy3ypwy9H4hvSPe9nsGaqyw5hhSjdYbcrKk+j3nba4HMOTzHrluLBYqxgNcBqGsL8GqxlhZgURnAtObvesEl5nZ+uBE8bviY0LWke8Zy9V/QYKxNV2FqllNXcfmstttyIkMKCCmVbCFM2JTF5wY0nFhHZSjPUL2Q1qvSUCUld+/WIXrx0oyKQmpB6o8NRrrNrsDf03oxI1p9FxUgMnwKKZeOA/uu+2IEvEBtb7muXsVbwbgX05UPPJvFurDXafG0RQyPR+mf1nDnAtQmmNOuiR5MIkdQ39xn1vWwi1O5oazPoQJz0nTYjxxEE8kv3kFxtAGVRe3ypD3WeK2XeFYFMNMpatF9XiKzHo3]]></Encrypt>
<MsgSignature><![CDATA[407518b7649e86ef23978113f92d27afa9296533]]></MsgSignature>
<TimeStamp>1411525903</TimeStamp>
<Nonce><![CDATA[461056294]]></Nonce>
</xml>"""

        crypto = WeChatCrypto(self.token, self.encoding_aes_key, self.corp_id)
        encrypted = crypto.encrypt_message(reply, nonce, timestamp)

        _crypto.PrpCrypto = origin_crypto

        self.assertEqual(expected, encrypted)

    def test_decrypt_message(self):
        xml = """<xml><ToUserName><![CDATA[wx49f0ab532d5d035a]]></ToUserName>
<Encrypt><![CDATA[RgqEoJj5A4EMYlLvWO1F86ioRjZfaex/gePD0gOXTxpsq5Yj4GNglrBb8I2BAJVODGajiFnXBu7mCPatfjsu6IHCrsTyeDXzF6Bv283dGymzxh6ydJRvZsryDyZbLTE7rhnus50qGPMfp2wASFlzEgMW9z1ef/RD8XzaFYgm7iTdaXpXaG4+BiYyolBug/gYNx410cvkKR2/nPwBiT+P4hIiOAQqGp/TywZBtDh1yCF2KOd0gpiMZ5jSw3e29mTvmUHzkVQiMS6td7vXUaWOMZnYZlF3So2SjHnwh4jYFxdgpkHHqIrH/54SNdshoQgWYEvccTKe7FS709/5t6NMxuGhcUGAPOQipvWTT4dShyqio7mlsl5noTrb++x6En749zCpQVhDpbV6GDnTbcX2e8K9QaNWHp91eBdCRxthuL0=]]></Encrypt>
<AgentID><![CDATA[1]]></AgentID>
</xml>"""

        signature = '74d92dfeb87ba7c714f89d98870ae5eb62dff26d'
        timestamp = '1411525903'
        nonce = '461056294'

        crypto = WeChatCrypto(self.token, self.encoding_aes_key, self.corp_id)
        msg = crypto.decrypt_message(xml, signature, timestamp, nonce)
        msg_dict = xmltodict.parse(msg)['xml']
        self.assertEqual('test', msg_dict['Content'])
        self.assertEqual('messense', msg_dict['FromUserName'])

    def test_decrypt_binary_message(self):
        xml = b"""<xml><ToUserName><![CDATA[wx49f0ab532d5d035a]]></ToUserName>
<Encrypt><![CDATA[RgqEoJj5A4EMYlLvWO1F86ioRjZfaex/gePD0gOXTxpsq5Yj4GNglrBb8I2BAJVODGajiFnXBu7mCPatfjsu6IHCrsTyeDXzF6Bv283dGymzxh6ydJRvZsryDyZbLTE7rhnus50qGPMfp2wASFlzEgMW9z1ef/RD8XzaFYgm7iTdaXpXaG4+BiYyolBug/gYNx410cvkKR2/nPwBiT+P4hIiOAQqGp/TywZBtDh1yCF2KOd0gpiMZ5jSw3e29mTvmUHzkVQiMS6td7vXUaWOMZnYZlF3So2SjHnwh4jYFxdgpkHHqIrH/54SNdshoQgWYEvccTKe7FS709/5t6NMxuGhcUGAPOQipvWTT4dShyqio7mlsl5noTrb++x6En749zCpQVhDpbV6GDnTbcX2e8K9QaNWHp91eBdCRxthuL0=]]></Encrypt>
<AgentID><![CDATA[1]]></AgentID>
</xml>"""

        signature = '74d92dfeb87ba7c714f89d98870ae5eb62dff26d'
        timestamp = '1411525903'
        nonce = '461056294'

        crypto = WeChatCrypto(self.token, self.encoding_aes_key, self.corp_id)
        msg = crypto.decrypt_message(xml, signature, timestamp, nonce)
        msg_dict = xmltodict.parse(msg)['xml']
        self.assertEqual('test', msg_dict['Content'])
        self.assertEqual('messense', msg_dict['FromUserName'])
