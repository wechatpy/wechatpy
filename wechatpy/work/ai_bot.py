# -*- coding: utf-8 -*-
"""WeCom intelligent-bot callback and WebSocket helpers."""

import base64
import hashlib
import json
import time
import uuid

from wechatpy.crypto import BasePrpCrypto, BaseWeChatCrypto, _get_signature
from wechatpy.exceptions import InvalidSignatureException, WeChatException
from wechatpy.utils import to_binary, to_text
from wechatpy.work.exceptions import InvalidCorpIdException


AI_BOT_DEFAULT_WS_URL = "wss://openws.work.weixin.qq.com"
AI_BOT_EVENT_CALLBACK_COMMAND = "aibot_event_callback"
AI_BOT_HEARTBEAT_COMMAND = "ping"
AI_BOT_MEDIA_TYPES = ("file", "image", "voice", "video")
AI_BOT_MAX_MEDIA_CHUNK_SIZE = 512 * 1024
AI_BOT_MAX_MEDIA_CHUNKS = 100
AI_BOT_MESSAGE_CALLBACK_COMMAND = "aibot_msg_callback"
AI_BOT_RESPONSE_COMMAND = "aibot_respond_msg"


class WeChatAIBotWebSocketException(WeChatException):
    """Raised when the WeCom intelligent-bot WebSocket protocol fails."""

    def __init__(self, errcode=-1, errmsg="WeCom intelligent-bot WebSocket error"):
        super().__init__(errcode, errmsg)


class AIBotPrpCrypto(BasePrpCrypto):
    """Encrypt and decrypt the intelligent-bot payload with an empty receive ID."""

    def encrypt(self, text, receive_id=None):
        del receive_id
        return self._encrypt(text, "")

    def decrypt(self, text, receive_id=None):
        del receive_id
        return self._decrypt(text, "", InvalidCorpIdException)


class WeChatAIBotCrypto(BaseWeChatCrypto):
    """Handle the JSON callback protocol used by WeCom intelligent bots."""

    def __init__(self, token, encoding_aes_key):
        super().__init__(token, encoding_aes_key, "")

    def verify_url(self, signature, timestamp, nonce, echo_str):
        """Verify the callback URL and return WeCom's plaintext challenge."""
        return self._check_signature(
            signature,
            timestamp,
            nonce,
            echo_str,
            AIBotPrpCrypto,
        )

    def decrypt_message(self, msg, signature, timestamp, nonce):
        """Verify and decrypt a JSON callback payload into a dictionary."""
        if not isinstance(msg, dict):
            msg = json.loads(to_text(msg))
        encrypt = msg.get("encrypt")
        if not encrypt:
            raise ValueError("The intelligent-bot payload has no encrypt value.")
        expected_signature = _get_signature(self.token, timestamp, nonce, encrypt)
        if expected_signature != signature:
            raise InvalidSignatureException()
        payload = AIBotPrpCrypto(self.key).decrypt(encrypt)
        return json.loads(payload)

    def encrypt_message(self, msg, nonce, timestamp=None):
        """Encrypt a JSON response for an intelligent-bot callback."""
        if not isinstance(msg, str):
            msg = json.dumps(msg, ensure_ascii=False, separators=(",", ":"))
        timestamp = to_text(timestamp or int(time.time()))
        encrypt = to_text(AIBotPrpCrypto(self.key).encrypt(to_binary(msg)))
        return {
            "encrypt": encrypt,
            "msgsignature": _get_signature(self.token, timestamp, nonce, encrypt),
            "timestamp": timestamp,
            "nonce": nonce,
        }


class WeChatAIBotWebSocketClient(object):
    """Use WeCom intelligent-bot WebSocket connections for messages and media."""

    DEFAULT_WS_URL = AI_BOT_DEFAULT_WS_URL

    def __init__(self, bot_id, secret, ws_url=None, timeout=30, scene=None, plug_version=None):
        self.bot_id = bot_id
        self.scene = scene
        self.secret = secret
        self.timeout = timeout
        self.plug_version = plug_version
        self.ws_url = ws_url or self.DEFAULT_WS_URL
        self._connection = None
        self._deferred_frames = []
        self._poll_timeout = 1

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def _create_connection(self):
        try:
            import websocket
        except ImportError as error:
            raise WeChatAIBotWebSocketException(
                -1,
                "websocket-client is required for WeCom intelligent-bot media delivery.",
            ) from error
        return websocket.create_connection(self.ws_url, timeout=self.timeout)

    def _decode_frame(self, response):
        if isinstance(response, bytes):
            response = response.decode("utf-8")
        try:
            return json.loads(response)
        except (TypeError, ValueError) as error:
            raise WeChatAIBotWebSocketException(-1, "Invalid WebSocket response.") from error

    def _is_callback_frame(self, frame):
        return frame.get("cmd") in (
            AI_BOT_EVENT_CALLBACK_COMMAND,
            AI_BOT_MESSAGE_CALLBACK_COMMAND,
        )

    def _set_connection_timeout(self, timeout):
        if self._connection and hasattr(self._connection, "settimeout"):
            self._connection.settimeout(timeout)

    def _receive_response(self, request_id):
        self._set_connection_timeout(self.timeout)
        while True:
            frame = self._decode_frame(self._connection.recv())

            headers = frame.get("headers") or {}
            if headers.get("req_id") != request_id:
                if self._is_callback_frame(frame):
                    self._deferred_frames.append(frame)
                continue
            errcode = frame.get("errcode", 0)
            if errcode not in (0, "0", None):
                raise WeChatAIBotWebSocketException(errcode, frame.get("errmsg") or "WeCom rejected the request.")
            return frame

    def _request(self, command, body=None, request_id=None):
        if not self._connection:
            raise WeChatAIBotWebSocketException(-1, "The WebSocket connection is not open.")
        request_id = request_id or "%s_%s" % (command, uuid.uuid4().hex)
        frame = {
            "cmd": command,
            "headers": {"req_id": request_id},
        }
        if body is not None:
            frame["body"] = body
        self._connection.send(json.dumps(frame, ensure_ascii=False, separators=(",", ":")))
        try:
            return self._receive_response(request_id)
        finally:
            self._set_connection_timeout(self._poll_timeout)

    def _media_body(self, media_type, media_id, video_options=None):
        if media_type not in AI_BOT_MEDIA_TYPES:
            raise ValueError("Unsupported intelligent-bot media type: %s" % media_type)
        media_body = {"media_id": media_id}
        if media_type == "video" and video_options:
            if video_options.get("title"):
                media_body["title"] = video_options["title"]
            if video_options.get("description"):
                media_body["description"] = video_options["description"]
        return {"msgtype": media_type, media_type: media_body}

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    def connect(self):
        if self._connection:
            return self
        if not self.bot_id or not self.secret:
            raise WeChatAIBotWebSocketException(-1, "Both bot_id and secret are required.")
        self._connection = self._create_connection()
        try:
            body = {"bot_id": self.bot_id, "secret": self.secret}
            if self.scene is not None:
                body["scene"] = self.scene
            if self.plug_version is not None:
                body["plug_version"] = self.plug_version
            self._request("aibot_subscribe", body)
        except Exception:
            self.close()
            raise
        return self

    def reply(self, request_id, body):
        """Reply to a callback by preserving its ``headers.req_id`` value."""
        if not request_id:
            raise ValueError("request_id is required to reply to an intelligent-bot callback.")
        return self._request(AI_BOT_RESPONSE_COMMAND, body, request_id=request_id)

    def reply_media_message(self, request_id, media_type, media_id, video_options=None):
        """Reply to an inbound callback with an already uploaded media item."""
        return self.reply(request_id, self._media_body(media_type, media_id, video_options))

    def reply_stream(self, request_id, stream_id, content, finish=False):
        """Reply or update a stream message for an inbound callback."""
        if not stream_id:
            raise ValueError("stream_id is required for an intelligent-bot stream reply.")
        return self.reply(request_id, {
            "msgtype": "stream",
            "stream": {
                "content": content or "",
                "finish": bool(finish),
                "id": stream_id,
            },
        })

    def serve_forever(
        self,
        on_message,
        stop_event,
        on_event=None,
        on_authenticated=None,
        on_idle=None,
        on_connected=None,
        on_error=None,
        poll_interval=1,
        reconnect_interval=5,
        heartbeat_interval=30,
        should_continue=None,
    ):
        """Keep one authenticated connection and dispatch server callback frames.

        ``on_message`` and ``on_event`` receive the complete protocol frame. The
        caller can reply immediately with :meth:`reply` or :meth:`reply_stream`.
        The method reconnects until ``stop_event`` is set or ``should_continue``
        returns false.
        """
        self._poll_timeout = max(float(poll_interval), 0.1)
        next_heartbeat_at = 0
        while not stop_event.is_set():
            if should_continue and not should_continue():
                return
            try:
                self.connect()
                self._set_connection_timeout(self._poll_timeout)
                if on_authenticated:
                    on_authenticated()
                if on_connected:
                    on_connected()
                next_heartbeat_at = time.time() + heartbeat_interval
                while not stop_event.is_set():
                    if should_continue and not should_continue():
                        return
                    while self._deferred_frames:
                        self._dispatch_frame(self._deferred_frames.pop(0), on_message, on_event)
                    try:
                        frame = self._decode_frame(self._connection.recv())
                    except Exception as error:
                        if error.__class__.__name__ not in ("WebSocketTimeoutException", "timeout"):
                            raise
                        frame = False
                    if frame:
                        self._dispatch_frame(frame, on_message, on_event)
                    now = time.time()
                    if on_idle:
                        on_idle()
                    if now >= next_heartbeat_at:
                        self._request(AI_BOT_HEARTBEAT_COMMAND)
                        next_heartbeat_at = time.time() + heartbeat_interval
            except Exception as error:
                if on_error:
                    on_error(error)
            finally:
                self.close()
            if not stop_event.is_set():
                stop_event.wait(reconnect_interval)

    def _dispatch_frame(self, frame, on_message, on_event):
        command = frame.get("cmd")
        if command == AI_BOT_MESSAGE_CALLBACK_COMMAND:
            on_message(frame)
            return
        if command == AI_BOT_EVENT_CALLBACK_COMMAND and on_event:
            on_event(frame)

    def send_media_message(self, chatid, media_type, media_id, video_options=None):
        """Actively send an uploaded media item to a user or group conversation."""
        if not chatid:
            raise ValueError("chatid is required to send intelligent-bot media.")
        body = self._media_body(media_type, media_id, video_options)
        body["chatid"] = chatid
        return self._request("aibot_send_msg", body)

    def upload_media(self, media_type, filename, content):
        """Upload bytes through WebSocket chunking and return the temporary media ID."""
        if media_type not in AI_BOT_MEDIA_TYPES:
            raise ValueError("Unsupported intelligent-bot media type: %s" % media_type)
        if not filename:
            raise ValueError("filename is required for intelligent-bot media upload.")
        if not isinstance(content, bytes):
            raise TypeError("content must be bytes.")
        if not content:
            raise ValueError("Cannot upload an empty file.")

        chunk_count = (len(content) + AI_BOT_MAX_MEDIA_CHUNK_SIZE - 1) // AI_BOT_MAX_MEDIA_CHUNK_SIZE
        if chunk_count > AI_BOT_MAX_MEDIA_CHUNKS:
            raise ValueError("File is too large for intelligent-bot media upload (maximum is about 50 MB).")

        init_response = self._request("aibot_upload_media_init", {
            "filename": filename,
            "md5": hashlib.md5(content).hexdigest(),
            "total_chunks": chunk_count,
            "total_size": len(content),
            "type": media_type,
        })
        upload_id = (init_response.get("body") or {}).get("upload_id")
        if not upload_id:
            raise WeChatAIBotWebSocketException(-1, "WeCom did not return an upload_id.")

        for chunk_index in range(chunk_count):
            start = chunk_index * AI_BOT_MAX_MEDIA_CHUNK_SIZE
            chunk = content[start:start + AI_BOT_MAX_MEDIA_CHUNK_SIZE]
            self._request("aibot_upload_media_chunk", {
                "base64_data": base64.b64encode(chunk).decode("ascii"),
                "chunk_index": chunk_index,
                "upload_id": upload_id,
            })

        finish_response = self._request("aibot_upload_media_finish", {"upload_id": upload_id})
        media_id = (finish_response.get("body") or {}).get("media_id")
        if not media_id:
            raise WeChatAIBotWebSocketException(-1, "WeCom did not return a media_id.")
        return media_id
