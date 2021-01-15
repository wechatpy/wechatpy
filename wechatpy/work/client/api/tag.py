# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatTag(BaseWeChatAPI):
    """
    标签管理

    https://work.weixin.qq.com/api/doc#90000/90135/90209
    """

    @staticmethod
    def _validate_tag_id(tag_id):
        if tag_id < 0:
            raise ValueError("tag id cannot be a negative integer")

    @staticmethod
    def _validate_tag_name(tag_name):
        if len(tag_name) > 32:
            raise ValueError("the length of the tag name cannot be more than 32 characters")

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
        if tag_id is not None:
            self._validate_tag_id(tag_id)
        self._validate_tag_name(name)

        data: Dict[str, Any] = {"tagname": name}
        if tag_id:
            data["tagid"] = tag_id
        return self._post("tag/create", data=data)

    def update(self, tag_id: int, name: str) -> dict:
        """更新标签名字

        参考：https://work.weixin.qq.com/api/doc/90000/90135/90211

        **权限说明**：调用的应用必须是指定标签的创建者。

        返回结果示例： ::

            {
               "errcode": 0,
               "errmsg": "updated"
            }

        结果参数说明：

        +---------+------------------------+
        | 参数    | 说明                   |
        +=========+========================+
        | errcode | 返回码                 |
        +---------+------------------------+
        | errmsg  | 对返回码的文本描述内容 |
        +---------+------------------------+

        :param tag_id: 标签ID
        :param name: 标签名称，长度限制为32个字（汉字或英文字母），标签不可与其他标签重名。
        :return: 更新结果
        """
        self._validate_tag_id(tag_id)
        self._validate_tag_name(name)

        return self._post("tag/update", data={"tagid": tag_id, "tagname": name})

    def delete(self, tag_id: int) -> dict:
        """删除标签

        参考：https://work.weixin.qq.com/api/doc/90000/90135/90212

        **权限说明**：调用的应用必须是指定标签的创建者。

        返回结果示例： ::

            {
               "errcode": 0,
               "errmsg": "deleted"
            }

        结果参数说明：

        +---------+------------------------+
        | 参数    | 说明                   |
        +=========+========================+
        | errcode | 返回码                 |
        +---------+------------------------+
        | errmsg  | 对返回码的文本描述内容 |
        +---------+------------------------+

        :param tag_id: 标签ID，非负整型
        :return: 删除结果
        """
        self._validate_tag_id(tag_id)
        return self._get("tag/delete", params={"tagid": tag_id})

    def get_users(self, tag_id: int) -> dict:
        """获取标签成员

        参考：https://work.weixin.qq.com/api/doc/90000/90135/90213

        **权限说明**：
        无限制，但返回列表仅包含应用可见范围的成员；第三方可获取自己创建的标签及应用可见
        范围内的标签详情。

        返回结果示例： ::

            {
               "errcode": 0,
               "errmsg": "ok",
               "tagname": "乒乓球协会",
               "userlist": [
                     {
                         "userid": "zhangsan",
                         "name": "李四"
                     }
                 ],
               "partylist": [2]
            }

        结果参数说明：

        +-----------+-------------------------------------------------------------------------------+
        | 参数      | 说明                                                                          |
        +===========+===============================================================================+
        | errcode   | 返回码                                                                        |
        +-----------+-------------------------------------------------------------------------------+
        | errmsg    | 对返回码的文本描述内容                                                        |
        +-----------+-------------------------------------------------------------------------------+
        | tagname   | 标签名                                                                        |
        +-----------+-------------------------------------------------------------------------------+
        | userlist  | 标签中包含的成员列表                                                          |
        +-----------+-------------------------------------------------------------------------------+
        | userid    | 成员帐号                                                                      |
        +-----------+-------------------------------------------------------------------------------+
        | name      | 成员名称，此字段从2019年12月30日起，对新创建第三方应用不再返回，              |
        |           | 2020年6月30日起，对所有历史第三方应用不再返回，后续第三方仅通讯录应用可获取， |
        |           | 第三方页面需要通过通讯录展示组件来展示名字                                    |
        +-----------+-------------------------------------------------------------------------------+
        | partylist | 标签中包含的部门id列表                                                        |
        +-----------+-------------------------------------------------------------------------------+

        :param tag_id: 标签ID，非负整型
        :return: 成员用户信息
        """
        self._validate_tag_id(tag_id)
        return self._get("tag/get", params={"tagid": tag_id})

    def add_users(
        self, tag_id: int, user_ids: Optional[List[str]] = None, department_ids: Optional[List[int]] = None
    ) -> dict:
        """增加标签成员

        参考：https://work.weixin.qq.com/api/doc/90000/90135/90214

        **权限说明**：
        调用的应用必须是指定标签的创建者；成员属于应用的可见范围。

        **注意**：每个标签下部门、人员总数不能超过3万个。

        返回结果示例：

        a. 正确时返回 ::

            {
               "errcode": 0,
               "errmsg": "ok"
            }

        b. 若部分userid、partylist非法，则返回 ::

            {
               "errcode": 0,
               "errmsg": "ok",
               "invalidlist"："usr1|usr2|usr",
               "invalidparty"：[2,4]
            }

        c. 当包含userid、partylist全部非法时返回 ::

            {
               "errcode": 40070,
               "errmsg": "all list invalid "
            }

        结果参数说明：

        +--------------+------------------------+
        | 参数         | 说明                   |
        +==============+========================+
        | errcode      | 返回码                 |
        +--------------+------------------------+
        | errmsg       | 对返回码的文本描述内容 |
        +--------------+------------------------+
        | invalidlist  | 非法的成员帐号列表     |
        +--------------+------------------------+
        | invalidparty | 非法的部门id列表       |
        +--------------+------------------------+

        :param tag_id: 标签ID，非负整型
        :param user_ids: 企业成员ID列表，注意：user_ids和department_ids不能同时为空，
            单次请求个数不超过1000
        :param department_ids: 企业部门ID列表，注意：user_ids和department_ids不能
            同时为空，单次请求个数不超过100
        :return: 请求结果
        """
        self._validate_tag_id(tag_id)
        if not user_ids and not department_ids:
            raise ValueError("user_ids and department_ids cannot be empty at the same time")
        if user_ids is not None and len(user_ids) > 1000:
            raise ValueError("the length of the user_ids cannot be greater than 1000")
        if department_ids is not None and len(department_ids) > 100:
            raise ValueError("the length of the department_ids cannot be greater than 100")

        data: Dict[str, Any] = {"tagid": tag_id}
        if user_ids:
            data["userlist"] = user_ids
        if department_ids:
            data["partylist"] = department_ids

        return self._post("tag/addtagusers", data=data)

    def delete_users(
        self, tag_id: int, user_ids: Optional[List[str]] = None, department_ids: Optional[List[int]] = None
    ) -> dict:
        """删除标签成员

        参考：https://work.weixin.qq.com/api/doc/90000/90135/90215

        **权限说明**：
        调用的应用必须是指定标签的创建者；成员属于应用的可见范围。

        返回结果示例：

        a. 正确时返回 ::

            {
               "errcode": 0,
               "errmsg": "deleted"
            }
        b. 若部分userid、partylist非法，则返回 ::

            {
               "errcode": 0,
               "errmsg": "deleted",
               "invalidlist"："usr1|usr2|usr",
               "invalidparty": [2,4]
            }

        c. 当包含的userid、partylist全部非法时返回 ::

            {
               "errcode": 40031,
               "errmsg": "all list invalid"
            }

        结果参数说明：

        +--------------+------------------------+
        | 参数         | 说明                   |
        +==============+========================+
        | errcode      | 返回码                 |
        +--------------+------------------------+
        | errmsg       | 对返回码的文本描述内容 |
        +--------------+------------------------+
        | invalidlist  | 非法的成员帐号列表     |
        +--------------+------------------------+
        | invalidparty | 非法的部门id列表       |
        +--------------+------------------------+

        :param tag_id: 标签ID，非负整型
        :param user_ids: 企业成员ID列表，注意：user_ids和department_ids不能同时为空，
            单次请求长度不超过1000
        :param department_ids: 企业部门ID列表，注意：user_ids和department_ids不能
            同时为空，单次请求长度不超过100
        :return: 处理结果
        """
        self._validate_tag_id(tag_id)
        if not user_ids and not department_ids:
            raise ValueError("user_ids and department_ids cannot be empty at the same time")
        if user_ids is not None and len(user_ids) > 1000:
            raise ValueError("the length of the user_ids cannot be greater than 1000")
        if department_ids is not None and len(department_ids) > 100:
            raise ValueError("the length of the department_ids cannot be greater than 100")

        data: Dict[str, Any] = {"tagid": tag_id}
        if user_ids:
            data["userlist"] = user_ids
        if department_ids:
            data["partylist"] = department_ids

        return self._post("tag/deltagusers", data={"tagid": tag_id, "userlist": user_ids})

    def list(self) -> List[dict]:
        """获取标签列表

        参考：https://work.weixin.qq.com/api/doc/90000/90135/90216

        **权限说明**：
        自建应用或通讯同步助手可以获取所有标签列表；第三方应用仅可获取自己创建的标签。

        返回结果示例： ::

            {
               "errcode": 0,
               "errmsg": "ok",
               "taglist":[
                  {"tagid":1,"tagname":"a"},
                  {"tagid":2,"tagname":"b"}
               ]
            }

        结果参数说明：

        +---------+------------------------+
        | 参数    | 说明                   |
        +=========+========================+
        | errcode | 返回码                 |
        +---------+------------------------+
        | errmsg  | 对返回码的文本描述内容 |
        +---------+------------------------+
        | taglist | 标签列表               |
        +---------+------------------------+
        | tagid   | 标签id                 |
        +---------+------------------------+
        | tagname | 标签名                 |
        +---------+------------------------+

        :return: 标签信息列表，不包含errcode等信息
        """
        res = self._get("tag/list")
        return res["taglist"]
