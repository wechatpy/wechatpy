# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.pay.base import BaseWeChatPayAPI


class WeChatTools(BaseWeChatPayAPI):

    def short_url(self, long_url):
        """
        长链接转短链接

        :param long_url: 长链接
        :return: 返回的结果数据
        """
        data = {
            'appid': self.appid,
            'long_url': long_url,
        }
        return self._post('tools/shorturl', data=data)
