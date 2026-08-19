# -*- coding: utf-8 -*-


from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatAgent(BaseWeChatAPI):
    """应用管理
    https://work.weixin.qq.com/api/doc#90000/90135/90226
    """

    def get(self, agent_id):
        """
        获取指定的应用详情
        https://work.weixin.qq.com/api/doc#90000/90135/90227/获取指定的应用详情/

        :param agent_id: 应用id
        :return: 返回的 JSON 数据包
        """
        return self._get("agent/get", params={"agentid": agent_id})

    def list(self):
        """
        获取access_token对应的应用列表
        https://work.weixin.qq.com/api/doc#90000/90135/90227/获取access_token对应的应用列表/

        :return: 应用概况列表
        """
        res = self._get("agent/list")
        return res["agentlist"]

    def set(
        self,
        agent_id,
        name=None,
        description=None,
        redirect_domain=None,
        logo_media_id=None,
        report_location_flag=0,
        is_report_user=True,
        is_report_enter=True,
    ):
        """
        设置应用
        https://work.weixin.qq.com/api/doc#90000/90135/90228

        :param agent_id: 企业应用的id
        :param name: 企业应用名称，长度不超过32个utf8字符
        :param description: 企业应用详情，长度为4至120个utf8字符
        :param redirect_domain: 企业应用可信域名。注意：域名需通过所有权校验，否则jssdk功能将受限，此时返回错误码85005
        :param logo_media_id: 企业应用头像的mediaid，通过素材管理接口上传图片获得mediaid，上传后会自动裁剪成方形和圆形两个头像
        :param report_location_flag: 企业应用是否打开地理位置上报 0：不上报；1：进入会话上报；
        :param is_report_enter: 是否上报用户进入应用事件。0：不接收；1：接收。
        :param is_report_user: 是否接收用户变更通知。0：不接收；1：接收。
        :return: 返回的 JSON 数据包
        """
        agent_data = optionaldict()
        agent_data["agentid"] = agent_id
        agent_data["name"] = name
        agent_data["description"] = description
        agent_data["redirect_domain"] = redirect_domain
        agent_data["logo_mediaid"] = logo_media_id
        agent_data["report_location_flag"] = report_location_flag
        agent_data["isreportenter"] = 1 if is_report_enter else 0
        agent_data["isreportuser"] = 1 if is_report_user else 0
        return self._post("agent/set", data=agent_data)
