# -*- coding: utf-8 -*-

from typing import Optional

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatTag(BaseWeChatAPI):
    """
    标签管理

    https://work.weixin.qq.com/api/doc#90000/90135/90209
    """

    def create(self, name: str, tag_id: Optional[int] = None) -> dict:
        """创建标签

        参考：https://work.weixin.qq.com/api/doc/90000/90135/90210

        **权限说明**： 创建的标签属于该应用，只有该应用才可以增删成员。

        **注意**： 标签总数不能超过3000个。

        返回结果示例: ::

            {
               "errcode": 0,
               "errmsg": "created"
               "tagid": 12
            }

        返回结果参数说明：

        +---------+------------------------+
        | 参数    | 说明                   |
        +=========+========================+
        | errcode | 返回码                 |
        +---------+------------------------+
        | errmsg  | 对返回码的文本描述内容 |
        +---------+------------------------+
        | tagid   | 标签id                 |
        +---------+------------------------+

        :param name: 标签名称，长度限制为32个字以内（汉字或英文字母），标签名不可与
        其他标签重名。
        :param tag_id: 标签id，非负整型，指定此参数时新增的标签会生成对应的标签id，不指
        定时则以目前最大的id自增。
        :return: 创建结果
        """
        if tag_id is not None and tag_id < 0:
            raise ValueError("tag id cannot be a negative integer")
        if len(name) > 32:
            raise ValueError("the length of the tag name cannot be more than 32 characters")

        data = {"tagname": name}
        if tag_id:
            data["tagid"] = tag_id
        return self._post("tag/create", data=data)

    def update(self, tag_id, name):
        return self._post("tag/update", data={"tagid": tag_id, "tagname": name})

    def delete(self, tag_id):
        return self._get("tag/delete", params={"tagid": tag_id})

    def get_users(self, tag_id):
        return self._get("tag/get", params={"tagid": tag_id})

    def add_users(self, tag_id, user_ids):
        return self._post("tag/addtagusers", data={"tagid": tag_id, "userlist": user_ids})

    def delete_users(self, tag_id, user_ids):
        return self._post("tag/deltagusers", data={"tagid": tag_id, "userlist": user_ids})

    def list(self):
        res = self._get("tag/list")
        return res["taglist"]
