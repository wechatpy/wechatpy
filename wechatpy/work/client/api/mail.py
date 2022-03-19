# -*- coding: utf-8 -*-


from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMail(BaseWeChatAPI):
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

        :param group_id: 必填， 邮件群组 ID，邮箱格式。
        :param group_name: 必填，邮件群组名称，不能与其他群组重名，长度限定64字节。
        :param email_list: 选填， 群组内成员邮箱地址，读取成员的 biz_mail 字段，email_list，group_list，department_list，tag_list 至少填写一个，不可同时为空。
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
        self._post("exmail/group/create", data=data)

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
        self._post("exmail/group/update", data=data)

    def delete_group(self, group_id):
        """
        删除邮件群组

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95510

        :param group_id: 必填， 邮件群组 ID，邮箱格式。
        """
        self._post("exmail/group/delete", data={"groupid": group_id})

    def get_group(self, group_id):
        """
        获取邮件群组详情

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95510

        :param group_id: 必填， 邮件群组 ID，邮箱格式。
        """
        self._get("exmail/group/get", params={"groupid": group_id})

    def search_group(self, fuzzy, group_id=None):
        """
        模糊搜索邮件群组，通过群组ID模糊搜索邮件群组。

        详情请参考
        https://developer.work.weixin.qq.com/document/path/95510

        :param fuzzy: 必填， 1 开启模糊搜索，0 获取全部邮件群组
        :param group_id: 选填， 邮件群组ID，邮箱格式。
        """
        params = {"fuzzy": fuzzy}
        if group_id is not None:
            params["groupid"] = group_id
        self._get("exmail/group/search", params=params)
