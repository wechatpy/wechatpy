# -*- coding: utf-8 -*-
import hashlib
import json
import os
import unittest
import pytest
from httmock import urlmatch, response, HTTMock

from wechatpy.pay.v3 import WeChatPay

_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_CERTS_PATH = os.path.join(_TESTS_PATH, "certs")
_FIXTURE_PATH = os.path.join(_TESTS_PATH, "fixtures", "pay/v3/")


@urlmatch(netloc=r"(.*\.)?api\.mch\.weixin\.qq\.com$")
def wechat_api_mock(url, request):
    path = (url.path[1:] if url.path.startswith("/") else url.path).replace("v3/", "").replace("/", "_")
    res_file = os.path.join(_FIXTURE_PATH, f"{path}.json")
    content = {
        "errcode": 99999,
        "errmsg": f"can not find fixture {res_file}",
    }
    headers = {"Content-Type": "application/json", "Wechatpay-Serial": "12345"}
    try:
        with open(res_file, "rb") as f:
            content = json.loads(f.read().decode("utf-8"))
    except (IOError, ValueError):
        pass
    return response(200, content, headers, request=request)


class WeChatPayTestCase(unittest.TestCase):
    def setUp(self):
        self.client = WeChatPay(
            appid="abc1234",
            apiv3_key="test123",
            mch_id="1192221",
            wechat_cert_dir=_CERTS_PATH,
            apiclient_cert_path=os.path.join(_CERTS_PATH, "apiclient_cert.pem"),
            apiclient_key_path=os.path.join(_CERTS_PATH, "apiclient_key.pem"),
            skip_check_signature=True,  # 测试无法校验证书
        )

    def test_calculate_signature(self):
        from wechatpy.pay.utils import calculate_signature_rsa

        with open(self.client.apiclient_key_path, "rb") as public_fp:
            apiclient_key = public_fp.read()

        nonce_str = "1E3A8D73B5A4AEE787C0F68B5DAB8520"
        timestamp = "1651854037"
        sign = calculate_signature_rsa(apiclient_key, "GET", "test", "", nonce_str=nonce_str, timestamp=timestamp)

        expected = (
            "c4VewIfiOrSXkYtGqoZFzzjOr3LMhFFJRD5l18glbIUyXEF1wcG1euB4w5QdBlhgytM+28W7wmwqWTA8RsQWTBXR0YEXC6Mtd5xpl"
            "SXlXghv7ORl0a2TRVQSuf/vhKOdXc54Ima3wqj8AOkMeaiswp8fdnwd6yq1s0bx6uchP9Q6PO0INGnpdH8NeKP21dlefeOc4H7Ovnq"
            "HEyj/BsvdE1/DYUIFkw1q5fIAfxcUoqeXThtIL6ajLZgaaQJgYhPV7Cd6UMf5gY3yxKYWIWWHALtdWrn+pCcIPKrop/keqHE9wJPYt"
            "AP3uJ8UKohiHDft01X5ex0Es5Z12+lR9VLyEQ=="
        )
        self.assertEqual(expected, sign)

    def test_media(self):
        with HTTMock(wechat_api_mock):
            data = b""
            sha256_data = hashlib.sha256(data).hexdigest()
            response = self.client.media.upload_image(data, "test.jpeg", sha256_data)
            self.assertIn("media_id", response)

    @pytest.mark.skip(reason="no way of currently testing this, need encrypt cert")
    def test_update_certificates(self):
        with HTTMock(wechat_api_mock):
            self.client.update_certificates(skip_check_signature=True)
            self.assertEqual(
                self.client.wechat_cert_dict,
                [{"encrypt_certificate": "", "serial_no": ""}, {"encrypt_certificate": "", "serial_no": ""}],
            )

    def test_applyments_query(self):
        with HTTMock(wechat_api_mock):
            response = self.client.ecommerce.applyments_query_by_applyment_id("1234")
            self.assertIn("applyment_id", response)
            self.assertIn("applyment_state", response)
            self.assertIn("applyment_state_desc", response)

            response = self.client.ecommerce.applyments_query_by_out_request_no("APPLYMENT_00000000001")
            self.assertIn("applyment_id", response)
            self.assertIn("applyment_state", response)
            self.assertIn("applyment_state_desc", response)

    def test_settlement_query(self):
        with HTTMock(wechat_api_mock):
            response = self.client.ecommerce.settlement_query("12345")
            self.assertIn("account_bank", response)
            self.assertIn("account_number", response)
            self.assertIn("verify_result", response)

    def test_provinces(self):
        with HTTMock(wechat_api_mock):
            response = self.client.banks.query_provinces()
            self.assertIn("data", response)

    def test_cities(self):
        with HTTMock(wechat_api_mock):
            response = self.client.banks.query_cities(20)
            self.assertIn("data", response)

    def test_merchant_balance_query(self):
        with HTTMock(wechat_api_mock):
            response = self.client.ecommerce.merchant_balance_query()
            self.assertIn("available_amount", response)
            self.assertIn("pending_amount", response)
