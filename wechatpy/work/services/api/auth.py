# -*- coding: utf-8 -*-


from wechatpy.client.api.base import BaseWeChatAPI


class WeChatAuth(BaseWeChatAPI):
    """
    应用授权（服务商、第三方应用开发相关）

    https://work.weixin.qq.com/api/doc/90001/90143/90597

    新的授权体系有部分接口未实现，欢迎提交 PR。
    """

    def get_permanent_code(self, auth_code):
        """
        获取企业永久授权码

        详情请参考
        https://work.weixin.qq.com/api/doc/90001/90143/90603
        :param auth_code: 临时授权码，会在授权成功时附加在redirect_uri中跳转回第三方服务商网站，或通过回调推送给服务商。长度为64至512个字节
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "service/get_permanent_code",
            data={
                "auth_code": auth_code,
            },
        )

    def get_auth_info(self, auth_code, permanent_code):
        """
        获取企业授权信息

        详情请参考
        https://work.weixin.qq.com/api/doc/10975
        :param auth_code: 临时授权码，会在授权成功时附加在redirect_uri中跳转回第三方服务商网站，或通过回调推送给服务商。长度为64至512个字节
        :param permanent_code: 	永久授权码，通过get_permanent_code获取
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "service/get_auth_info",
            data={
                "auth_code": auth_code,
                "permanent_code": permanent_code,
            },
        )
