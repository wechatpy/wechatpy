# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatWxa(BaseWeChatAPI):

    API_BASE_URL = 'https://api.weixin.qq.com/'

    def create_code(self, path, width=430, auth_color=False, line_color={"r": "0", "g": "0", "b": "0"}):
        """
        创建普通二维码
        详情请参考
        https://mp.weixin.qq.com/debug/wxadoc/dev/api/qrcode.html

        """
        return self._post(
            'cgi-bin/wxaapp/createwxaqrcode',
            data={
                'path': path,
                'width': width,
                'auth_color': auth_color,
                'line_color': line_color,
            }
        )

    def create_wxa_code(self, path, width=430):
        """
        创建小程序码
        详情请参考
        https://mp.weixin.qq.com/debug/wxadoc/dev/api/qrcode.html

        """
        return self._post(
            'wxa/getwxacode',
            data={
                'path': path,
                'width': width,
            }
        )

    def send_template_message(self, user_id, template_id, data, form_id, page=None, color=None, emphasis_keyword=None):
        """
        发送模板消息

        详情请参考
        https://mp.weixin.qq.com/debug/wxadoc/dev/api/notice.html
        """
        tpl_data = optionaldict(
            touser=user_id,
            template_id=template_id,
            page=page,
            form_id=form_id,
            data=data,
            color=color,
            emphasis_keyword=emphasis_keyword,
        )
        return self._post(
            'cgi-bin/message/wxopen/template/send',
            data=tpl_data
        )
