#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatShakeAround(BaseWeChatAPI):

    def get_shake_info(self, ticket):
        """
        获取摇周边的设备及用户信息
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=获取设备及用户信息
        :param ticket: 摇周边业务的ticket，可在摇到的 URL 中得到，ticket 生效时间为30分钟
        :return: 设备及用户信息
        """
        res = self._post(
            'shakearound/getshakeinfo',
            data={
                'ticket': ticket
            }
        )
        return res['data']
