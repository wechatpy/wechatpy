# -*- coding: utf-8 -*-
import json
import os
import unittest

from httmock import HTTMock, response, urlmatch

from wechatpy.iot import IotClient

_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_FIXTURE_PATH = os.path.join(_TESTS_PATH, "fixtures", "iot")


@urlmatch(netloc=r"(.*\.)?api\.weixin\.qq\.com$")
def wechat_api_mock(url, request):
    path = url.path.replace("/cgi-bin/", "").replace("/ilink/api/", "").replace("/", "_")
    res_file = os.path.join(_FIXTURE_PATH, f"{path}.json")
    content = {
        "errcode": 99999,
        "errmsg": f"can not find fixture {res_file}",
    }
    headers = {"Content-Type": "application/json"}
    try:
        with open(res_file, "rb") as f:
            content = json.loads(f.read().decode("utf-8"))
    except (IOError, ValueError) as e:
        content["errmsg"] = f"Loads fixture {res_file} failed, error: {e}"
    return response(200, content, headers, request=request)


class IotClientTestCase(unittest.TestCase):
    app_id = "123456"
    secret = "123456"

    def setUp(self):
        self.client = IotClient(self.app_id, self.secret)

    def test_init_client_with_access_token(self):
        client = IotClient(self.app_id, self.secret, access_token="abcdef")
        self.assertTrue(client)

    def test_fetch_access_token(self):
        with HTTMock(wechat_api_mock):
            token = self.client.fetch_access_token()
            self.assertEqual("1234567890", token["access_token"])
            self.assertEqual(7200, token["expires_in"])
            self.assertEqual("1234567890", self.client.access_token)

    def test_cloud_register_device(self):
        with HTTMock(wechat_api_mock):
            res = self.client.cloud.cloud_register_device(1, [{"sn": 1}, {"sn": 2}])
            self.assertEqual(0, res["errcode"])

    def test_get_device_ticket(self):
        with HTTMock(wechat_api_mock):
            res = self.client.device.get_device_ticket("xxx@ilink.im.sdk", "xxx")
            self.assertEqual(0, res["errcode"])

    def test_reset_device(self):
        with HTTMock(wechat_api_mock):
            res = self.client.device.reset_device("xxx@ilink.im.sdk")
            self.assertEqual(0, res["errcode"])
