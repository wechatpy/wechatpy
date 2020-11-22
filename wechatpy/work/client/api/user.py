# -*- coding: utf-8 -*-

from typing import Optional

from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatUser(BaseWeChatAPI):
    """
    成员管理

    https://work.weixin.qq.com/api/doc#90000/90135/90194

    邀请成员接口位于 `WeChatBatch.invite`
    """

    def create(
        self,
        user_id,
        name,
        department=None,
        position=None,
        mobile=None,
        gender=0,
        tel=None,
        email=None,
        weixin_id=None,
        extattr=None,
        **kwargs,
    ):
        """
        创建成员

        https://work.weixin.qq.com/api/doc#90000/90135/90195
        """
        user_data = optionaldict()
        user_data["userid"] = user_id
        user_data["name"] = name
        user_data["gender"] = gender
        user_data["department"] = department
        user_data["position"] = position
        user_data["mobile"] = mobile
        user_data["tel"] = tel
        user_data["email"] = email
        user_data["weixinid"] = weixin_id
        user_data["extattr"] = extattr
        user_data.update(kwargs)

        return self._post("user/create", data=user_data)

    def get(self, user_id):
        """
        读取成员

        https://work.weixin.qq.com/api/doc#90000/90135/90196
        """
        return self._get("user/get", params={"userid": user_id})

    def update(
        self,
        user_id,
        name=None,
        department=None,
        position=None,
        mobile=None,
        gender=None,
        tel=None,
        email=None,
        weixin_id=None,
        enable=None,
        extattr=None,
        **kwargs,
    ):
        """
        更新成员

        https://work.weixin.qq.com/api/doc#90000/90135/90197
        """
        user_data = optionaldict()
        user_data["userid"] = user_id
        user_data["name"] = name
        user_data["gender"] = gender
        user_data["department"] = department
        user_data["position"] = position
        user_data["mobile"] = mobile
        user_data["tel"] = tel
        user_data["email"] = email
        user_data["weixinid"] = weixin_id
        user_data["extattr"] = extattr
        user_data["enable"] = enable
        user_data.update(kwargs)

        return self._post("user/update", data=user_data)

    def delete(self, user_id):
        """
        删除成员

        https://work.weixin.qq.com/api/doc#90000/90135/90198
        """
        return self._get("user/delete", params={"userid": user_id})

    def batch_delete(self, user_ids):
        """
        批量删除成员

        https://work.weixin.qq.com/api/doc#90000/90135/90199
        """
        return self._post("user/batchdelete", data={"useridlist": user_ids})

    def list(self, department_id, fetch_child=False, status=0, simple=False):
        """
        批量获取部门成员 / 批量获取部门成员详情

        https://work.weixin.qq.com/api/doc#90000/90135/90200
        https://work.weixin.qq.com/api/doc#90000/90135/90201

        此接口和 `WeChatDepartment.get_users` 是同一个接口，区别为 simple 的默认值不同。
        """
        url = "user/simplelist" if simple else "user/list"
        res = self._get(
            url,
            params={
                "department_id": department_id,
                "fetch_child": 1 if fetch_child else 0,
                "status": status,
            },
        )
        return res["userlist"]

    def convert_to_openid(self, user_id, agent_id=None):
        """
        user_id 转成 openid

        https://work.weixin.qq.com/api/doc#90000/90135/90202

        :param user_id: 企业微信内的成员 ID
        :param agent_id: 可选，需要发送红包的应用ID，若只是使用微信支付和企业转账，则无需该参数
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(userid=user_id, agentid=agent_id)
        return self._post("user/convert_to_openid", data=data)

    def convert_to_user_id(self, openid):
        """
        openid 转成 user_id

        https://work.weixin.qq.com/api/doc#90000/90135/90202

        :param openid: 在使用微信支付、微信红包和企业转账之后，返回结果的openid
        :return: 该 openid 在企业微信中对应的成员 user_id
        """
        res = self._post("user/convert_to_userid", data={"openid": openid})
        return res["userid"]

    def verify(self, user_id):
        """
        二次验证

        https://work.weixin.qq.com/api/doc#90000/90135/90203

        :param user_id: 成员UserID。对应管理端的帐号
        """
        return self._get("user/authsucc", params={"userid": user_id})

    def get_join_qrcode(self, size_type: Optional[int] = None) -> str:
        """
        获取加入企业二维码

        该接口用于获取企业用户实时成员加入的二维码。详细接口细节请查看 `接口文档`_。

        需要注意的是获取到的二维码链接，**有效期为7天**。

        :param size_type: 图片尺寸类型。可用尺寸有：
            1: 171 x 171;
            2: 399 x 399;
            3: 741 x 741（默认）;
            4: 2052 x 2052
        :return: 二维码链接

        .. _接口文档: https://work.weixin.qq.com/api/doc/90000/90135/91714

        .. warning:: 使用本接口请确保开启了 **通讯录同步** 的API接口同步，并使用
          **通讯录同步** 的 ``secret``，否则调用接口时会出现错误。
        """
        params = optionaldict(size_type=size_type)
        resp = self._get("corp/get_join_qrcode", params=params)
        return resp["join_qrcode"]

    def get_active_stat(self, date: str) -> int:
        """
        获取企业活跃成员数

        该接口用于获取指定日期的企业的成员活跃数量，详细接口细节请查看 `接口文档`_。

        :param date: 具体某天的活跃人数，最长支持获取30天前数据。格式为: ``YYYY-MM-DD``。
        :return: 成员活跃数量

        .. _接口文档:: https://work.weixin.qq.com/api/doc/90000/90135/92714

        .. warning:: 仅通讯录同步助手可调用。
        """
        resp = self._post("user/get_active_stat", data={"date": date})
        return resp["active_cnt"]
