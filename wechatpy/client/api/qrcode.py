# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import requests
import six

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatQRCode(BaseWeChatAPI):

    def create(self, qrcode_data):
        """
        创建二维码
        详情请参考
        http://mp.weixin.qq.com/wiki/18/28fc21e7ed87bec960651f0ce873ef8a.html

        :param data: 你要发送的参数 dict
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.qrcode.create({
                'expire_seconds': 1800,
                'action_name': 'QR_SCENE',
                'action_info': {
                    'scene': {'scene_id': 123},
                }
            })

        """
        return self._post(
            'qrcode/create',
            data=qrcode_data
        )

    def show(self, ticket):
        """
        通过ticket换取二维码
        详情请参考
        http://mp.weixin.qq.com/wiki/18/28fc21e7ed87bec960651f0ce873ef8a.html

        :param ticket: 二维码 ticket 。可以通过 :func:`create` 获取到
        :return: 返回的 Request 对象

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.qrcode.show('ticket data')

        """
        if isinstance(ticket, dict):
            ticket = ticket['ticket']
        return requests.get(
            url='https://mp.weixin.qq.com/cgi-bin/showqrcode',
            params={
                'ticket': ticket
            }
        )

    @classmethod
    def get_url(cls, ticket):
        """
        通过ticket换取二维码地址
        详情请参考
        http://mp.weixin.qq.com/wiki/18/28fc21e7ed87bec960651f0ce873ef8a.html

        :param ticket: 二维码 ticket 。可以通过 :func:`create` 获取到
        :return: 返回的二维码地址

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            url = client.qrcode.get_url('ticket data')

        """
        url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={ticket}'
        if isinstance(ticket, dict):
            ticket = ticket['ticket']
        ticket = six.moves.urllib.parse.quote(ticket)
        return url.format(ticket=ticket)
