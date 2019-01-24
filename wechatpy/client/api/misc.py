# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMisc(BaseWeChatAPI):

    def short_url(self, long_url):
        """
        将一条长链接转成短链接
        详情请参考
        http://mp.weixin.qq.com/wiki/10/165c9b15eddcfbd8699ac12b0bd89ae6.html

        :param long_url: 长链接地址
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.misc.short_url('http://www.qq.com')

        """
        return self._post(
            'shorturl',
            data={
                'action': 'long2short',
                'long_url': long_url
            }
        )

    def get_wechat_ips(self):
        """
        获取微信服务器 IP 地址列表

        :return: IP 地址列表

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            ips = client.misc.get_wechat_ips()

        """
        res = self._get(
            'getcallbackip',
            result_processor=lambda x: x['ip_list']
        )
        return res
