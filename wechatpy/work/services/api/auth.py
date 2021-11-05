# -*- coding: utf-8 -*-


from wechatpy.client.api.base import BaseWeChatAPI


class WeChatAuth(BaseWeChatAPI):
    """
    应用授权（服务商、第三方应用开发相关）

    https://work.weixin.qq.com/api/doc/90001/90143/90597

    新的授权体系有部分接口未实现，欢迎提交 PR。
    """

    def get_pre_auth_code(self):
        """
        获取预授权码

        详情请参考
        https://open.work.weixin.qq.com/api/doc/90001/90143/90601
        :return: 返回的 JSON 数据包
        """
        return self._get(
            "service/get_pre_auth_code",
        )

    def set_session_info(self, pre_auth_code, app_id=None, auth_type=0):
        """
        设置授权配置

        详情请参考
        https://open.work.weixin.qq.com/api/doc/90001/90143/90602
        :param pre_auth_code: 预授权码
        :param app_id: 允许进行授权的应用id，如1、2、3， 不填或者填空数组都表示允许授权套件内所有应用
                       （仅旧的多应用套件可传此参数，新开发者可忽略）
        :param auth_type: 授权类型：0 正式授权， 1 测试授权。 默认值为0。注意，请确保应用在正式发布后的授权类型为“正式授权”
        :return: 返回的 JSON 数据包
        """
        session_info = {"auth_type": auth_type}
        if app_id:
            session_info["appid"] = app_id
        return self._post(
            "service/set_session_info",
            data={"pre_auth_code": pre_auth_code, "session_info": session_info},
        )

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
