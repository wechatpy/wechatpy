# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatService(BaseWeChatAPI):
    """
    应用授权（服务商、第三方应用开发相关）

    https://work.weixin.qq.com/api/doc#90001/90143/90597

    新的授权体系有部分接口未实现，欢迎提交 PR。
    """

    def get_provider_token(self, provider_secret):
        """
        获取服务商凭证

        https://work.weixin.qq.com/api/doc#90001/90143/91200

        :param provider_secret: 服务商的secret，在服务商管理后台可见
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'service/get_provider_token',
            data={
                'corpid': self._client.corp_id,
                'provider_secret': provider_secret,
            }
        )

    def get_suite_token(self, suite_id, suite_secret, suite_ticket):
        """
        获取第三方应用凭证

        https://work.weixin.qq.com/api/doc#90001/90143/9060

        :param suite_id: 以ww或wx开头应用id（对应于旧的以tj开头的套件id）
        :param suite_secret:  应用secret
        :param suite_ticket: 企业微信后台推送的ticket
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'service/get_suite_token',
            data={
                'suite_id': suite_id,
                'suite_secret': suite_secret,
                'suite_ticket': suite_ticket
            }
        )

    def get_login_info(self, auth_code, provider_access_token=None):
        """
        获取企业号登录用户信息

        详情请参考
        https://qydev.weixin.qq.com/wiki/index.php?title=获取企业号登录用户信息

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

    def get_login_url(self, login_ticket, target, agentid=None, provider_access_token=None):
        """
        获取登录企业号官网的url

        详情请参考
        https://qydev.weixin.qq.com/wiki/index.php?title=获取登录企业号官网的url

        :param provider_access_token: 服务提供商的 accesstoken
        :param login_ticket: 通过get_login_info得到的login_ticket, 10小时有效
        :param target: 登录跳转到企业号后台的目标页面
        :param agentid: 可选，授权方应用id
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'service/get_login_url',
            params={
                'provider_access_token': provider_access_token,
            },
            data={
                'login_ticket': login_ticket,
                'target': target,
                'agentid': agentid,
            }
        )
