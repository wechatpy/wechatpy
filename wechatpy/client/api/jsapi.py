# -*- coding: utf-8 -*-
"""
    wechatpy.client.jsapi
    ~~~~~~~~~~~~~~~~~~~~

    This module provides some APIs for JS SDK

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""


import hashlib
import time
from typing import Optional

from wechatpy.utils import WeChatSigner, random_string
from wechatpy.client.api.base import BaseWeChatAPI
from wechatpy.schemes import JsApiCardExt


class WeChatJSAPI(BaseWeChatAPI):
    def get_ticket(self, type="jsapi"):
        """
        获取微信 JS-SDK ticket

        :return: 返回的 JSON 数据包
        """
        return self._get("ticket/getticket", params={"type": type})

    def get_jsapi_ticket(self):
        """
        获取微信 JS-SDK ticket

        该方法会通过 session 对象自动缓存管理 ticket

        :return: ticket
        """
        ticket_key = f"{self.appid}_jsapi_ticket"
        expires_at_key = f"{self.appid}_jsapi_ticket_expires_at"
        ticket = self.session.get(ticket_key)
        expires_at = self.session.get(expires_at_key) or 0
        if not ticket or expires_at < int(time.time()):
            jsapi_ticket_response = self.get_ticket("jsapi")
            ticket = jsapi_ticket_response["ticket"]
            expires_at = int(time.time()) + int(jsapi_ticket_response["expires_in"])
            self.session.set(ticket_key, ticket)
            self.session.set(expires_at_key, expires_at)
        return ticket

    def get_jsapi_signature(self, noncestr, ticket, timestamp, url):
        """
        获取 JSAPI 签名

        :param noncestr: nonce string
        :param ticket: JS-SDK ticket
        :param timestamp: 时间戳
        :param url: URL
        :return: 签名
        """
        data = [
            f"noncestr={noncestr}",
            f"jsapi_ticket={ticket}",
            f"timestamp={timestamp}",
            f"url={url}",
        ]
        signer = WeChatSigner(delimiter=b"&")
        signer.add_data(*data)
        return signer.signature

    def get_jsapi_card_ticket(self):
        """
        获取 api_ticket：是用于调用微信卡券JS API的临时票据, 有效期为7200 秒, 通过access_token 来获取.
        微信文档地址：https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/JS-SDK.html#62
        该方法会通过 session 对象自动缓存管理 ticket

        :return: ticket
        """
        jsapi_card_ticket_key = f"{self.appid}_jsapi_card_ticket"
        jsapi_card_ticket_expire_at_key = f"{self.appid}_jsapi_card_ticket_expires_at"

        ticket = self.session.get(jsapi_card_ticket_key)
        expires_at = self.session.get(jsapi_card_ticket_expire_at_key, 0)
        if not ticket or int(expires_at) < int(time.time()):
            ticket_response = self.get_ticket("wx_card")
            ticket = ticket_response["ticket"]
            expires_at = int(time.time()) + int(ticket_response["expires_in"])
            self.session.set(jsapi_card_ticket_key, ticket)
            self.session.set(jsapi_card_ticket_expire_at_key, expires_at)
        return ticket

    def get_jsapi_add_card_params(
        self,
        card_id: str,
        code: str = "",
        openid: str = "",
        fixed_begintimestamp: Optional[int] = None,
        outer_str: str = "",
        nonce_str: str = "",
        timestamp: int = 0,
        card_ticket: str = "",
    ) -> JsApiCardExt:
        """
        用于生成 jsapi 批量添加卡券接口的 cardList 参数中的 cardExt 参数
        参数意义见微信文档地址：
            https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/JS-SDK.html#65 和
            https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/WeChat_Coupon_Interface.html#4
        :param card_id: 卡券ID. 一个卡券ID对应一类卡券, 包含了相应库存数量的Code码.
        :param code: 卡券Code码. 一张卡券的唯一标识, 核销卡券时使用此串码, 支持商户自定义.
        :param openid: 用户在该公众号下的唯一身份.
        :param fixed_begintimestamp: 卡券在第三方系统的实际领取时间, 为东八区时间戳 (UTC+8,精确到秒) . 当卡券的有效期类型为
                                     DATE_TYPE_FIX_TERM 时专用, 标识卡券的实际生效时间,
                                     用于解决商户系统内起始时间和领取时间不同步的问题.
        :param outer_str: 领取渠道参数, 用于标识本次领取的渠道值.  支持商户自定义场景值填入card_ext进行卡券投放,
                          当用户领取时会将相应场景值通过事件通知商户.
        :param nonce_str: 随机字符串, 由开发者设置传入, 加强安全性 (若不填写可能被重放请求).
        :param timestamp: unix 时间戳, 不同添加请求的时间戳须动态生成, 若重复将会导致领取失败.
        :param card_ticket: 用于卡券的微信 api_ticket

        :return: 卡券的附加信息 card_ext 的 dict
        """
        nonce_str = nonce_str or random_string()
        timestamp = timestamp or int(time.time())
        card_ticket = card_ticket or self.get_jsapi_card_ticket()

        card_signature_dict = {
            "nonce_str": nonce_str,
            "api_ticket": card_ticket,
            "timestamp": str(timestamp),
            "code": code,
            "openid": openid,
            "card_id": card_id,
        }
        list_before_sign = sorted([str(x) for x in card_signature_dict.values()])
        str_to_sign = "".join(list_before_sign).encode()
        card_ext = JsApiCardExt(
            code=code,
            openid=openid,
            timestamp=str(timestamp),
            fixed_begintimestamp=fixed_begintimestamp,
            outer_str=outer_str,
            nonce_str=nonce_str,
            signature=hashlib.sha1(str_to_sign).hexdigest(),
        )

        return card_ext
