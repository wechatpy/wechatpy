# -*- coding: utf-8 -*-
import json
import os
import unittest
from httmock import urlmatch, response, HTTMock

from wechatpy.pay.v3 import WeChatPay

_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_CERTS_PATH = os.path.join(_TESTS_PATH, "certs")
_FIXTURE_PATH = os.path.join(_TESTS_PATH, "fixtures", "pay/v3/")


@urlmatch(netloc=r"(.*\.)?api\.mch\.weixin\.qq\.com$")
def wechat_api_down_file_mock(url, request):
    res_file = os.path.join(_FIXTURE_PATH, "bill.xlsx")
    headers = {
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # 指定内容类型为纯文本
        "Content-Disposition": "attachment; filename=zd.xlsx",  # 可选，提示浏览器以文件下载的方式处理响应
    }
    try:
        bill_file = open(res_file, "rb")
        bill_file_bytes = bill_file.read()
    except (IOError, ValueError):
        pass
    return response(200, bill_file_bytes, headers, request=request)


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


class DownBillFileTestCase(unittest.TestCase):
    def setUp(self):
        self.client = WeChatPay(
            appid="11",
            apiv3_key="",
            mch_id="11",
            wechat_cert_dir=_CERTS_PATH,
            apiclient_cert_path=os.path.join(_CERTS_PATH, "apiclient_cert.pem"),
            apiclient_key_path=os.path.join(_CERTS_PATH, "apiclient_key.pem"),
            skip_check_signature=True,  # 测试无法校验证书
        )

    def test_trade_bill(self):
        with HTTMock(wechat_api_mock):
            response = self.client.ecommerce.trade_bill("2024-12-31")
            self.assertIn("hash_type", response)
            self.assertIn("hash_value", response)
            self.assertIn("download_url", response)

    def test_fund_flow_bill(self):
        with HTTMock(wechat_api_mock):
            response = self.client.ecommerce.fund_flow_bill("2024-12-31")
            self.assertIn("hash_type", response)
            self.assertIn("hash_value", response)
            self.assertIn("download_url", response)

    def test_profit_sharing_bill(self):
        with HTTMock(wechat_api_mock):
            response = self.client.ecommerce.profit_sharing_bill("2024-12-31")
            self.assertIn("hash_type", response)
            self.assertIn("hash_value", response)
            self.assertIn("download_url", response)

    def test_eco_fund_flow_bill(self):
        with HTTMock(wechat_api_mock):
            response = self.client.ecommerce.eco_fund_flow_bill("2024-12-31")
            self.assertIn("download_bill_count", response)
            self.assertIn("download_bill_list", response)

    def test_sub_mch_fund_flow_bill(self):
        with HTTMock(wechat_api_mock):
            response = self.client.ecommerce.sub_mch_fund_flow_bill(1657489417, "2024-12-31", "BASIC")
            self.assertIn("download_bill_count", response)
            self.assertIn("download_bill_list", response)

    def test_download_bill(self):
        with HTTMock(wechat_api_down_file_mock):
            response = self.client.ecommerce.download_bill("https://api.mch.weixin.qq.com/v3/billdownload/file")
            target_file_path = os.path.join(_FIXTURE_PATH, "downloadBill.xlsx")
            try:
                with open(target_file_path, "wb") as target_file:
                    target_file.write(response.content)
            except Exception as e:
                print(e)

    def test_download_bill_streamable(self):
        target_file_path = os.path.join(_FIXTURE_PATH, "downloadBill.xlsx")
        with HTTMock(wechat_api_down_file_mock):
            response = self.client.ecommerce.download_bill(
                "https://api.mch.weixin.qq.com/v3/billdownload/file", stream=True
            )
            for chunk in response.iter_content(chunk_size=10240):
                with open(target_file_path, "wb") as target_file:
                    target_file.write(chunk)
