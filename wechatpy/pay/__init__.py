# -*- coding: utf-8 -*-

import inspect
import logging

import requests
import xmltodict
from xml.parsers.expat import ExpatError
from optionaldict import optionaldict

from wechatpy.crypto import WeChatRefundCrypto
from wechatpy.utils import random_string
from wechatpy.exceptions import WeChatPayException, InvalidSignatureException
from wechatpy.pay.utils import (
    calculate_signature,
    calculate_signature_hmac,
    _check_signature,
    dict_to_xml,
)
from wechatpy.pay.api.base import BaseWeChatPayAPI
from wechatpy.pay import api

logger = logging.getLogger(__name__)


def _is_api_endpoint(obj):
    return isinstance(obj, BaseWeChatPayAPI)


class WeChatPay:
    """
    微信支付接口

    :param appid: 微信公众号 appid
    :param sub_appid: 当前调起支付的小程序APPID
    :param api_key: 商户 key,不要在这里使用小程序的密钥
    :param mch_id: 商户号
    :param sub_mch_id: 可选，子商户号，受理模式下必填
    :param mch_cert: 必填，商户证书路径
    :param mch_key: 必填，商户证书私钥路径
    :param timeout: 可选，请求超时时间，单位秒，默认无超时设置
    :param sandbox: 可选，是否使用测试环境，默认为 False
    """

    redpack = api.WeChatRedpack()
    """红包接口"""
    transfer = api.WeChatTransfer()
    """企业付款接口"""
    coupon = api.WeChatCoupon()
    """代金券接口"""
    order = api.WeChatOrder()
    """订单接口"""
    refund = api.WeChatRefund()
    """退款接口"""
    micropay = api.WeChatMicroPay()
    """刷卡支付接口"""
    tools = api.WeChatTools()
    """工具类接口"""
    jsapi = api.WeChatJSAPI()
    """公众号网页 JS 支付接口"""
    withhold = api.WeChatWithhold()
    """代扣接口"""
    app_auth = api.WeChatAppAuth()
    """实名认证接口"""

    API_BASE_URL = "https://api.mch.weixin.qq.com/"

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
        api_key,
        mch_id,
        sub_mch_id=None,
        mch_cert=None,
        mch_key=None,
        timeout=None,
        sandbox=False,
        sub_appid=None,
    ):
        self.appid = appid
        self.sub_appid = sub_appid
        self.api_key = api_key
        self.mch_id = mch_id
        self.sub_mch_id = sub_mch_id
        self.mch_cert = mch_cert
        self.mch_key = mch_key
        self._using_pkcs12_cert = False
        self.timeout = timeout
        self.sandbox = sandbox
        self._sandbox_api_key = None
        self._http = requests.Session()
        if mch_cert and mch_cert.endswith(".p12"):
            from requests_pkcs12 import Pkcs12Adapter

            # 商户 .p12 格式证书，证书密码默认为商户 ID
            self._http.mount(
                self.API_BASE_URL, Pkcs12Adapter(pkcs12_filename=self.mch_cert, pkcs12_password=self.mch_id)
            )
            self._using_pkcs12_cert = True

    def _fetch_sandbox_api_key(self):
        nonce_str = random_string(32)
        sign = calculate_signature({"mch_id": self.mch_id, "nonce_str": nonce_str}, self.api_key)
        payload = dict_to_xml(
            {
                "mch_id": self.mch_id,
                "nonce_str": nonce_str,
            },
            sign=sign,
        )
        headers = {"Content-Type": "text/xml"}
        api_url = f"{self.API_BASE_URL}sandboxnew/pay/getsignkey"
        response = self._http.post(api_url, data=payload, headers=headers)
        return xmltodict.parse(response.text)["xml"].get("sandbox_signkey")

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(("http://", "https://")):
            api_base_url = kwargs.pop("api_base_url", self.API_BASE_URL)
            if self.sandbox:
                api_base_url = f"{api_base_url}sandboxnew/"
            url = f"{api_base_url}{url_or_endpoint}"
        else:
            url = url_or_endpoint

        if isinstance(kwargs.get("data", ""), dict):
            data = kwargs["data"]
            if "mchid" not in data:
                # Fuck Tencent
                data.setdefault("mch_id", self.mch_id)
            data.setdefault("sub_mch_id", self.sub_mch_id)
            data.setdefault("nonce_str", random_string(32))
            data = optionaldict(data)

            if data.get("sign_type", "MD5") == "HMAC-SHA256":
                sign = calculate_signature_hmac(data, self.sandbox_api_key if self.sandbox else self.api_key)
            else:
                sign = calculate_signature(data, self.sandbox_api_key if self.sandbox else self.api_key)
            body = dict_to_xml(data, sign)
            body = body.encode("utf-8")
            kwargs["data"] = body

        # 商户 PEM 证书
        if not self._using_pkcs12_cert and self.mch_cert and self.mch_key:
            kwargs["cert"] = (self.mch_cert, self.mch_key)

        kwargs["timeout"] = kwargs.get("timeout", self.timeout)
        logger.debug("Request to WeChat API: %s %s\n%s", method, url, kwargs)
        res = self._http.request(method=method, url=url, **kwargs)
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise WeChatPayException(
                return_code=None,
                client=self,
                request=reqe.request,
                response=reqe.response,
            )

        return self._handle_result(res)

    def _handle_result(self, res):
        res.encoding = "utf-8-sig"
        xml = res.text
        logger.debug("Response from WeChat API \n %s", xml)
        try:
            data = xmltodict.parse(xml)["xml"]
        except (xmltodict.ParsingInterrupted, ExpatError):
            # 解析 XML 失败
            logger.debug("WeChat payment result xml parsing error", exc_info=True)
            return xml

        return_code = data["return_code"]
        return_msg = data.get("return_msg", data.get("retmsg"))
        result_code = data.get("result_code", data.get("retcode"))
        errcode = data.get("err_code")
        errmsg = data.get("err_code_des")
        if return_code != "SUCCESS" or result_code != "SUCCESS":
            # 返回状态码不为成功
            raise WeChatPayException(
                return_code,
                result_code,
                return_msg,
                errcode,
                errmsg,
                client=self,
                request=res.request,
                response=res,
            )
        return data

    def get(self, url, **kwargs):
        return self._request(method="get", url_or_endpoint=url, **kwargs)

    def post(self, url, **kwargs):
        return self._request(method="post", url_or_endpoint=url, **kwargs)

    def check_signature(self, params):
        return _check_signature(params, self.api_key if not self.sandbox else self.sandbox_api_key)

    @classmethod
    def get_payment_data(cls, xml):
        """
        解析微信支付结果通知，获得appid, mch_id, out_trade_no, transaction_id
        如果你需要进一步判断，请先用appid, mch_id来生成WeChatPay,
        然后用`wechatpay.parse_payment_result(xml)`来校验支付结果

        使用示例::

            from wechatpy.pay import WeChatPay
            # 假设你已经获取了微信服务器推送的请求中的xml数据并存入xml变量
            data = WeChatPay.get_payment_appid(xml)
            {
                "appid": "公众号或者小程序的id",
                "mch_id": "商户id",
            }

        """
        try:
            data = xmltodict.parse(xml)
        except (xmltodict.ParsingInterrupted, ExpatError):
            raise ValueError("invalid xml")
        if not data or "xml" not in data:
            raise ValueError("invalid xml")
        data = data["xml"]
        return {
            "appid": data["appid"],
            "mch_id": data["mch_id"],
            "out_trade_no": data["out_trade_no"],
            "transaction_id": data["transaction_id"],
        }

    def parse_payment_result(self, xml):
        """解析微信支付结果通知"""
        try:
            data = xmltodict.parse(xml)
        except (xmltodict.ParsingInterrupted, ExpatError):
            raise InvalidSignatureException()

        if not data or "xml" not in data:
            raise InvalidSignatureException()

        data = data["xml"]
        sign = data.pop("sign", None)
        real_sign = calculate_signature(data, self.api_key if not self.sandbox else self.sandbox_api_key)
        if sign != real_sign:
            raise InvalidSignatureException()

        for key in (
            "total_fee",
            "settlement_total_fee",
            "cash_fee",
            "coupon_fee",
            "coupon_count",
        ):
            if key in data:
                data[key] = int(data[key])
        data["sign"] = sign
        return data

    def parse_refund_notify_result(self, xml):
        """解析微信退款结果通知"""
        refund_crypto = WeChatRefundCrypto(self.api_key if not self.sandbox else self.sandbox_api_key)
        data = refund_crypto.decrypt_message(xml, self.appid, self.mch_id)
        for key in (
            "total_fee",
            "settlement_total_fee",
            "refund_fee",
            "settlement_refund_fee",
        ):
            if key in data:
                data[key] = int(data[key])
        return data

    @property
    def sandbox_api_key(self):
        if self.sandbox and self._sandbox_api_key is None:
            self._sandbox_api_key = self._fetch_sandbox_api_key()

        return self._sandbox_api_key
