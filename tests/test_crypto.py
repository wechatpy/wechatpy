# -*- coding: utf-8 -*-
import unittest

import xmltodict

from wechatpy.work import crypto as _crypto
from wechatpy.work.crypto import WeChatCrypto


class PrpCryptoMock(_crypto.PrpCrypto):
    def get_random_string(self):
        return "1234567890123456"


class CryptoTestCase(unittest.TestCase):

    token = "123456"
    encoding_aes_key = "kWxPEV2UEDyxWpmPdKC3F4dgPDmOvfKX1HGnEUDS1aR"
    corp_id = "wx49f0ab532d5d035a"

    def test_check_signature_should_ok(self):
        signature = "dd6b9c95b495b3f7e2901bfbc76c664930ffdb96"
        timestamp = "1411443780"
        nonce = "437374425"
        echo_str = "4ByGGj+sVCYcvGeQYhaKIk1o0pQRNbRjxybjTGblXrBaXlTXeOo1+bXFXDQQb1o6co6Yh9Bv41n7hOchLF6p+Q=="  # NOQA

        crypto = WeChatCrypto(self.token, self.encoding_aes_key, self.corp_id)
        echo_str = crypto.check_signature(signature, timestamp, nonce, echo_str)

    def test_check_signature_should_fail(self):
        from wechatpy.exceptions import InvalidSignatureException

        signature = "dd6b9c95b495b3f7e2901bfbc76c664930ffdb96"
        timestamp = "1411443780"
        nonce = "437374424"
        echo_str = "4ByGGj+sVCYcvGeQYhaKIk1o0pQRNbRjxybjTGblXrBaXlTXeOo1+bXFXDQQb1o6co6Yh9Bv41n7hOchLF6p+Q=="  # NOQA

        crypto = WeChatCrypto(self.token, self.encoding_aes_key, self.corp_id)
        self.assertRaises(
            InvalidSignatureException,
            crypto.check_signature,
            signature,
            timestamp,
            nonce,
            echo_str,
        )

    def test_encrypt_message(self):
        origin_crypto = _crypto.PrpCrypto
        _crypto.PrpCrypto = PrpCryptoMock

        nonce = "461056294"
        timestamp = "1411525903"
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

        signature = "74d92dfeb87ba7c714f89d98870ae5eb62dff26d"
        timestamp = "1411525903"
        nonce = "461056294"

        crypto = WeChatCrypto(self.token, self.encoding_aes_key, self.corp_id)
        msg = crypto.decrypt_message(xml, signature, timestamp, nonce)
        msg_dict = xmltodict.parse(msg)["xml"]
        self.assertEqual("test", msg_dict["Content"])
        self.assertEqual("messense", msg_dict["FromUserName"])

    def test_decrypt_binary_message(self):
        xml = b"""<xml><ToUserName><![CDATA[wx49f0ab532d5d035a]]></ToUserName>
<Encrypt><![CDATA[RgqEoJj5A4EMYlLvWO1F86ioRjZfaex/gePD0gOXTxpsq5Yj4GNglrBb8I2BAJVODGajiFnXBu7mCPatfjsu6IHCrsTyeDXzF6Bv283dGymzxh6ydJRvZsryDyZbLTE7rhnus50qGPMfp2wASFlzEgMW9z1ef/RD8XzaFYgm7iTdaXpXaG4+BiYyolBug/gYNx410cvkKR2/nPwBiT+P4hIiOAQqGp/TywZBtDh1yCF2KOd0gpiMZ5jSw3e29mTvmUHzkVQiMS6td7vXUaWOMZnYZlF3So2SjHnwh4jYFxdgpkHHqIrH/54SNdshoQgWYEvccTKe7FS709/5t6NMxuGhcUGAPOQipvWTT4dShyqio7mlsl5noTrb++x6En749zCpQVhDpbV6GDnTbcX2e8K9QaNWHp91eBdCRxthuL0=]]></Encrypt>
<AgentID><![CDATA[1]]></AgentID>
</xml>"""

        signature = "74d92dfeb87ba7c714f89d98870ae5eb62dff26d"
        timestamp = "1411525903"
        nonce = "461056294"

        crypto = WeChatCrypto(self.token, self.encoding_aes_key, self.corp_id)
        msg = crypto.decrypt_message(xml, signature, timestamp, nonce)
        msg_dict = xmltodict.parse(msg)["xml"]
        self.assertEqual("test", msg_dict["Content"])
        self.assertEqual("messense", msg_dict["FromUserName"])

    def test_wxa_decrypt_message(self):
        from wechatpy.crypto import WeChatWxaCrypto

        appid = "wx4f4bc4dec97d474b"
        session_key = "tiihtNczf5v6AKRyjwEUhQ=="
        encrypted_data = (
            "CiyLU1Aw2KjvrjMdj8YKliAjtP4gsMZMQmRzooG2xrDcvSnxIMXFufNstNGTyaGS9uT5geRa0W4oTOb1WT7fJlAC"
            "+oNPdbB+3hVbJSRgv+4lGOETKUQz6OYStslQ142dNCuabNPGBzlooOmB231qMM85d2"
            "/fV6ChevvXvQP8Hkue1poOFtnEtpyxVLW1zAo6/1Xx1COxFvrc2d7UL/lmHInNlxuacJXwu0fjpXfz"
            "/YqYzBIBzD6WUfTIF9GRHpOn/Hz7saL8xz+W//FRAUid1OksQaQx4CMs8LOddcQhULW4ucetDf96JcR3g0gfRK4PC7E"
            "/r7Z6xNrXd2UIeorGj5Ef7b1pJAYB6Y5anaHqZ9J6nKEBvB4DnNLIVWSgARns"
            "/8wR2SiRS7MNACwTyrGvt9ts8p12PKFdlqYTopNHR1Vf7XjfhQlVsAJdNiKdYmYVoKlaRv85IfVunYzO0IKXsyl7JCUjCpoG"
            "20f0a04COwfneQAGGwd5oa+T8yO5hzuyDb/XcxxmK01EpqOyuxINew=="
        )
        iv = "r7BXXKkLb8qrSNn05n0qiA=="

        crypto = WeChatWxaCrypto(session_key, iv, appid)
        decrypted = crypto.decrypt_message(encrypted_data)
        self.assertEqual(appid, decrypted["watermark"]["appid"])

    def test_refund_notify_decrypt_message(self):
        from wechatpy.crypto import WeChatRefundCrypto

        appid = "wx4f4bc4dec97d474b"
        mch_id = "12345678"
        api_key = "OF4Ne3znh8KqL0V4NqmALQa0uXMYKcEk"
        xml = """
<xml>
<return_code>SUCCESS</return_code>
<appid><![CDATA[wx4f4bc4dec97d474b]]></appid>
<mch_id><![CDATA[12345678]]></mch_id>
<nonce_str><![CDATA[c1c237efc87ee8dfcb3f9124b63a4d94]]></nonce_str>
<req_info><![CDATA[51A27s9LxbaEv52nBOrqa0FCs3HVIM31Wc3BpNqSCP5MQlS8HL1Vl7mZ21043B7PZy7adtOZGtZv44lGl0U8JXlVFL4Ltxsw6+pACjZBB0Qi1LUDjFlP2IyTxYX4eC57kxnCphDdIyRkU67kOWW/HN/efggTUlaPJkoL5kVe9Y1MZF55IHR4lwGI7WtVLtxATX1tkAVZF+/ri0WlPXo9+GkqeB2/id6Ozw09Tqp8C/TKbmKBpRhTCRU2TzfQoLa6fjbgETFHJ795aEMyUZPQYbbsz6U9Rj9lUzEh8+Oc8KYTXa9zVk+nnFr82+yjffb3d36ylTe0y/VmYf90rf9cbiJQdM00zZ8Qa99SlMTs2wjOO4Mi4Btlg1PebsLF8TkqbSZkRJDGs61UunUB8Km1b/VeBxXuv4D3H7DiVZ9Fj7lq2j07zFDpxxlhhen7kZvMWWO3lrfFpA9c4eFOqfF9SxcU9nBmHfDD1g/dsrMl6+a71xQHJ/gn80fZOefUBv92ggqutsuJ4gd4OqkmO0XUs8e4XQyLpra+LvpmahsU5lBIZuQcMq3FHrqe8hXTfp3+3qym2wGfvPI75jx41VZwmBQy9izB1Id+A5lUeXC5QJy+ryDu/dWkhB+aMjkElaI/Epmcc/IEPaI73W6Hc58hNednOM536rPnn+GDc98PdGszpLTjmaZSu8dtqwPaym66yRqFQowzFoBbooik57iHUFBCeWya7XcXYL9WKhRF3uIZM+Kfv9/Zs2pF+w9/EJpltuzPpT1GP2VTMSHz45zwphFlS2lX8wHyZ+k9n2dptzQqpOCPedt5iQAmAe1oNQMxNdPDH9g68x9UzWD1kfK/dPO+3NPAh0XG+io4x15fIknNf7JLjpAuWicMMzCdwC4hhqeYOzQ+pC9f2xJXi5YViNKIZY69oO8eoHYRitLZrHLgx3oB2zimmqX6BI+DMklKAzAqqgGmbFxcVTvxZB6cMCx+H7TTWXnjAG+6A3SrCcxg0l5+UB93pkAYR7SVJ+VaZoiBqlqnZvb7IM17n9XaaFntlzvbbFCIa7OnOQb5Lvw=]]></req_info>
</xml>"""
        refund_crypto = WeChatRefundCrypto(api_key)
        data = refund_crypto.decrypt_message(xml, appid, mch_id)
        self.assertEqual("1234", data["out_refund_no"])
        self.assertEqual("2020010418301551404339261814", data["out_trade_no"])
        self.assertEqual("4200000483202001042069747825", data["transaction_id"])
        self.assertEqual("50300103182020010413419046597", data["refund_id"])
