# -*- coding: utf-8 -*-

from urllib.parse import quote

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatOAuth(BaseWeChatAPI):
    OAUTH_BASE_URL = "https://open.weixin.qq.com/connect/oauth2/authorize"

    def authorize_url(self, redirect_uri, state=None, agent_id=None, scope="snsapi_base"):
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
            "&agentid=",
            agent_id,
            f"&response_type=code&scope={scope}",
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

    def get_user_detail(self,ticket):
        """
        获取用户敏感信息

        https://developer.work.weixin.qq.com/document/path/95833
        :param ticket: 用户OAuth授权后拿到的票据
        :return: 包含敏感信息的用户信息
        """

        return self._post(
            "auth/getuserdetail",
            data={
                "user_ticket": ticket
            }
        )
