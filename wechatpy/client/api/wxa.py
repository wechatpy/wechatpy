# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatWxa(BaseWeChatAPI):

    API_BASE_URL = 'https://api.weixin.qq.com/'

    def create_qrcode(self, path, width=430):
        """
        创建小程序二维码（接口C：适用于需要的码数量较少的业务场景）
        详情请参考
        https://mp.weixin.qq.com/debug/wxadoc/dev/api/qrcode.html

        """
        return self._post(
            'cgi-bin/wxaapp/createwxaqrcode',
            data={
                'path': path,
                'width': width
            }
        )

    def get_wxa_code(self, path, width=430, auto_color=False, line_color={"r": "0", "g": "0", "b": "0"}):
        """
        创建小程序码（接口A: 适用于需要的码数量较少的业务场景）
        详情请参考
        https://mp.weixin.qq.com/debug/wxadoc/dev/api/qrcode.html

        """
        return self._post(
            'wxa/getwxacode',
            data={
                'path': path,
                'width': width,
                'auto_color': auto_color,
                'line_color': line_color,
            }
        )

    def get_wxa_code_unlimited(self, scene, width=430, auto_color=False, line_color={"r": "0", "g": "0", "b": "0"}):
        """
        创建小程序码（接口B：适用于需要的码数量极多，或仅临时使用的业务场景）
        详情请参考
        https://mp.weixin.qq.com/debug/wxadoc/dev/api/qrcode.html

        """
        return self._post(
            'wxa/getwxacodeunlimit',
            data={
                'scene': scene,
                'width': width,
                'auto_color': auto_color,
                'line_color': line_color,
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
