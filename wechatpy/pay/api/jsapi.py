# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import time

from wechatpy.utils import random_string, to_text
from wechatpy.pay.base import BaseWeChatPayAPI
from wechatpy.pay.utils import calculate_signature


class WeChatJSAPI(BaseWeChatPayAPI):

    def get_jsapi_signature(self, prepay_id, timestamp=None, nonce_str=None):
        """
        获取 JSAPI 签名

        :param prepay_id: 统一下单接口返回的 prepay_id 参数值
        :param timestamp: 可选，时间戳，默认为当前时间戳
        :param nonce_str: 可选，随机字符串，默认自动生成
        :return: 签名
        """
        data = {
            'appId': self.appid,
            'timeStamp': timestamp or to_text(int(time.time())),
            'nonceStr': nonce_str or random_string(32),
            'signType': 'MD5',
            'package': 'prepay_id={0}'.format(prepay_id),
        }
        return calculate_signature(data, self._client.api_key)

    def get_jsapi_params(self, prepay_id, timestamp=None, nonce_str=None):
        """
        获取 JSAPI 参数

        :param prepay_id: 统一下单接口返回的 prepay_id 参数值
        :param timestamp: 可选，时间戳，默认为当前时间戳
        :param nonce_str: 可选，随机字符串，默认自动生成
        :return: 签名
        """
        data = {
            'appId': self.appid,
            'timeStamp': timestamp or to_text(int(time.time())),
            'nonceStr': nonce_str or random_string(32),
            'signType': 'MD5',
            'package': 'prepay_id={0}'.format(prepay_id),
        }
        sign = calculate_signature(data, self._client.api_key)
        data['paySign'] = sign
        return data
