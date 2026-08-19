# -*- coding: utf-8 -*-
import json
import threading
import unittest

from wechatpy.crypto import _get_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.work import ai_bot as _ai_bot
from wechatpy.work.ai_bot import WeChatAIBotCrypto, WeChatAIBotWebSocketClient


class AIBotPrpCryptoMock(_ai_bot.AIBotPrpCrypto):
    def get_random_string(self):
        return "1234567890123456"


class WeChatAIBotCryptoTestCase(unittest.TestCase):
    token = "123456"
    encoding_aes_key = "kWxPEV2UEDyxWpmPdKC3F4dgPDmOvfKX1HGnEUDS1aR"
    nonce = "461056294"
    timestamp = "1411525903"

    def setUp(self):
        self.crypto = WeChatAIBotCrypto(self.token, self.encoding_aes_key)

    def test_verify_url_returns_plaintext_challenge(self):
        encrypted_echo = _ai_bot.AIBotPrpCrypto(self.crypto.key).encrypt("echo-ok")
        signature = _get_signature(
            self.token,
            self.timestamp,
            self.nonce,
            encrypted_echo,
        )

        result = self.crypto.verify_url(
            signature,
            self.timestamp,
            self.nonce,
            encrypted_echo,
        )

        self.assertEqual(result, "echo-ok")

    def test_encrypt_and_decrypt_json_message(self):
        original_crypto = _ai_bot.AIBotPrpCrypto
        _ai_bot.AIBotPrpCrypto = AIBotPrpCryptoMock
        try:
            encrypted = self.crypto.encrypt_message(
                {"msgtype": "text", "text": {"content": "连接测试"}},
                self.nonce,
                self.timestamp,
            )
        finally:
            _ai_bot.AIBotPrpCrypto = original_crypto

        self.assertEqual(encrypted["timestamp"], self.timestamp)
        payload = self.crypto.decrypt_message(
            encrypted,
            encrypted["msgsignature"],
            encrypted["timestamp"],
            encrypted["nonce"],
        )

        self.assertEqual(payload["msgtype"], "text")
        self.assertEqual(payload["text"]["content"], "连接测试")

    def test_decrypt_message_rejects_invalid_signature(self):
        encrypted = self.crypto.encrypt_message(
            {"msgtype": "text", "text": {"content": "连接测试"}},
            self.nonce,
            self.timestamp,
        )

        with self.assertRaises(InvalidSignatureException):
            self.crypto.decrypt_message(
                encrypted,
                "invalid",
                encrypted["timestamp"],
                encrypted["nonce"],
            )


class FakeWebSocket(object):
    def __init__(self):
        self.closed = False
        self.sent_frames = []

    def close(self):
        self.closed = True

    def recv(self):
        request = self.sent_frames[-1]
        command = request["cmd"]
        body = {}
        if command == "aibot_upload_media_init":
            body = {"upload_id": "upload-1"}
        elif command == "aibot_upload_media_finish":
            body = {"media_id": "media-1"}
        return json.dumps({
            "headers": {"req_id": request["headers"]["req_id"]},
            "body": body,
            "errcode": 0,
        })

    def send(self, payload):
        self.sent_frames.append(json.loads(payload))


class WeChatAIBotWebSocketClientTestCase(unittest.TestCase):
    def test_connect_passes_optional_subscription_fields(self):
        connection = FakeWebSocket()
        client = WeChatAIBotWebSocketClient(
            "bot-id",
            "secret",
            plug_version="1.0.0",
            scene=1,
        )
        client._create_connection = lambda: connection

        with client:
            pass

        self.assertEqual(connection.sent_frames[0]["body"], {
            "bot_id": "bot-id",
            "plug_version": "1.0.0",
            "scene": 1,
            "secret": "secret",
        })

    def test_heartbeat_has_no_body(self):
        class ListenerWebSocket(FakeWebSocket):
            def recv(self):
                request = self.sent_frames[-1]
                if request["cmd"] == "ping":
                    return json.dumps({
                        "headers": {"req_id": request["headers"]["req_id"]},
                        "errcode": 0,
                    })
                return super().recv()

        connection = ListenerWebSocket()
        client = WeChatAIBotWebSocketClient("bot-id", "secret")
        client._create_connection = lambda: connection
        stop_event = threading.Event()

        def on_idle():
            if len(connection.sent_frames) >= 2:
                stop_event.set()

        client.serve_forever(
            lambda frame: None,
            stop_event,
            heartbeat_interval=0,
            on_idle=on_idle,
            reconnect_interval=0,
        )

        self.assertEqual(connection.sent_frames[-1]["cmd"], "ping")
        self.assertNotIn("body", connection.sent_frames[-1])

    def test_upload_and_send_file(self):
        connection = FakeWebSocket()
        client = WeChatAIBotWebSocketClient("bot-id", "secret")
        client._create_connection = lambda: connection

        with client:
            media_id = client.upload_media("file", "test.pdf", b"pdf-content")
            client.send_media_message("zhangsan", "file", media_id)

        self.assertEqual(media_id, "media-1")
        self.assertTrue(connection.closed)
        self.assertEqual(
            [frame["cmd"] for frame in connection.sent_frames],
            [
                "aibot_subscribe",
                "aibot_upload_media_init",
                "aibot_upload_media_chunk",
                "aibot_upload_media_finish",
                "aibot_send_msg",
            ],
        )
        self.assertEqual(connection.sent_frames[2]["body"]["chunk_index"], 0)
        self.assertEqual(connection.sent_frames[-1]["body"], {
            "chatid": "zhangsan",
            "msgtype": "file",
            "file": {"media_id": "media-1"},
        })

    def test_serve_forever_dispatches_callback_and_replies_with_same_request_id(self):
        class ListenerWebSocket(FakeWebSocket):
            def __init__(self):
                super().__init__()
                self.subscription_acknowledged = False
                self.responses = [
                    {
                        "cmd": "aibot_msg_callback",
                        "headers": {"req_id": "callback-1"},
                        "body": {"msgid": "message-1", "msgtype": "text"},
                    },
                ]

            def recv(self):
                if not self.subscription_acknowledged:
                    self.subscription_acknowledged = True
                    return json.dumps({
                        "headers": {"req_id": self.sent_frames[-1]["headers"]["req_id"]},
                        "errcode": 0,
                    })
                if self.responses:
                    return json.dumps(self.responses.pop(0))
                if len(self.sent_frames) == 2:
                    return json.dumps({"headers": {"req_id": "callback-1"}, "errcode": 0})
                raise TimeoutError()

        connection = ListenerWebSocket()
        client = WeChatAIBotWebSocketClient("bot-id", "secret")
        client._create_connection = lambda: connection
        stop_event = threading.Event()

        def on_message(frame):
            client.reply_stream(
                frame["headers"]["req_id"],
                "stream-1",
                "Working...",
            )
            stop_event.set()

        client.serve_forever(on_message, stop_event, reconnect_interval=0)

        self.assertTrue(connection.closed)
        self.assertEqual(connection.sent_frames[-1]["cmd"], "aibot_respond_msg")
        self.assertEqual(connection.sent_frames[-1]["headers"]["req_id"], "callback-1")
        self.assertEqual(connection.sent_frames[-1]["body"]["stream"]["id"], "stream-1")
