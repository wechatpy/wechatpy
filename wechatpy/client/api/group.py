# -*- coding: utf-8 -*-


from wechatpy.utils import to_text
from wechatpy.client.api.base import BaseWeChatAPI


class WeChatGroup(BaseWeChatAPI):
    def create(self, name):
        """
        创建分组

        详情请参考
        http://mp.weixin.qq.com/wiki/0/56d992c605a97245eb7e617854b169fc.html

        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.group.create('New Group')

        """
        name = to_text(name)
        return self._post("groups/create", data={"group": {"name": name}})

    def get(self, user_id=None):
        """
        查询所有分组或查询用户所在分组 ID

        详情请参考
        http://mp.weixin.qq.com/wiki/0/56d992c605a97245eb7e617854b169fc.html

        :param user_id: 用户 ID，提供时查询该用户所在分组，否则查询所有分组
        :return: 所有分组列表或用户所在分组 ID

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            group = client.group.get('openid')

        """
        if user_id is None:
            res = self._get("groups/get", result_processor=lambda x: x["groups"])
        else:
            res = self._post(
                "groups/getid",
                data={"openid": user_id},
                result_processor=lambda x: x["groupid"],
            )
        return res

    def update(self, group_id, name):
        """
        修改分组名

        详情请参考
        http://mp.weixin.qq.com/wiki/0/56d992c605a97245eb7e617854b169fc.html

        :param group_id: 分组id，由微信分配
        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.group.update(1234, 'New Name')

        """
        name = to_text(name)
        return self._post("groups/update", data={"group": {"id": int(group_id), "name": name}})

    def move_user(self, user_id, group_id):
        """
        移动用户分组

        详情请参考
        http://mp.weixin.qq.com/wiki/0/56d992c605a97245eb7e617854b169fc.html

        :param user_id: 用户 ID, 可以是单个或者列表，为列表时为批量移动用户分组
        :param group_id: 分组 ID
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.group.move_user('openid', 1234)

        """
        data = {"to_groupid": group_id}
        if isinstance(user_id, (tuple, list)):
            endpoint = "groups/members/batchupdate"
            data["openid_list"] = user_id
        else:
            endpoint = "groups/members/update"
            data["openid"] = user_id
        return self._post(endpoint, data=data)

    def delete(self, group_id):
        """
        删除分组

        详情请参考
        http://mp.weixin.qq.com/wiki/0/56d992c605a97245eb7e617854b169fc.html

        :param group_id: 分组 ID
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.group.delete(1234)

        """
        return self._post("groups/delete", data={"group": {"id": group_id}})
