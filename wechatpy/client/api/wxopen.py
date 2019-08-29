#!/usr/bin/python
# -*- encoding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatWeOpen(BaseWeChatAPI):
    API_BASE_URL = 'https://api.weixin.qq.com/'

    def get_wxamp_link(self):
        """
        获取公众号关联的小程序
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&id=open1513255108_gFkRI&token=&lang=zh_CN
        """
        return self._post(
            'cgi-bin/wxopen/wxamplinkget',
            data={}
        )
