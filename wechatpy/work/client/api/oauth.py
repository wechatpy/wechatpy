# -*- coding: utf-8 -*-

from urllib.parse import quote

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatOAuth(BaseWeChatAPI):
    OAUTH_BASE_URL = "https://open.weixin.qq.com/connect/oauth2/authorize"

    def authorize_url(self, redirect_uri, state=None):
        """
        构造网页授权链接
        详情请参考
        https://work.weixin.qq.com/api/doc#90000/90135/91022

        :param redirect_uri: 授权后重定向的回调链接地址
        :param state: 重定向后会带上 state 参数
        :return: 返回的 JSON 数据包
        """
        redirect_uri = quote(redirect_uri, safe=b"")
        url_list = [
            self.OAUTH_BASE_URL,
            "?appid=",
            self._client.corp_id,
            "&redirect_uri=",
            redirect_uri,
            "&response_type=code&scope=snsapi_base",
        ]
        if state:
            url_list.extend(["&state=", state])
        url_list.append("#wechat_redirect")
        return "".join(url_list)

    def get_user_info(self, code):
        """
        获取访问用户身份
        详情请参考
        https://work.weixin.qq.com/api/doc#90000/90135/91023

        :param code: 通过成员授权获取到的code
        :return: 返回的 JSON 数据包
        """

        return self._get(
            "user/getuserinfo",
            params={
                "code": code,
            },
        )
