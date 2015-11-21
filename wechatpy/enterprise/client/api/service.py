# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.client.api.base import BaseWeChatAPI


class WeChatService(BaseWeChatAPI):

    def get_provider_token(self, provider_secret):
        """
        获取应用提供商凭证

        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=获取应用提供商凭证

        :param provider_secret: 提供商的secret，在提供商管理页面可见
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'service/get_provider_token',
            data={
                'corpid': self._client.corp_id,
                'provider_secret': provider_secret,
            }
        )

    def get_login_info(self, provider_access_token, auth_code):
        """
        获取企业号管理员登录信息

        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=获取企业号管理员登录信息

        :param provider_access_token: 服务提供商的 accesstoken
        :param auth_code: OAuth 2.0 授权企业号管理员登录产生的 code
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'service/get_login_info',
            params={
                'provider_access_token': provider_access_token,
            },
            data={
                'auth_code': auth_code,
            }
        )
