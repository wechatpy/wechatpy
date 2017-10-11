# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import inspect
import logging

import requests
import xmltodict
from xml.parsers.expat import ExpatError
from optionaldict import optionaldict

from wechatpy.utils import random_string
from wechatpy.exceptions import WeChatPayException, InvalidSignatureException
from wechatpy.pay.utils import (
    calculate_signature, _check_signature, dict_to_xml
)
from wechatpy.pay.base import BaseWeChatPayAPI
from wechatpy.pay import api


logger = logging.getLogger(__name__)


def _is_api_endpoint(obj):
    return isinstance(obj, BaseWeChatPayAPI)


class WeChatPay(object):
    """
    微信支付接口

    :param appid: 微信公众号 appid
    :param api_key: 商户 key
    :param mch_id: 商户号
    :param sub_mch_id: 可选，子商户号，受理模式下必填
    :param mch_cert: 必填，商户证书路径
    :param mch_key: 必填，商户证书私钥路径
    """
    _http = requests.Session()

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

    API_BASE_URL = 'https://api.mch.weixin.qq.com/'

    def __new__(cls, *args, **kwargs):
        self = super(WeChatPay, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, _api in api_endpoints:
            api_cls = type(_api)
            _api = api_cls(self)
            setattr(self, name, _api)
        return self

    def __init__(self, appid, api_key, mch_id, sub_mch_id=None,
                 mch_cert=None, mch_key=None):
        """
        :param appid: 微信公众号 appid
        :param api_key: 商户 key
        :param mch_id: 商户号
        :param sub_mch_id: 可选，子商户号，受理模式下必填
        :param mch_cert: 商户证书路径
        :param mch_key: 商户证书私钥路径
        """
        self.appid = appid
        self.api_key = api_key
        self.mch_id = mch_id
        self.sub_mch_id = sub_mch_id
        self.mch_cert = mch_cert
        self.mch_key = mch_key

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = '{base}{endpoint}'.format(
                base=api_base_url,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        if isinstance(kwargs.get('data', ''), dict):
            data = optionaldict(kwargs['data'])
            if 'mchid' not in data:
                # Fuck Tencent
                data.setdefault('mch_id', self.mch_id)
            data.setdefault('sub_mch_id', self.sub_mch_id)
            data.setdefault('nonce_str', random_string(32))
            sign = calculate_signature(data, self.api_key)
            body = dict_to_xml(data, sign)
            body = body.encode('utf-8')
            kwargs['data'] = body

        # 商户证书
        if self.mch_cert and self.mch_key:
            kwargs['cert'] = (self.mch_cert, self.mch_key)

        res = self._http.request(
            method=method,
            url=url,
            **kwargs
        )
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise WeChatPayException(
                return_code=None,
                client=self,
                request=reqe.request,
                response=reqe.response
            )

        return self._handle_result(res)

    def _handle_result(self, res):
        res.encoding = 'utf-8'
        xml = res.text
        try:
            data = xmltodict.parse(xml)['xml']
        except (xmltodict.ParsingInterrupted, ExpatError):
            # 解析 XML 失败
            logger.debug('WeChat payment result xml parsing error', exc_info=True)
            return xml

        return_code = data['return_code']
        return_msg = data.get('return_msg')
        result_code = data.get('result_code')
        errcode = data.get('err_code')
        errmsg = data.get('err_code_des')
        if return_code != 'SUCCESS' or result_code != 'SUCCESS':
            # 返回状态码不为成功
            raise WeChatPayException(
                return_code,
                result_code,
                return_msg,
                errcode,
                errmsg,
                client=self,
                request=res.request,
                response=res
            )
        return data

    def get(self, url, **kwargs):
        return self._request(
            method='get',
            url_or_endpoint=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self._request(
            method='post',
            url_or_endpoint=url,
            **kwargs
        )

    def check_signature(self, params):
        return _check_signature(params, self.api_key)

    def parse_payment_result(self, xml):
        """解析微信支付结果通知"""
        try:
            data = xmltodict.parse(xml)
        except (xmltodict.ParsingInterrupted, ExpatError):
            raise InvalidSignatureException()

        if not data or 'xml' not in data:
            raise InvalidSignatureException()

        data = data['xml']
        sign = data.pop('sign', None)
        real_sign = calculate_signature(data, self.api_key)
        if sign != real_sign:
            raise InvalidSignatureException()

        for key in ('total_fee', 'settlement_total_fee', 'cash_fee', 'coupon_fee', 'coupon_count'):
            if key in data:
                data[key] = int(data[key])
        data['sign'] = sign
        return data
