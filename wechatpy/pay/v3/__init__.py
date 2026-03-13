# -*- coding: utf-8 -*-
import datetime
import inspect
import json
import logging
import os
import time
from urllib.parse import urlparse, urlencode

import cryptography
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate

from wechatpy.exceptions import InvalidSignatureException, WeChatPayV3Exception
from wechatpy.pay.v3.api.base import BaseWeChatPayAPI
from wechatpy.pay.utils import (
    calculate_signature_rsa,
    check_rsa_signature,
    aes_decrypt,
    rsa_public_encrypt,
    calculate_pay_params_signature_rsa,
    get_serial_no,
)
from wechatpy.utils import random_string, to_text
from wechatpy.pay.v3 import api

logger = logging.getLogger(__name__)


def _is_api_endpoint(obj):
    return isinstance(obj, BaseWeChatPayAPI)


class WeChatPay:
    """
    微信支付接口

    :param appid: 微信公众号 appid
    :param sub_appid: 当前调起支付的小程序APPID
    :param apiv3_key: 商户 api v3 密钥，商户平台下载
    :param mch_id: 商户号
    :param sub_mchid: 可选，子商户号，受理模式下必填
    :param apiclient_cert_path: 必填，商户证书路径
    :param apiclient_key_path: 必填，商户证书私钥路径
    :param wechat_cert_dir: 必填，微信证书保存文件夹
    :param timeout: 可选，请求超时时间，单位秒，默认无超时设置
    """

    # 媒体文件接口
    media = api.WeChatMedia()
    # 订单接口
    partner_order = api.WeChatPartnerOrder()
    # 银行信息接口
    banks = api.WeChatBanks()
    # 电商收付通接口
    ecommerce = api.WeChatEcommerce()

    API_BASE_URL = "https://api.mch.weixin.qq.com/v3/"

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, _api in api_endpoints:
            api_cls = type(_api)
            _api = api_cls(self)
            setattr(self, name, _api)
        return self

    def __init__(
        self,
        appid,
        apiv3_key,
        mch_id,
        apiclient_cert_path=None,
        apiclient_key_path=None,
        wechat_cert_dir=None,
        timeout=None,
        sub_appid=None,
        skip_check_signature=False,
    ):
        self.appid = appid
        self.sub_appid = sub_appid
        self.apiv3_key = apiv3_key
        self.mch_id = mch_id
        self.apiclient_cert_path = apiclient_cert_path
        self.apiclient_key_path = apiclient_key_path
        self.wechat_cert_dir = wechat_cert_dir
        self.timeout = timeout
        self.skip_check_signature = skip_check_signature
        self._http = requests.Session()

        # 证书内存缓存
        self.wechat_cert_dict = {}
        self.load_wechat_cert()

        with open(self.apiclient_key_path, "rb") as f:
            self.apiclient_key = f.read()
        with open(self.apiclient_cert_path, "rb") as f:
            self.apiclient_cert = f.read()

        pem_x509 = cryptography.x509.load_pem_x509_certificate(self.apiclient_cert)
        self.serial_no = get_serial_no(pem_x509)

    def download_file(self, url, method="get", headers=None, **kwargs):
        nonce_str = random_string(32).upper()
        timestamp = str(int(time.time()))
        sign = calculate_signature_rsa(
            self.apiclient_key,
            method,
            url,
            "",
            nonce_str=nonce_str,
            timestamp=timestamp,
        )
        authorization = (
            f'WECHATPAY2-SHA256-RSA2048 mchid="{self.mch_id}",nonce_str="{nonce_str}",signature="{sign}",'
            f'timestamp="{timestamp}",serial_no="{self.serial_no}"'
        )
        headers = headers or {}
        headers.update(
            {
                "Authorization": authorization,
                "Accept": "application/json",
            }
        )
        kwargs["timeout"] = kwargs.get("timeout", self.timeout)
        logger.debug("Request to WeChat API: %s %s\n%s", method, url, kwargs)
        res = self._http.request(method=method, url=url, headers=headers, **kwargs)
        res_code = res.status_code
        res_text = res.text
        if res_code != 200:
            if res_code == 401:
                raise InvalidSignatureException(res_code, res_text)
            # 返回状态码不为成功
            raise WeChatPayV3Exception(res_code, res_text)
        return res

    def _request(self, method, url_or_endpoint, headers=None, sign_data=None, skip_check_signature=False, **kwargs):
        if not url_or_endpoint.startswith(("http://", "https://")):
            api_base_url = kwargs.pop("api_base_url", self.API_BASE_URL)
            url = f"{api_base_url}{url_or_endpoint}"
        else:
            url = url_or_endpoint

        params = kwargs.get("params")
        url_parse = urlparse(url)
        if params:
            endpoint = url_parse.path + "?" + urlencode(params)
        else:
            endpoint = url_parse.path

        nonce_str = random_string(32).upper()
        timestamp = str(int(time.time()))
        sign_data = sign_data or kwargs.get("json")
        sign = calculate_signature_rsa(
            self.apiclient_key,
            method,
            endpoint,
            json.dumps(sign_data) if sign_data else "",
            nonce_str=nonce_str,
            timestamp=timestamp,
        )
        authorization = (
            f'WECHATPAY2-SHA256-RSA2048 mchid="{self.mch_id}",nonce_str="{nonce_str}",signature="{sign}",'
            f'timestamp="{timestamp}",serial_no="{self.serial_no}"'
        )

        headers = headers or {}
        headers.update(
            {
                "Authorization": authorization,
                "Accept": "application/json",
            }
        )
        if skip_check_signature is False and self.skip_check_signature is False:
            # 跳过，首次获取证书的时候不需要这个
            headers.update({"Wechatpay-Serial": get_serial_no(self._get_wechat_cert())})

        kwargs["timeout"] = kwargs.get("timeout", self.timeout)
        logger.debug("Request to WeChat API: %s %s\n%s", method, url, kwargs)
        res = self._http.request(method=method, url=url, headers=headers, **kwargs)
        return self._handle_result(res, skip_check_signature)

    def _handle_result(self, res, skip_check_signature):
        logger.debug("Response from WeChat API \n %s", res.text)

        # 无内容返回
        if res.status_code == 204:
            return {}

        try:
            data = res.json()
        except json.JSONDecodeError:
            # 解析 json 失败
            logger.debug("WeChat payment result json parsing error", exc_info=True)
            return res.text

        code = data.get("code")
        message = data.get("message")
        if code:
            if code == "SIGN_ERROR":
                raise InvalidSignatureException(code, message)
            # 返回状态码不为成功
            raise WeChatPayV3Exception(code, message)

        if self.skip_check_signature is False and self.check_response_signature(res.headers, res.text) is False:
            raise InvalidSignatureException()

        return data

    def get(self, url, **kwargs):
        return self._request(method="get", url_or_endpoint=url, **kwargs)

    def post(self, url, **kwargs):
        return self._request(method="post", url_or_endpoint=url, **kwargs)

    def update_certificates(self, skip_check_signature=False):
        """
        获取证书，该接口需要定期执行

        :param: skip_check_signature: 首次下载证书需要跳过签名，或请提前使用微信工具下载证书
        :return: 返回的结果数据
        """
        if not self.wechat_cert_dir:
            raise WeChatPayV3Exception(code=0, message="请设置微信证书存储目录(wechat_cert_dir)")

        # 首次使用需要下载证书，跳过校验签名
        response = self.get("certificates", skip_check_signature=skip_check_signature)

        cert_list = response.get("data")
        for cert in cert_list:
            serial_no = cert.get("serial_no")
            encrypt_certificate = cert.get("encrypt_certificate")
            nonce = encrypt_certificate.get("nonce")
            ciphertext = encrypt_certificate.get("ciphertext")
            associated_data = encrypt_certificate.get("associated_data")
            cert_str = aes_decrypt(nonce, ciphertext, associated_data, self.apiv3_key)

            new_cert = cryptography.x509.load_pem_x509_certificate(cert_str.encode())
            now = datetime.datetime.utcnow()
            # 跳过证书过期
            if now < new_cert.not_valid_before or now > new_cert.not_valid_after:
                continue
            # 验证序列号
            if serial_no != get_serial_no(new_cert):
                continue
            cert_path = self.get_cert_path(serial_no)
            if not os.path.exists(cert_path):
                with open(cert_path, "w") as f:
                    f.write(cert_str)
            self.wechat_cert_dict[serial_no] = new_cert

    def get_cert_path(self, serial_no):
        return os.path.join(self.wechat_cert_dir, "wechatpay_" + serial_no + ".pem")

    def load_wechat_cert(self):
        dirs = os.listdir(self.wechat_cert_dir)
        for file in dirs:
            if file.startswith("wechatpay_"):
                # 读取证书并缓存
                with open(os.path.join(self.wechat_cert_dir, file), "rb") as f:
                    cert_file = f.read()
                serial_no = file.replace("wechatpay_", "").replace(".pem", "")
                certificate = load_pem_x509_certificate(data=cert_file, backend=default_backend())
                self.wechat_cert_dict[serial_no] = certificate

    def _get_wechat_cert(self):
        if len(self.wechat_cert_dict.keys()) == 0:
            raise WeChatPayV3Exception(code=0, message="请先加载微信证书")
        certificate = list(self.wechat_cert_dict.values())[0]
        return certificate

    def rsa_encrypt_data(self, data):
        certificate = self._get_wechat_cert()
        return rsa_public_encrypt(data, certificate)

    def calculate_pay_params_signature_rsa(self, app_id, package, timestamp=None, nonce_str=None):
        """支付参数rsa签名"""
        return calculate_pay_params_signature_rsa(self.apiclient_key, app_id, package, timestamp, nonce_str)

    def check_response_signature(self, headers, response_body):
        """校验微信响应签名"""
        timestamp = headers.get("Wechatpay-Timestamp")
        nonce_str = headers.get("Wechatpay-Nonce")
        signature = headers.get("Wechatpay-Signature")
        serial_no = headers.get("Wechatpay-Serial")

        certificate = self.wechat_cert_dict.get(serial_no)
        if not certificate:
            cert_path = self.get_cert_path(serial_no)
            if not os.path.exists(cert_path):
                raise WeChatPayV3Exception(code=0, message="微信证书不存在，请手动更新证书并跳过签名验证")

            # 读取证书并缓存
            with open(cert_path, "rb") as f:
                cert_file = f.read()

            certificate = load_pem_x509_certificate(data=cert_file, backend=default_backend())
            self.wechat_cert_dict[serial_no] = certificate

        return check_rsa_signature(certificate, timestamp, nonce_str, response_body, signature)

    def parse_message(self, message) -> dict:
        """
        解析回调结果
        :param message: 微信返回的原始内容
        :return: 解密结果
        """
        if not message:
            return {}
        if isinstance(message, bytes):
            message = json.loads(to_text(message))

        # 解密数据
        decrypt_data = {}
        resource = message.get("resource")
        if resource.get("algorithm") == "AEAD_AES_256_GCM":
            nonce = resource.get("nonce")
            ciphertext = resource.get("ciphertext")
            associated_data = resource.get("associated_data")
            encrypt_data = aes_decrypt(nonce, ciphertext, associated_data, self.apiv3_key)
            decrypt_data = json.loads(encrypt_data)
        return decrypt_data
