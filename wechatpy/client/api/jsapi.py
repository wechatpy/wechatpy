# -*- coding: utf-8 -*-
"""
    wechatpy.client.jsapi
    ~~~~~~~~~~~~~~~~~~~~

    This module provides some APIs for JS SDK

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import time

from wechatpy.utils import WeChatSigner
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
        ticket = self.session.get('jsapi_ticket')
        expires_at = self.session.get('jsapi_ticket_expires_at', 0)
        if not ticket or expires_at < int(time.time()):
            jsapi_ticket = self.get_ticket('jsapi')
            ticket = jsapi_ticket['ticket']
            expires_at = int(time.time()) + int(jsapi_ticket['expires_in'])
            self.session.set('jsapi_ticket', ticket)
            self.session.set('jsapi_ticket_expires_at', expires_at)
        return ticket

    def get_jsapi_signature(self, noncestr, ticket, timestamp, url):
        data = [
            'noncestr={noncestr}'.format(noncestr=noncestr),
            'jsapi_ticket={ticket}'.format(ticket=ticket),
            'timestamp={timestamp}'.format(timestamp=timestamp),
            'url={url}'.format(url=url),
        ]
        signer = WeChatSigner(delimiter=b'&')
        signer.add_data(*data)
        return signer.signature
