# encoding: utf-8
from __future__ import absolute_import, unicode_literals
import six

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatOAuth(BaseWeChatAPI):

    OAUTH_BASE_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize'

    def authorize_url(self, redirect_uri, state=None):
        """
        获取授权地址
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=OAuth%E9%AA%8C%E8%AF%81%E6%8E%A5%E5%8F%A3

        :param redirect_uri: 授权后重定向的回调链接地址
        :param state: 重定向后会带上 state 参数
        :return: 返回的 JSON 数据包
        """
        redirect_uri = six.moves.urllib.parse.quote(redirect_uri, safe='')
        url_list = [
            self.OAUTH_BASE_URL,
            '?appid=',
            self._client.corp_id,
            '&redirect_uri=',
            redirect_uri,
            '&response_type=code&scope=snsapi_base',
        ]
        if state:
            url_list.extend(['&state=', state])
        url_list.append('#wechat_redirect')
        return ''.join(url_list)

    def get_user_info(self, code):
        """
        根据 code 获取用户信息
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=OAuth%E9%AA%8C%E8%AF%81%E6%8E%A5%E5%8F%A3

        :param code: 通过成员授权获取到的code
        :return: 返回的 JSON 数据包
        """

        return self._get(
            'user/getuserinfo',
            params={
                'code': code,
            }
        )
