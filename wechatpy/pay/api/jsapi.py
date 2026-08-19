# -*- coding: utf-8 -*-
import logging
import time

from wechatpy.pay.api.base import BaseWeChatPayAPI
from wechatpy.pay.utils import calculate_signature
from wechatpy.utils import random_string, to_text

logger = logging.getLogger(__name__)


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
            "appId": self.sub_appid or self.appid,
            "timeStamp": timestamp or to_text(int(time.time())),
            "nonceStr": nonce_str or random_string(32),
            "signType": "MD5",
            "package": f"prepay_id={prepay_id}",
        }
        return calculate_signature(
            data,
            self._client.api_key if not self._client.sandbox else self._client.sandbox_api_key,
        )

    def get_jsapi_params(self, prepay_id, timestamp=None, nonce_str=None, jssdk=False):
        """
        获取 JSAPI 参数

        :param prepay_id: 统一下单接口返回的 prepay_id 参数值
        :param timestamp: 可选，时间戳，默认为当前时间戳
        :param nonce_str: 可选，随机字符串，默认自动生成
        :param jssdk: 前端调用方式，默认使用 WeixinJSBridge
                      使用 jssdk 调起支付的话，timestamp 的 s 为小写
                      使用 WeixinJSBridge 调起支付的话，timeStamp 的 S 为大写
        :return: 参数
        """
        data = {
            "appId": self.sub_appid or self.appid,
            "timeStamp": timestamp or to_text(int(time.time())),
            "nonceStr": nonce_str or random_string(32),
            "signType": "MD5",
            "package": f"prepay_id={prepay_id}",
        }
        sign = calculate_signature(
            data,
            self._client.api_key if not self._client.sandbox else self._client.sandbox_api_key,
        )
        logger.debug("JSAPI payment parameters: data = %s, sign = %s", data, sign)
        data["paySign"] = sign
        if jssdk:
            data["timestamp"] = data.pop("timeStamp")
        return data
