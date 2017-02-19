# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import time

from wechatpy.client.api.base import BaseWeChatAPI
from wechatpy.utils import WeChatSigner


class WeChatJSAPI(BaseWeChatAPI):

    def get_ticket(self):
        """
        获取微信 JS-SDK ticket

        http://qydev.weixin.qq.com/wiki/index.php?title=%E5%BE%AE%E4%BF%A1JS%E6%8E%A5%E5%8F%A3

        :return: 返回的 JSON 数据包
        """
        return self._get('get_jsapi_ticket')

    def get_jsapi_ticket(self):
        """
        获取微信 JS-SDK ticket

        该方法会通过 session 对象自动缓存管理 ticket

        :return: ticket
        """
        ticket_key = '{}_jsapi_ticket'.format(self._client.corp_id)
        expires_at_key = '{}_jsapi_ticket_expires_at'.format(self._client.corp_id)
        ticket = self.session.get(ticket_key)
        expires_at = self.session.get(expires_at_key, 0)
        if not ticket or expires_at < int(time.time()):
            jsapi_ticket = self.get_ticket()
            ticket = jsapi_ticket['ticket']
            expires_at = int(time.time()) + int(jsapi_ticket['expires_in'])
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
