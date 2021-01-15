# -*- coding: utf-8 -*-


from wechatpy.utils import to_text
from wechatpy.client.api.base import BaseWeChatAPI


class WeChatTag(BaseWeChatAPI):
    def create(self, name):
        """
        创建标签

        :param name: 标签名（30个字符以内）
        :return: 返回的 JSON 数据包

        """
        name = to_text(name)
        return self._post(
            "tags/create",
            data={"tag": {"name": name}},
            result_processor=lambda x: x["tag"],
        )

    def get(self):
        """
        获取公众号已创建的标签

        :return: 所有标签列表

        """

        res = self._get("tags/get", result_processor=lambda x: x["tags"])

        return res

    def update(self, tag_id, name):
        """
        编辑标签

        :param tag_id: 标签id，由微信分配
        :param name: 标签名字（30个字符以内）
        :return: 返回的 JSON 数据包

        """
        name = to_text(name)
        return self._post("tags/update", data={"tag": {"id": int(tag_id), "name": name}})

    def delete(self, tag_id):
        """
        删除标签

        :param tag_id: 标签 ID
        :return: 返回的 JSON 数据包

        """
        return self._post("tags/delete", data={"tag": {"id": tag_id}})

    def tag_user(self, tag_id, user_id):
        """
        批量为用户打标签

        :param tag_id: 标签 ID
        :param user_id: 用户 ID, 可以是单个或者列表

        :return: 返回的 JSON 数据包

        """
        data = {"tagid": tag_id}
        if isinstance(user_id, (tuple, list)):
            data["openid_list"] = user_id
        else:
            data["openid_list"] = [
                user_id,
            ]
        return self._post("tags/members/batchtagging", data=data)

    def untag_user(self, tag_id, user_id):
        """
        批量为用户取消标签

        :param tag_id: 标签 ID
        :param user_id: 用户 ID, 可以是单个或者列表

        :return: 返回的 JSON 数据包

        """
        data = {"tagid": tag_id}
        if isinstance(user_id, (tuple, list)):
            data["openid_list"] = user_id
        else:
            data["openid_list"] = [
                user_id,
            ]
        return self._post("tags/members/batchuntagging", data=data)

    def get_user_tag(self, user_id):
        """
        获取用户身上的标签列表

        :param user_id: 用户 ID, 可以是单个或者列表
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "tags/getidlist",
            data={"openid": user_id},
            result_processor=lambda x: x["tagid_list"],
        )

    def get_tag_users(self, tag_id, first_user_id=None):
        """
        获取标签下粉丝列表

        :param tag_id: 标签 ID
        :param first_user_id: 可选。第一个拉取的 OPENID，不填默认从头开始拉取
        :return: 返回的 JSON 数据包
        """
        data = {
            "tagid": tag_id,
        }
        if first_user_id:
            data["next_openid"] = first_user_id
        return self._post("user/tag/get", data=data)

    def iter_tag_users(self, tag_id, first_user_id=None):
        """
        获取标签下粉丝openid列表

        :return: 返回一个迭代器，可以用for进行循环，得到openid

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            for openid in client.tag.iter_tag_users(0):
                print(openid)

        """
        while True:
            follower_data = self.get_tag_users(tag_id, first_user_id)
            if "data" not in follower_data:
                return
            for openid in follower_data["data"]["openid"]:
                yield openid
            first_user_id = follower_data.get("next_openid")
            if not first_user_id:
                return

    def get_black_list(self, begin_openid=None):
        """
        获取公众号的黑名单列表
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1471422259_pJMWA

        :param begin_openid: 起始的 OpenID，传空则默认从头开始拉取
        :return: 返回的 JSON 数据包
        :rtype: dict
        """
        data = {}
        if begin_openid:
            data["begin_openid"] = begin_openid
        return self._post(
            "tags/members/getblacklist",
            data=data,
        )

    def batch_black_list(self, openid_list):
        """
        批量拉黑用户
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1471422259_pJMWA

        :param openid_list: 批量拉黑用户的 OpenID list, 最多20个
        :type openid_list: list
        """
        return self._post(
            "tags/members/batchblacklist",
            data={
                "openid_list": openid_list,
            },
        )

    def batch_unblack_list(self, openid_list):
        """
        批量取消拉黑
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1471422259_pJMWA

        :param openid_list: 批量取消拉黑的 OpenID list, 最多20个
        :type openid_list: list
        """
        return self._post(
            "tags/members/batchunblacklist",
            data={
                "openid_list": openid_list,
            },
        )
