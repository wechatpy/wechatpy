# -*- coding: utf-8 -*-
"""
    wechatpy.client.jsapi
    ~~~~~~~~~~~~~~~~~~~~

    This module provides some APIs for JS SDK

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals

import hashlib
import time

from wechatpy.utils import WeChatSigner, random_string
from wechatpy.client.api.base import BaseWeChatAPI


class WeChatJSAPI(BaseWeChatAPI):

    def get_ticket(self, type='jsapi'):
        """
        获取微信 JS-SDK ticket

        :return: 返回的 JSON 数据包
        """
        return self._get(
            'ticket/getticket',
            params={'type': type}
        )

    def get_jsapi_ticket(self):
        """
        获取微信 JS-SDK ticket

        该方法会通过 session 对象自动缓存管理 ticket

        :return: ticket
        """
        ticket_key = '{0}_jsapi_ticket'.format(self.appid)
        expires_at_key = '{0}_jsapi_ticket_expires_at'.format(self.appid)
        ticket = self.session.get(ticket_key)
        expires_at = self.session.get(expires_at_key, 0)
        if not ticket or expires_at < int(time.time()):
            jsapi_ticket_response = self.get_ticket('jsapi')
            ticket = jsapi_ticket_response['ticket']
            expires_at = int(time.time()) + int(jsapi_ticket_response['expires_in'])
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
            'noncestr={noncestr}'.format(noncestr=noncestr),
            'jsapi_ticket={ticket}'.format(ticket=ticket),
            'timestamp={timestamp}'.format(timestamp=timestamp),
            'url={url}'.format(url=url),
        ]
        signer = WeChatSigner(delimiter=b'&')
        signer.add_data(*data)
        return signer.signature

    def get_jsapi_card_ticket(self):
        """
        获取 api_ticket：是用于调用微信卡券JS API的临时票据，有效期为7200 秒，通过access_token 来获取。
        微信文档地址：http://mp.weixin.qq.com/wiki/7/aaa137b55fb2e0456bf8dd9148dd613f.html
        该方法会通过 session 对象自动缓存管理 ticket

        :return: ticket
        """
        jsapi_card_ticket_key = '{0}_jsapi_card_ticket'.format(self.appid)
        jsapi_card_ticket_expire_at_key = '{0}_jsapi_card_ticket_expires_at'.format(self.appid)

        ticket = self.session.get(jsapi_card_ticket_key)
        expires_at = self.session.get(jsapi_card_ticket_expire_at_key, 0)
        if not ticket or expires_at < int(time.time()):
            ticket_response = self.get_ticket('wx_card')
            ticket = ticket_response['ticket']
            expires_at = int(time.time()) + int(ticket_response['expires_in'])
            self.session.set(jsapi_card_ticket_key, ticket)
            self.session.set(jsapi_card_ticket_expire_at_key, expires_at)
        return ticket

    def get_jsapi_card_params(self, card_ticket, card_type, **kwargs):
        """
        参数意义见微信文档地址：http://mp.weixin.qq.com/wiki/7/aaa137b55fb2e0456bf8dd9148dd613f.html
        :param card_ticket: 用于卡券的微信 api_ticket
        :param card_type: 
        :param kwargs: 非必须参数：noncestr, timestamp, code, openid, fixed_begintimestamp, outer_str
        :return: 包含调用jssdk所有所需参数的 dict
        """
        card_signature_dict = {
            'card_type': card_type,
            'noncestr': kwargs.get('noncestr', random_string()),
            'api_ticket': card_ticket,
            'appid': self.appid,
            'timestamp': kwargs.get('timestamp', str(int(time.time()))),
        }
        list_before_sign = sorted([str(x) for x in card_signature_dict.values()])
        str_to_sign = "".join(list_before_sign).encode()
        card_signature_dict['sign'] = hashlib.sha1(str_to_sign).hexdigest()
        return card_signature_dict
