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

    def link_wxamp(self, appid, notify_users=0, show_profile=1):
        """
        关联小程序
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&id=open1513255108_gFkRI&token=&lang=zh_CN

        :param appid:小程序appid
        :param notify_users:是否发送模板消息通知公众号粉丝
        :param show_profile:是否展示公众号主页中
        :return:
        """
        return self._post(
            "cgi-bin/wxopen/wxamplink",
            data={
                "appid": appid,
                "notify_users": notify_users,
                "show_profile": show_profile
            }
        )

    def unlink_wxamp(self, appid):
        """
        解除已关联的小程序
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&id=open1513255108_gFkRI&token=&lang=zh_CN
        :param appid:小程序appid
        :return:
        """
        return self._post(
            "cgi-bin/wxopen/wxampunlink",
            data={
                "appid": appid,
            }
        )
