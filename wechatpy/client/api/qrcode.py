# -*- coding: utf-8 -*-

from urllib.parse import quote

import requests

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatQRCode(BaseWeChatAPI):
    def create(self, qrcode_data):
        """
        创建二维码
        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1443433542

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
            # 创建永久的二维码, 参数使用字符串而不是数字id
            res = client.qrcode.create({
                'action_name': 'QR_LIMIT_STR_SCENE',
                'action_info': {
                    'scene': {'scene_str': "scan_qrcode_from_scene"},
                }
            })

        """
        return self._post("qrcode/create", data=qrcode_data)

    def show(self, ticket):
        """
        通过ticket换取二维码
        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1443433542

        :param ticket: 二维码 ticket 。可以通过 :func:`create` 获取到
        :return: 返回的 Request 对象

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.qrcode.show('ticket data')

        """
        if isinstance(ticket, dict):
            ticket = ticket["ticket"]
        return requests.get(url="https://mp.weixin.qq.com/cgi-bin/showqrcode", params={"ticket": ticket})

    @classmethod
    def get_url(cls, ticket):
        """
        通过ticket换取二维码地址
        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1443433542

        :param ticket: 二维码 ticket 。可以通过 :func:`create` 获取到
        :return: 返回的二维码地址

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            url = client.qrcode.get_url('ticket data')

        """
        if isinstance(ticket, dict):
            ticket = ticket["ticket"]
        ticket = quote(ticket)
        return f"https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={ticket}"
