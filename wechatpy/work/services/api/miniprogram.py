# -*- coding: utf-8 -*-


from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMiniProgram(BaseWeChatAPI):
    """
    小程序接口（服务商、第三方应用开发相关）

    https://work.weixin.qq.com/api/doc/90001/90144/92423

    新的授权体系有部分接口未实现，欢迎提交 PR。
    """

    def jscode2session(self, js_code):
        """
        临时登录凭证校验接口

        详情请参考
        https://work.weixin.qq.com/api/doc/90001/90143/90603
        :param js_code: 登录时获取的 code
        :return: 返回的 JSON 数据包
        """
        return self._get(
            "service/miniprogram/jscode2session",
            params={"js_code": js_code, "grant_type": "authorization_code"},
        )
