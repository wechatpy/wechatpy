# -*- coding: utf-8 -*-
from operator import itemgetter

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatEMail(BaseWeChatAPI):
    """
    企业微信邮箱接口

    https://developer.work.weixin.qq.com/document/path/95486
    """

    def create_group(
        self,
        group_id,
        group_name,
        email_list=None,
        tag_list=None,
        department_list=None,
        group_list=None,
        allow_type=None,
        allow_emaillist=None,
        allow_departmentlist=None,
        allow_taglist=None,
    ):
        """
        该接口用于创建新邮件群组，可以指定群组成员，定义群组使用权限范围

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95510

        :param group_id: 必填，邮件群组 ID，邮箱格式。
        :param group_name: 必填，邮件群组名称，不能与其他群组重名，长度限定64字节。
        :param email_list: 选填，群组内成员邮箱地址，读取成员的 biz_mail 字段，email_list，group_list，department_list，tag_list 至少填写一个，不可同时为空。
        :param tag_list: 选填，群组内包含的标签ID。
        :param department_list: 选填，群组内包含的部门 ID。
        :param group_list: 选填，群组内包含的群组邮箱。
        :param allow_type: 选填，群组使用权限。
            - 0: 企业成员
            - 1：任何人
            - 2：组内成员
            - 3：自定义成员
            当值为 0、1、2时，不得传入 allow_emaillist，allow_departmentlist，allow_taglist。
            当值为 3 时，必须传入 allow_emaillist，allow_departmentlist，allow_taglist至少一项。
        :param allow_emaillist: 选填，允许使用群组群发的成员邮箱地址，读取成员的biz_mail字段。
        :param allow_departmentlist: 选填，允许使用群组群发的部门 ID。
        :param allow_taglist: 选填，允许使用群组群发的标签 ID。
        """
        if not any((email_list, group_list, department_list, tag_list)):
            raise ValueError("email_list, group_list, department_list and tag_list must be a choice.")

        data = {
            "groupid": group_id,
            "groupname": group_name,
            "email_list": {
                "list": email_list or [],
            },
            "tag_list": {
                "list": tag_list or [],
            },
            "department_list": {
                "list": department_list or [],
            },
            "group_list": {
                "list": group_list or [],
            },
        }

        if allow_type is not None:
            if allow_type in {0, 1, 2}:
                data["allow_type"] = allow_type
            elif allow_type == 3:
                if not any((allow_emaillist, allow_departmentlist, allow_taglist)):
                    raise ValueError("allow_emaillist, allow_departmentlist and allow_taglist must be a choice.")
                data.update(
                    {
                        "allow_emaillist": {
                            "list": allow_emaillist or [],
                        },
                        "allow_departmentlist": {
                            "list": allow_departmentlist or [],
                        },
                        "allow_taglist": {"list": allow_taglist or []},
                    }
                )
            else:
                raise ValueError("Unsupported allow_type. Valid allow_types are 0, 1, 2 or 3")
        return self._post("exmail/group/create", data=data)

    def update_group(
        self,
        group_id,
        group_name=None,
        email_list=None,
        tag_list=None,
        department_list=None,
        group_list=None,
        allow_type=None,
        allow_emaillist=None,
        allow_departmentlist=None,
        allow_taglist=None,
    ):
        """
        更新邮件群组
        可以修改群组名称、群组成员、群组使用权限等。需要注意的是 Json 数组类型传空值将会清空其内容，不传则保持不变。

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95510

        参数含义见 create
        """
        data = {"groupid": group_id}
        if group_name is not None:
            data["groupname"] = group_name
        if email_list is not None:
            data["email_list"] = {"list": email_list}
        if tag_list is not None:
            data["tag_list"] = {"list": tag_list}
        if department_list is not None:
            data["department_list"] = {"list": department_list}
        if group_list is not None:
            data["group_list"] = {"list": group_list}
        if allow_type is not None:
            if allow_type not in {0, 1, 2, 3}:
                raise ValueError("Unsupported allow_type. Valid allow_types are 0, 1, 2 or 3")
            data["allow_type"] = allow_type
        if allow_emaillist is not None:
            data["allow_emaillist"] = {"list": allow_emaillist}
        if allow_departmentlist is not None:
            data["allow_departmentlist"] = {"list": allow_departmentlist}
        if allow_taglist is not None:
            data["allow_taglist"] = {"list": allow_taglist}
        return self._post("exmail/group/update", data=data)

    def delete_group(self, group_id):
        """
        删除邮件群组

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95510

        :param group_id: 必填，邮件群组 ID，邮箱格式。
        """
        return self._post("exmail/group/delete", data={"groupid": group_id})

    def get_group(self, group_id):
        """
        获取邮件群组详情

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95510

        :param group_id: 必填，邮件群组 ID，邮箱格式。
        """
        return self._get("exmail/group/get", params={"groupid": group_id})

    def search_group(self, fuzzy, group_id=None):
        """
        模糊搜索邮件群组，通过群组ID模糊搜索邮件群组。

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95510

        :param fuzzy: 必填，1 开启模糊搜索，0 获取全部邮件群组
        :param group_id: 选填，邮件群组ID，邮箱格式。
        """
        params = {"fuzzy": fuzzy}
        if group_id is not None:
            params["groupid"] = group_id
        return self._get("exmail/group/search", params=params, result_processor=itemgetter("groups"))

    def create_public_email(self, email, name, userid_list=None, department_list=None, tag_list=None):
        """
        创建业务邮箱

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95511

        :param email: 必填，	业务邮箱地址。
        :param name：必填，业务邮箱名称，不多于 64 个字符或 32 个汉字，不得与其他业务邮箱重名。
        :param userid_list：选填，有权限使用业务邮箱的成员 UserID 列表。userid_list、department_list、taglist 不能同时为空。
        :param department_list：有权限使用业务邮箱的部门 ID 列表。
        :param tag_list：有权限使用业务邮箱的标签ID列表。
        """
        data = {"email": email, "name": name}
        if userid_list:
            data["userid_list"] = {"list": userid_list}
        if department_list:
            data["department_list"] = {"list": department_list}
        if tag_list:
            data["tag_list"] = {"list": tag_list}
        return self._post("exmail/publicmail/create", data=data, result_processor=itemgetter("id"))

    def update_public_email(self, email_id, name=None, userid_list=None, department_list=None, tag_list=None):
        """
        更新业务邮箱
        该接口用于更新业务邮箱，支持更新名称、使用权限。需要注意的是Json数组类型传空值将会清空其内容，不传则保持不变，传空为清空。

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95511

        :param email_id: 必填，业务邮箱 ID。
        :param name：必填，业务邮箱名称，不多于 64 个字符或 32 个汉字，不得与其他业务邮箱重名。
        :param userid_list：选填，有权限使用业务邮箱的成员 UserID 列表。userid_list、department_list、taglist 不能同时为空。
        :param department_list：有权限使用业务邮箱的部门 ID 列表。
        :param tag_list：有权限使用业务邮箱的标签ID列表
        """
        data = {"id": email_id}
        if name is not None:
            data["name"] = name
        if userid_list is not None:
            data["userid_list"] = {"list": userid_list}
        if department_list is not None:
            data["department_list"] = {"list": department_list}
        if tag_list is not None:
            data["tag_list"] = {"list": tag_list}
        return self._post(
            "exmail/publicmail/update",
            data=data,
        )

    def delete_public_email(self, email_id):
        """
        删除业务邮箱

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95511

        :param email_id: 必填，业务邮箱 ID。
        """
        return self._post(
            "exmail/publicmail/delete",
            data={"id": email_id},
        )

    def get_public_email(self, email_id):
        """
        获取业务邮箱详情

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95511

        :param email_id: 必填，业务邮箱 ID。
        """
        return self.batch_get_public_email([email_id])[0]

    def batch_get_public_email(self, email_ids):
        """
        获取业务邮箱详情

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95511

        :param email_ids: 必填，业务邮箱 ID 列表。
        """
        return self._post("exmail/publicmail/get", data={"id_list": email_ids}, result_processor=itemgetter("list"))

    def search_public_email(self, fuzzy, email=None):
        """
        模糊搜索业务邮箱
        用于模糊搜索业务邮箱，可匹配邮箱名也可匹配邮箱地址。

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95511

        :param fuzzy: 必填，1 开启模糊搜索，0 获取全部业务邮箱
        :param email: 选填，邮件群组 ID，邮箱格式。
        """
        params = {"fuzzy": fuzzy}
        if email is not None:
            params["email"] = email
        return self._get("exmail/publicmail/search", params=params, result_processor=itemgetter("list"))

    def active_email(self, user_id=None, public_email_id=None):
        """
        启用邮箱

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95512

        :param user_id: 成员 UserID，userid 与 public_email_id 至少应该传一项，同时传则只操作 userid。不可禁用超管与企业创建人。
        :param public_email_id: 业务邮箱 ID，userid 与 public_email_id 至少应该传一项，同时传则只操作 userid。
        """
        data = {"type": 1}
        if user_id:
            data["userid"] = user_id
        elif public_email_id:
            data["publicemail_id"] = public_email_id
        else:
            raise ValueError("user_id and public_email_id must be a choice.")

        return self._post(
            "exmail/account/act_email",
            data=data,
        )

    def inactive_email(self, user_id=None, public_email_id=None):
        """
        禁用邮箱

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95512

        :param user_id: 成员 UserID，userid 与 public_email_id 至少应该传一项，同时传则只操作 userid。不可禁用超管与企业创建人。
        :param public_email_id: 业务邮箱 ID，userid 与 public_email_id 至少应该传一项，同时传则只操作 userid。
        """
        data = {"type": 2}
        if user_id:
            data["userid"] = user_id
        elif public_email_id:
            data["publicemail_id"] = public_email_id
        else:
            raise ValueError("user_id and public_email_id must be a choice.")

        return self._post(
            "exmail/account/act_email",
            data=data,
        )

    def get_user_option(self, user_id, types):
        """
        获取用户功能属性

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95513

        :param user_id: 用户 UserID。
        :param types: 想查询的功能设置属性类型列表
            - 1: 强制启用安全登录
            - 2: IMAP/SMTP服务
            - 3: POP/SMTP服务
            - 4: 是否启用安全登录
        """
        return self._post(
            "exmail/useroption/get",
            data={
                "userid": user_id,
                "type": types,
            },
            result_processor=lambda x: x["option"]["list"],
        )

    def update_user_option(self, user_id, option):
        """
        更改用户功能属性

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95513

        :param user_id: 用户 UserID。
        :param option: 功能属性设置。

        option 数据示例：
        >>>[
        >>>    {
        >>>      "type": 1,
        >>>      "value": "0"
        >>>    },
        >>>    {
        >>>      "type": 2,
        >>>      "value": "1"
        >>>    },
        >>>    {
        >>>      "type": 3,
        >>>      "value": "0"
        >>>    }
        >>>]
        type: 功能属性类型
            - 1: 强制启用安全登录
            - 2: IMAP/SMTP服务
            - 3: POP/SMTP服务
            - 4: 是否启用安全登录
        value: 值
            - 1 表示启用
            - 0 表示关闭
        """
        return self._post(
            "exmail/useroption/update",
            data={
                "userid": user_id,
                "option": {"list": option},
            },
        )

    def get_new_email_count(self, user_id):
        """
        获取用户新邮件数

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95514

        :param user_id: 用户 UserID。
        """
        return self._post(
            "exmail/mail/get_newcount",
            data={
                "userid": user_id,
            },
            result_processor=itemgetter("count"),
        )
