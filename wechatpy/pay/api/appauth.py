# -*- coding: utf-8 -*-
from urllib.parse import quote
from typing import Any, Dict

from wechatpy.pay import calculate_signature_hmac
from wechatpy.pay.api.base import BaseWeChatPayAPI


class WeChatAppAuth(BaseWeChatPayAPI):
    """微信支付实名认证接口"""

    def get_auth_url(self, redirect_uri: str, state: str) -> str:
        """
        获取实名认证授权重定向地址，如果用户同意授权，页面将跳转至 `redirect_uri/?code=CODE&state=STATE`；
        code 作为换取 access_token 的票据，每次用户授权带上的 code 将不一样，code 只能使用一次，10分钟未被使用自动过期。

        详情请参考 https://pay.weixin.qq.com/wiki/doc/api/realnameauth.php?chapter=60_1&index=2

        :param redirect_uri: 重定向地址，自动 urlencode，需在支付安全域下(商户平台上配置“支付授权目录”)
        :param state: 随机字符串，回调时将带上该参数
        """
        redirect_uri = quote(redirect_uri, safe=b"")
        url_parts = [
            "https://payapp.weixin.qq.com/appauth/authindex?mch_id=",
            self.mch_id,
            "&appid=",
            self.appid,
            "&redirect_uri=",
            redirect_uri,
            "&response_type=code&scope=pay_identity&state=",
            state,
            "#wechat_redirect",
        ]
        return "".join(url_parts)

    def get_access_token(self, openid: str, code: str) -> Dict[str, Any]:
        """
        获取微信用户的授权, 用授权小程序得到的授权码调用 OAuth2.0 接口 access_token

        :param openid: 用户 openid
        :param code: 预授权码
        """
        params = {
            "mch_id": self.mch_id,
            "appid": self.appid,
            "openid": openid,
            "code": code,
            "scope": "pay_identity",
            "grant_type": "authorization_code",
            "sign_type": "HMAC-SHA256",
        }
        sign = calculate_signature_hmac(params, self._client.api_key)
        params["sign"] = sign
        res = self._get(
            "appauth/getaccesstoken",
            params=params,
        )
        return res

    def real_name_auth(self, openid: str, real_name: str, cred_id: str, access_token: str) -> Dict[str, Any]:
        """
        取得 access_token 后调用本接口验证微信用户的姓名和身份证信息是否匹配

        :param openid: 用户 openid
        :param real_name: 真实姓名
        :param cred_id: 身份证号码
        :param access_token: 获取用户授权后换取的 access_token
        """
        return self._post(
            "https://fraud.mch.weixin.qq.com/secsvc/realnameauth",
            data={
                "version": "1.0",
                "appid": self.appid,
                "openid": openid,
                "real_name": real_name,
                "cred_type": 1,
                "cred_id": cred_id,
                "access_token": access_token,
                "sign_type": "HMAC-SHA256",
            },
        )
