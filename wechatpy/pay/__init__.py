# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import sys
import inspect

import requests
import xmltodict
from xml.parsers.expat import ExpatError
from optionaldict import optionaldict

from wechatpy.utils import random_string
from wechatpy.exceptions import WeChatPayException
from wechatpy.pay.utils import (
    calculate_signature, _check_signature, dict_to_xml
)
from wechatpy.pay.base import BaseWeChatPayAPI
from wechatpy.pay import api


def _is_api_endpoint(obj):
    return isinstance(obj, BaseWeChatPayAPI)


class WeChatPay(object):
    """
    微信红包接口

    :param appid: 微信公众号 appid
    :param api_key: 商户 key
    :param mch_id: 商户号
    :param sub_mch_id: 可选，子商户号，受理模式下必填
    :param mch_cert: 必填，商户证书路径
    :param mch_key: 必填，商户证书私钥路径
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
    """刷卡支付接口"""
    micropay = api.WeChatMicroPay()
    """退款接口"""
    tools = api.WeChatTools()
    """工具类接口"""
    jsapi = api.WeChatJSAPI()

    API_BASE_URL = 'https://api.mch.weixin.qq.com/'

    def __new__(cls, *args, **kwargs):
        self = super(WeChatPay, cls).__new__(cls)
        if sys.version_info[:2] == (2, 6):
            import copy
            # Python 2.6 inspect.gemembers bug workaround
            # http://bugs.python.org/issue1785
            for name, _api in self.__class__.__dict__.items():
                if isinstance(_api, BaseWeChatPayAPI):
                    _api = copy.deepcopy(_api)
                    _api._client = self
                    setattr(self, name, _api)
        else:
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

        res = requests.request(
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
