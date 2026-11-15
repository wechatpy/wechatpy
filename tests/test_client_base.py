# -*- coding: utf-8 -*-
"""Shared client timeout, token refresh, and request preservation regressions."""

import json
import unittest
from unittest import mock
from urllib.parse import parse_qs

import requests
from httmock import HTTMock, response

from wechatpy import WeChatClient
from wechatpy.exceptions import APILimitedException, WeChatClientException
from wechatpy.iot.client import IotClient
from wechatpy.work import WeChatClient as WorkClient
from wechatpy.work.services import WeChatServiceClient


class BaseWeChatClientTestCase(unittest.TestCase):
    """Exercise the shared behavior through concrete clients' public requests."""

    client_types = (WeChatClient, WorkClient, IotClient)

    def clients(self, **kwargs):
        """Create each client that consumes the shared result handler."""
        for client_type in self.client_types:
            yield client_type("appid", "secret", **kwargs)
        yield WeChatServiceClient("corp", "suite", "secret", "ticket", **kwargs)

    @staticmethod
    def token_response(url, request):
        """Return a token response only for a token acquisition endpoint."""
        if url.path.endswith(("/token", "/gettoken", "/get_suite_token")):
            key = "suite_access_token" if url.path.endswith("/get_suite_token") else "access_token"
            return response(200, {key: "new-token", "expires_in": 7200}, request=request)

    def test_token_requests_use_client_timeout_and_cache(self):
        """Token requests inherit the timeout and successful calls reuse the cache."""

        def api_mock(url, request):
            """Accept token acquisition and ordinary API requests."""
            return self.token_response(url, request) or response(200, {"errcode": 0}, request=request)

        for timeout in (None, 5, (2, 5)):
            for client in self.clients(timeout=timeout):
                with self.subTest(client=type(client), timeout=timeout):
                    with HTTMock(api_mock), mock.patch.object(client._http, "send", wraps=client._http.send) as send:
                        self.assertEqual(0, client.get("test")["errcode"])
                        self.assertEqual(0, client.get("test")["errcode"])
                    self.assertEqual(3, send.call_count)
                    self.assertEqual([timeout] * 3, [call.kwargs["timeout"] for call in send.call_args_list])

    def test_token_refresh_is_limited_to_one_retry(self):
        """Repeated token rejection raises after one refresh and one retry."""
        for errcode in (40001, 40014, 42001):
            for client in self.clients(access_token="old-token"):
                with self.subTest(client=type(client), errcode=errcode):
                    api_requests = []
                    token_requests = []

                    def api_mock(
                        url, request, api_requests=api_requests, token_requests=token_requests, errcode=errcode
                    ):
                        """Reject API calls while recording this case's token refreshes."""
                        token = self.token_response(url, request)
                        if token is not None:
                            token_requests.append(request)
                            return token
                        api_requests.append(request)
                        self.assertLessEqual(len(api_requests), 2, "retried an already refreshed token")
                        return response(200, {"errcode": errcode, "errmsg": "invalid token"}, request=request)

                    with HTTMock(api_mock), self.assertRaises(WeChatClientException) as raised:
                        client.get("test")
                    self.assertEqual(errcode, raised.exception.errcode)
                    self.assertEqual("invalid token", raised.exception.errmsg)
                    self.assertIs(api_requests[-1], raised.exception.request)
                    self.assertEqual(2, len(api_requests))
                    self.assertEqual(1, len(token_requests))
                    self.assertTrue(client.auto_retry)

    def test_token_refresh_preserves_request_and_result_processor(self):
        """Recovery retains the request and processes the successful result once."""
        for client_type in self.client_types:
            with self.subTest(client=client_type):
                client = client_type("appid", "secret", access_token="old-token", timeout=5)
                api_requests = []
                token_requests = []
                processor = mock.Mock(side_effect=lambda result: result["value"])

                def api_mock(url, request, api_requests=api_requests, token_requests=token_requests):
                    """Accept the same request after its expired token is refreshed."""
                    token = self.token_response(url, request)
                    if token is not None:
                        token_requests.append(request)
                        return token
                    api_requests.append(request)
                    query = parse_qs(url.query)
                    self.assertEqual(["kept"], query["param"])
                    self.assertEqual("POST", request.method)
                    self.assertEqual({"content": "hello"}, json.loads(request.body.decode("utf-8")))
                    if query["access_token"] == ["old-token"]:
                        return response(200, {"errcode": 42001, "errmsg": "expired"}, request=request)
                    self.assertEqual(["new-token"], query["access_token"])
                    return response(200, {"errcode": 0, "value": "ok"}, request=request)

                with HTTMock(api_mock), mock.patch.object(client._http, "send", wraps=client._http.send) as send:
                    result = client.post(
                        "test",
                        params={"param": "kept"},
                        data={"content": "hello"},
                        timeout=(1, 3),
                        result_processor=processor,
                    )
                self.assertEqual("ok", result)
                processor.assert_called_once_with({"errcode": 0, "value": "ok"})
                self.assertEqual(2, len(api_requests))
                self.assertEqual(1, len(token_requests))
                self.assertEqual([(1, 3), 5, (1, 3)], [call.kwargs["timeout"] for call in send.call_args_list])

    def test_retry_disabled_and_other_api_errors_do_not_refresh(self):
        """Disabled retries and unrelated API errors preserve the original failure."""
        for auto_retry, errcode, exception in (
            (False, 42001, WeChatClientException),
            (True, 40003, WeChatClientException),
            (True, 45009, APILimitedException),
        ):
            for client in self.clients(access_token="old-token", auto_retry=auto_retry):
                with self.subTest(client=type(client), auto_retry=auto_retry, errcode=errcode):
                    api_requests = []

                    def api_mock(url, request, api_requests=api_requests, errcode=errcode):
                        """Return this case's API error without acquiring a new token."""
                        api_requests.append(request)
                        return response(200, {"errcode": errcode, "errmsg": "rejected"}, request=request)

                    with HTTMock(api_mock), self.assertRaises(exception) as raised:
                        client.get("test")
                    self.assertEqual(errcode, raised.exception.errcode)
                    self.assertEqual(1, len(api_requests))

    def test_transport_timeouts_do_not_retry(self):
        """A transport timeout on token acquisition or the API call propagates once."""
        for access_token in (None, "cached-token"):
            for client in self.clients(access_token=access_token, timeout=5):
                with self.subTest(client=type(client), access_token=access_token):
                    api_requests = []

                    def api_mock(url, request, api_requests=api_requests):
                        """Record the attempted request before timing out."""
                        api_requests.append(request)
                        raise requests.Timeout("request timed out")

                    with HTTMock(api_mock), self.assertRaises(requests.Timeout):
                        client.get("test")
                    self.assertEqual(1, len(api_requests))
