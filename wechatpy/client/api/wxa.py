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

    def modify_domain(self, action, request_domain=(), wsrequest_domain=(), upload_domain=(), download_domain=()):
        """
        修改小程序服务器授权域名

        :param action: 增删改查的操作类型，仅支持 'add', 'delete', 'set', 'get'
        :param request_domain: request 合法域名
        :param wsrequest_domain: socket 合法域名
        :param upload_domain: upload file 合法域名
        :param download_domain: download file 合法域名
        """
        return self._post(
            'wxa/modify_domain',
            data={
                'action': action,
                'requestdomain': request_domain,
                'wsrequestdomain': wsrequest_domain,
                'upload_domain': upload_domain,
                'download_domain': download_domain,
            }
        )

    def bind_tester(self, wechat_id):
        """
        绑定微信用户成为小程序体验者

        :param wechat_id: 微信号
        """
        return self._post(
            'wxa/bind_tester',
            data={
                'wechatid': wechat_id,
            }
        )

    def unbind_tester(self, wechat_id):
        """
        解除绑定小程序的体验者

        :param wechat_id: 微信号
        """
        return self._post(
            'wxa/unbind_tester',
            data={
                'wechatid': wechat_id,
            }
        )

    def commit(self, template_id, ext_json, version, description):
        """
        为授权的小程序账号上传小程序代码

        :param template_id: 代码库中的代码模版 ID
        :param ext_json: 第三方自定义的配置
        :param version: 代码版本号，开发者可自定义
        :param description: 代码描述，开发者可自定义
        """
        return self._post(
            'wxa/commit',
            data={
                'template_id': template_id,
                'ext_json': ext_json,
                'user_version': version,
                'user_desc': description,
            }
        )

    def create_open(self, appid):
        """
        创建开放平台账号，并绑定公众号/小程序

        :param appid: 授权公众号或小程序的 appid
        :return: 开放平台的 appid
        """
        return self._post(
            'cgi-bin/open/create',
            data={
                'appid': appid,
            },
            result_processor=lambda x: x['open_appid'],
        )

    def get_open(self, appid):
        """
        获取公众号/小程序所绑定的开放平台账号

        :param appid: 授权公众号或小程序的 appid
        :return: 开放平台的 appid
        """
        return self._post(
            'cgi-bin/open/get',
            data={
                'appid': appid,
            },
            result_processor=lambda x: x['open_appid'],
        )

    def bind_open(self, appid, open_appid):
        """
        将公众号/小程序绑定到开放平台帐号下

        :param appid: 授权公众号或小程序的 appid
        :param open_appid: 开放平台帐号 appid
        """
        return self._post(
            'cgi-bin/open/bind',
            data={
                'appid': appid,
                'open_appid': open_appid,
            }
        )

    def unbind_open(self, appid, open_appid):
        """
        将公众号/小程序绑定到开放平台帐号下

        :param appid: 授权公众号或小程序的 appid
        :param open_appid: 开放平台帐号 appid
        """
        return self._post(
            'cgi-bin/open/unbind',
            data={
                'appid': appid,
                'open_appid': open_appid,
            }
        )
