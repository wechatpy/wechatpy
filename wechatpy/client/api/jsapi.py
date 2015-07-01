# -*- coding: utf-8 -*-
"""
    wechatpy.client.jsapi
    ~~~~~~~~~~~~~~~~~~~~

    This module provides some APIs for JS SDK

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals

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
