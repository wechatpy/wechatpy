# -*- coding: utf-8 -*-


from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatKF(BaseWeChatAPI):
    """
    微信客服接口

    https://work.weixin.qq.com/api/doc/90000/90135/94670
    """

    def sync_msg(self, token, cursor="", limit=1000):
        """
        微信客户发送的消息、接待人员在企业微信回复的消息、发送消息接口发送失败事件（如被用户拒收）
        、客户点击菜单消息的回复消息，可以通过该接口获取具体的消息内容和事件。不支持读取通过发送消息接口发送的消息。
        支持的消息类型：文本、图片、语音、视频、文件、位置、链接、名片、小程序、事件。


        :param token: 回调事件返回的token字段，10分钟内有效；可不填，如果不填接口有严格的频率限制。不多于128字节
        :param cursor: 上一次调用时返回的next_cursor，第一次拉取可以不填。不多于64字节
        :param limit: 期望请求的数据量，默认值和最大值都为1000。
        注意：可能会出现返回条数少于limit的情况，需结合返回的has_more字段判断是否继续请求。
        :return: 接口调用结果
        """
        data = {
            "token": token,
            "cursor": cursor,
            "limit": limit,
        }
        return self._post("kf/sync_msg", data=data)

    def get_service_state(self, open_kfid, external_userid):
        """
        获取会话状态

        ID	状态	说明
        0	未处理	新会话接入。可选择：1.直接用API自动回复消息。2.放进待接入池等待接待人员接待。3.指定接待人员进行接待
        1	由智能助手接待	可使用API回复消息。可选择转入待接入池或者指定接待人员处理。
        2	待接入池排队中	在待接入池中排队等待接待人员接入。可选择转为指定人员接待
        3	由人工接待	人工接待中。可选择结束会话
        4	已结束	会话已经结束。不允许变更会话状态，等待用户重新发起咨询

        :param open_kfid: 客服帐号ID
        :param external_userid: 微信客户的external_userid
        :return: 接口调用结果
        """
        data = {
            "open_kfid": open_kfid,
            "external_userid": external_userid,
        }
        return self._post("kf/service_state/get", data=data)

    def trans_service_state(self, open_kfid, external_userid, service_state, servicer_userid=""):
        """
        变更会话状态

        :param open_kfid: 客服帐号ID
        :param external_userid: 微信客户的external_userid
        :param service_state: 当前的会话状态，状态定义参考概述中的表格
        :return: 接口调用结果
        """
        data = {
            "open_kfid": open_kfid,
            "external_userid": external_userid,
            "service_state": service_state,
        }
        if servicer_userid:
            data['servicer_userid'] = servicer_userid
        return self._post("kf/service_state/trans", data=data)

    def get_servicer_list(self, open_kfid):
        """
        获取接待人员列表

        :param open_kfid: 客服帐号ID
        :return: 接口调用结果
        """
        data = {
            "open_kfid": open_kfid,
        }
        return self._get("kf/servicer/list", params=data)

    def add_servicer(self, open_kfid, userid_list):
        """
        添加接待人员
        添加指定客服帐号的接待人员。

        :param open_kfid: 客服帐号ID
        :param userid_list: 接待人员userid列表
        :return: 接口调用结果
        """
        if not isinstance(userid_list, list):
            userid_list = [userid_list]

        data = {
            "open_kfid": open_kfid,
            "userid_list": userid_list,
        }
        return self._post("kf/servicer/add", data=data)

    def del_servicer(self, open_kfid, userid_list):
        """
        删除接待人员
        从客服帐号删除接待人员

        :param open_kfid: 客服帐号ID
        :param userid_list: 接待人员userid列表
        :return: 接口调用结果
        """
        if not isinstance(userid_list, list):
            userid_list = [userid_list]

        data = {
            "open_kfid": open_kfid,
            "userid_list": userid_list,
        }
        return self._post("kf/servicer/del", data=data)

    def batchget_customer(self, external_userid_list):
        """
        客户基本信息获取

        :param external_userid_list: external_userid列表
        :return: 接口调用结果
        """
        if not isinstance(external_userid_list, list):
            external_userid_list = [external_userid_list]

        data = {
            "external_userid_list": external_userid_list,
        }
        return self._post("kf/customer/batchget", data=data)

    def get_account_list(self):
        """
        获取客服帐号列表

        :return: 接口调用结果
        """
        return self._get("kf/account/list")