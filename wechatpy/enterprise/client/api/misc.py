# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMisc(BaseWeChatAPI):

    def get_wechat_ips(self):
        """
        获取微信服务器 IP 列表

        :return: IP 地址列表
        """
        res = self._get('getcallbackip')
        return res['ip_list']
