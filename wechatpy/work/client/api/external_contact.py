# -*- coding: utf-8 -*-
from typing import Optional, List, Iterator

from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatExternalContact(BaseWeChatAPI):
    """
    外部联系人管理

    详细说明请查阅企业微信有关 `外部联系人管理`_ 的文档。

    .. _外部联系人管理: https://work.weixin.qq.com/api/doc/90000/90135/92109

    .. _客户联系secret: https://work.weixin.qq.com/api/doc/90000/90135/92570
            #13473/%E5%BC%80%E5%A7%8B%E5%BC%80%E5%8F%91

    .. _可调用应用: https://work.weixin.qq.com/api/doc/90000/90135/92570#134
        73/%E5%BC%80%E5%A7%8B%E5%BC%80%E5%8F%91

    .. _客户联系功能: https://work.weixin.qq.com/api/doc/90000/90135/92125
        #13473/%E5%BC%80%E5%A7%8B%E5%BC%80%E5%8F%91

    .. _企业客户权限: https://work.weixin.qq.com/api/doc/90000/90135/92572#19519

    .. _获取外部联系人详情: https://work.weixin.qq.com/api/doc/90000/90135/92572
        #13878
    """

    def get_follow_user_list(self) -> dict:
        """
        获取配置了客户联系功能的成员列表

        企业和第三方服务商可获取配置了客户联系功能的成员列表。

        详细请查阅企业微信官方文档 `获取配置了客户联系功能的成员列表`_ 章节。

        使用示例:

        .. code-block:: python

            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            # 获取成员用户userid列表数据
            follow_users = client.external_contact.get_follow_user_list()["follow_user"]

        :return: 配置了客户联系功能的成员用户userid信息

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需拥有“企业客户”权限。
            - 第三方/自建应用只能获取到可见范围内的配置了客户联系功能的成员。

        .. _获取配置了客户联系功能的成员列表:
            https://work.weixin.qq.com/api/doc/90000/90135/92570
        """
        return self._get("externalcontact/get_follow_user_list")

    def list(self, userid: str) -> dict:
        """
        获取客户列表

        企业可通过此接口获取指定成员添加的客户列表。客户是指配置了客户联系功能的成员所添加的
        外部联系人。没有配置客户联系功能的成员，所添加的外部联系人将不会作为客户返回。

        详细请查阅企业微信官方文档 `获取客户列表`_ 章节。

        使用示例:

        .. code-block:: python

            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            # 获取外部联系人的userid列表
            follow_users = client.external_contact.list("user_id")["external_userid"]

        :param userid: 企业成员的userid
        :return: 包含外部联系人的userid列表的字典类型数据

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需拥有“企业客户”权限。
            - 第三方/自建应用只能获取到可见范围内的配置了客户联系功能的成员。

        .. _获取客户列表: https://work.weixin.qq.com/api/doc/90000/90135/92113
        """
        return self._get("externalcontact/list", params={"userid": userid})

    def batch_get_by_user(self, userid: str, cursor: str = "", limit: int = 50) -> dict:
        """
        批量获取客户详情

        使用示例：

        .. code-block:: python

            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            # 批量获取该企业员工添加的客户(外部联系人)的详情
            external_contact_list = client.external_contact.batch_get_by_user("user_id", "cursor", 10)["external_contact_list"]

        :param userid: 企业成员的userid
        :param cursor: 用于分页查询的游标，字符串类型，由上一次调用返回，首次调用可不填
        :param limit: 返回的最大记录数，整型，最大值100，默认值50，超过最大值时取最大值
        :return: 包含该企业员工添加的部分客户详情列表的字典类型数据

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需具有“企业客户权限->客户基础信息”权限
            - 第三方/自建应用调用此接口时，userid需要在相关应用的可见范围内。

        .. _批量获取客户详情: https://work.weixin.qq.com/api/doc/90000/90135/92994
        """
        data = optionaldict(
            userid=userid,
            cursor=cursor,
            limit=limit,
        )
        return self._post("externalcontact/batch/get_by_user", data=data)

    def gen_all_by_user(self, userid: str, limit: int = 50) -> Iterator[dict]:
        """
        获取企业员工添加的所有客户详情列表的生成器

        .. code-block:: python

            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            #  获取企业员工添加的所有客户详情列表
            for i in client.external_contact.gen_all_by_user("user_id", 10):
                print(i)

        :param userid: 企业员工userid
        :param limit: 每次需要请求微信接口时返回的最大记录数，整型，最大值100，默认值50，超过最大值时取最大值
        :return: 企业员工添加的所有客户详情列表的生成器

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需具有“企业客户权限->客户基础信息”权限
            - 第三方/自建应用调用此接口时，userid需要在相关应用的可见范围内。
        """
        cursor = ""
        while True:
            response = self.batch_get_by_user(userid, cursor, limit)
            if response.get("errcode") == 0:
                yield from response.get("external_contact_list", [])
            if response.get("next_cursor"):
                cursor = response["next_cursor"]
            else:
                break

    def get(self, external_userid: str) -> dict:
        """
        获取客户详情

        企业可通过此接口，根据 `外部联系人的userid（如何获取?）`_，拉取客户详情。

        详细请查阅企业微信官方文档 `获取客户详情`_ 章节。

        使用示例:

        .. code-block:: python

            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            # 接口数据
            data = client.external_contact.get("external_userid")
            # 外部联系人的自定义展示信息
            external_profile = data["external_profile"]  # type: dict
            # 部联系人的企业成员userid
            follow_users = data["follow_user"]  # type: List[dict]

        :param external_userid: 外部联系人的userid，注意不是企业成员的帐号
        :return: 用户信息（字段内容请参考官方文档 `获取客户详情`_ 章节）

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方/自建应用调用时，返回的跟进人follow_user仅包含应用可见范围之内的成员。

        .. _外部联系人的userid（如何获取?）: https://work.weixin.qq.com/api/doc/9
            0000/90135/92114#15445

        .. _获取客户详情: https://work.weixin.qq.com/api/doc/90000/90135/92114
        """
        return self._get("externalcontact/get", params={"external_userid": external_userid})

    def add_contact_way(
        self,
        type: int,
        scene: int,
        style: Optional[int] = None,
        remark: Optional[str] = None,
        skip_verify: bool = True,
        state: Optional[str] = None,
        user: List[str] = None,
        party: List[int] = None,
        is_temp: bool = False,
        expires_in: Optional[int] = None,
        chat_expires_in: Optional[int] = None,
        unionid: Optional[str] = None,
        conclusions: Optional[dict] = None,
    ) -> dict:
        """
        配置客户联系「联系我」方式

        详细请查阅企业微信官方文档 `配置客户联系「联系我」方式`_ 章节。

        **注意:**

        - 每个联系方式最多配置100个使用成员（包含部门展开后的成员）
        - 当设置为临时会话模式时（即 ``is_temp`` 为 `True` ），联系人仅支持配置为单人，
          暂不支持多人
        - 使用 ``unionid`` 需要调用方（企业或服务商）的企业微信“客户联系”中已绑定微信开
          发者账户

        使用示例:

        .. code-block:: python

            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            # 调用接口
            result = client.external_contact.add_contact_way(
                type=1,
                scene=1,
                style=1,
                remark="渠道用户",
                skip_verify=True,
                state="teststate",
                user=["zhansan", "lisi"],
                party=[2,3],
                is_temp=True,
                expires_in=86400,
                chat_expires_in=86400,
                unionid="oxTWIuGaIt6gTKsQRLau2M0AAAA",
                conclusions={
                    "text": {"content": "文本消息内容"},
                    "image": {"media_id": "MEDIA_ID"},
                    "link": {
                        "title": "消息标题",
                        "picurl": "https://example.pic.com/path",
                        "desc": "消息描述",
                        "url": "https://example.link.com/path",
                    },
                    "miniprogram": {
                        "title": "消息标题",
                        "pic_media_id": "MEDIA_ID",
                        "appid": "wx8bd80126147dfAAA",
                        "page": "/path/index.html",
                    },
                },
            )
            # 新增联系方式的配置id
            config_id = result["config_id"]
            # 联系我二维码链接，仅在scene为2时返回
            qr_code = result.get("qr_code")

        :param type: 联系方式类型,1-单人, 2-多人
        :param scene: 场景，1-在小程序中联系，2-通过二维码联系
        :param style: 在小程序中联系时使用的控件样式，详见附表
        :param remark: 联系方式的备注信息，用于助记，不超过30个字符
        :param skip_verify: 外部客户添加时是否无需验证，默认为true
        :param state: 企业自定义的state参数，用于区分不同的添加渠道，在调用
            `获取外部联系人详情`_ 时会返回该参数值
        :param user: 使用该联系方式的用户userID列表，在type为1时为必填，且只能有一个
        :param party: 使用该联系方式的部门id列表，只在type为2时有效
        :param is_temp: 是否临时会话模式，``True`` 表示使用临时会话模式，默认为 ``False``
        :param expires_in: 临时会话二维码有效期，以秒为单位。该参数仅在 ``is_temp`` 为
            ``True`` 时有效，默认7天
        :param chat_expires_in: 临时会话有效期，以秒为单位。该参数仅在 ``is_temp`` 为
            ``True`` 时有效，默认为添加好友后24小时
        :param unionid: 可进行临时会话的客户unionid，该参数仅在 ``is_temp`` 为
            ``True``时有效，如不指定则不进行限制
        :param conclusions: 结束语，会话结束时自动发送给客户，可参考 `结束语定义`_，
            仅在 ``is_temp`` 为 ``True`` 时有效
        :return: 返回的 JSON 数据包

        .. note::
            **调用接口应满足如下的权限要求：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 使用人员需要配置了 `客户联系功能`_。
            - 第三方调用时，应用需具有 `企业客户权限`_。
            - 第三方/自建应用调用时，传入的userid和partyid需要在此应用的可见范围内。
            - 配置的使用成员必须在企业微信激活且已经过实名认证。
            - 临时会话的二维码具有有效期，添加企业成员后仅能在指定有效期内进行会话，
              仅支持医疗行业企业创建。
              临时会话模式可以配置会话结束时自动发送给用户的结束语。

        .. _配置客户联系「联系我」方式: https://work.weixin.qq.com/api/doc/90000/9
            0135/92572#%E9%85%8D%E7%BD%AE%E5%AE%A2%E6%88%B7%E8%81%94%E7%B3%BB
            %E3%80%8C%E8%81%94%E7%B3%BB%E6%88%91%E3%80%8D%E6%96%B9%E5%BC%8F

        .. _结束语定义: https://work.weixin.qq.com/api/doc/90000/90135/92572#156
            45/%E7%BB%93%E6%9D%9F%E8%AF%AD%E5%AE%9A%E4%B9%89
        """
        data = optionaldict(
            type=type,
            scene=scene,
            style=style,
            remark=remark,
            skip_verify=skip_verify,
            state=state,
            user=user,
            party=party,
            is_temp=is_temp,
            expires_in=expires_in,
            chat_expires_in=chat_expires_in,
            unionid=unionid,
            conclusions=conclusions,
        )
        return self._post("externalcontact/add_contact_way", data=data)

    def get_contact_way(self, config_id: str) -> dict:
        """
        获取企业已配置的「联系我」方式

        批量获取企业配置的「联系我」二维码和「联系我」小程序按钮。

        详细请查阅企业微信官方文档 `获取企业已配置的「联系我」方式`_ 章节。

        :param config_id: 联系方式的配置id, e.g.42b34949e138eb6e027c123cba77fad7
        :return: 返回的 JSON 数据包

        .. note::
            **调用接口应满足如下的权限要求：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 使用人员需要配置了 `客户联系功能`_。
            - 第三方调用时，应用需具有 `企业客户权限`_。
            - 第三方/自建应用调用时，传入的userid和partyid需要在此应用的可见范围内。
            - 配置的使用成员必须在企业微信激活且已经过实名认证。
            - 临时会话的二维码具有有效期，添加企业成员后仅能在指定有效期内进行会话，
              仅支持医疗行业企业创建。
              临时会话模式可以配置会话结束时自动发送给用户的结束语。

        .. _获取企业已配置的「联系我」方式: https://work.weixin.qq.com/api/doc/90000
           /90135/92572#%E8%8E%B7%E5%8F%96%E4%BC%81%E4%B8%9A%E5%B7%B2%E9%85%8D
           %E7%BD%AE%E7%9A%84%E3%80%8C%E8%81%94%E7%B3%BB%E6%88%91%E3%80%8D%E6%
           96%B9%E5%BC%8F
        """
        data = optionaldict(config_id=config_id)
        return self._post("externalcontact/get_contact_way", data=data)

    def update_contact_way(
        self,
        config_id,
        remark,
        skip_verify=True,
        style=None,
        state=None,
        user=None,
        party=None,
    ) -> dict:
        """
        更新企业已配置的「联系我」方式

        更新企业配置的「联系我」二维码和「联系我」小程序按钮中的信息，如使用人员和备注等。

        详细请查阅企业微信官方文档 `更新企业已配置的「联系我」方式`_ 章节。

        :param config_id: 企业联系方式的配置id
        :param remark: 联系方式的备注信息，不超过30个字符，将覆盖之前的备注
        :param skip_verify: 外部客户添加时是否无需验证
        :param style: 样式，只针对“在小程序中联系”的配置生效
        :param state: 企业自定义的state参数，用于区分不同的添加渠道，在调用“获取外部联系
           人详情”时会返回该参数值
        :param user: 使用该联系方式的用户列表，将覆盖原有用户列表
        :param party: 使用该联系方式的部门列表，将覆盖原有部门列表，只在配置的type为2时有效
        :return: 返回的 JSON 数据包

        .. note::
            **调用接口应满足如下的权限要求：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 使用人员需要配置了 `客户联系功能`_。
            - 第三方调用时，应用需具有 `企业客户权限`_。
            - 第三方/自建应用调用时，传入的userid和partyid需要在此应用的可见范围内。
            - 配置的使用成员必须在企业微信激活且已经过实名认证。
            - 临时会话的二维码具有有效期，添加企业成员后仅能在指定有效期内进行会话，
              仅支持医疗行业企业创建。
              临时会话模式可以配置会话结束时自动发送给用户的结束语。

        .. _更新企业已配置的「联系我」方式: https://work.weixin.qq.com/api/doc/90000
           /90135/92572#%E6%9B%B4%E6%96%B0%E4%BC%81%E4%B8%9A%E5%B7%B2%E9%85%8D
           %E7%BD%AE%E7%9A%84%E3%80%8C%E8%81%94%E7%B3%BB%E6%88%91%E3%80%8D%E6%
           96%B9%E5%BC%8F
        """
        data = optionaldict(
            config_id=config_id,
            remark=remark,
            skip_verify=skip_verify,
            style=style,
            state=state,
            user=user,
            party=party,
        )
        return self._post("externalcontact/update_contact_way", data=data)

    def del_contact_way(self, config_id: str) -> dict:
        """
        删除企业已配置的「联系我」方式

        删除一个已配置的「联系我」二维码或者「联系我」小程序按钮。

        详细请查阅企业微信官方文档 `删除企业已配置的「联系我」方式`_ 章节。

        :param config_id: 企业联系方式的配置id
        :return: 返回的 JSON 数据包

        .. note::
            **调用接口应满足如下的权限要求：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 使用人员需要配置了 `客户联系功能`_。
            - 第三方调用时，应用需具有 `企业客户权限`_。
            - 第三方/自建应用调用时，传入的userid和partyid需要在此应用的可见范围内。
            - 配置的使用成员必须在企业微信激活且已经过实名认证。
            - 临时会话的二维码具有有效期，添加企业成员后仅能在指定有效期内进行会话，
              仅支持医疗行业企业创建。
              临时会话模式可以配置会话结束时自动发送给用户的结束语。

        .. _删除企业已配置的「联系我」方式: https://work.weixin.qq.com/api/doc/90000
           /90135/92572#%E5%88%A0%E9%99%A4%E4%BC%81%E4%B8%9A%E5%B7%B2%E9%85%8D
           %E7%BD%AE%E7%9A%84%E3%80%8C%E8%81%94%E7%B3%BB%E6%88%91%E3%80%8D%E6%
           96%B9%E5%BC%8F

        """
        data = optionaldict(config_id=config_id)
        return self._post("externalcontact/del_contact_way", data=data)

    def add_msg_template(self, template: dict) -> dict:
        """
        添加企业群发消息模板

        企业可通过此接口添加企业群发消息的任务并通知客服人员发送给相关客户或客户群。
        （注：企业微信终端需升级到2.7.5版本及以上）

        **注意**：调用该接口并不会直接发送消息给客户/客户群，需要相关的客服人员操作以后才会
        实际发送（客服人员的企业微信需要升级到2.7.5及以上版本）

        同一个企业每个自然月内仅可针对一个客户/客户群发送4条消息，超过限制的用户将会被忽略。

        详细请查阅企业微信官方文档 `添加企业群发消息任务`_ 章节。

        使用示例:

        .. code-block:: python

            from wechatpy.exceptions import WeChatClientException
            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            template = {
                "chat_type":"single",
                "external_userid":[
                    "woAJ2GCAAAXtWyujaWJHDDGi0mACAAAA",
                    "wmqfasd1e1927831123109rBAAAA"
                ],
                "sender":"zhangsan",
                "text":{
                    "content":"文本消息内容"
                },
                "image":{
                    "media_id":"MEDIA_ID",
                    "pic_url":"http://p.qpic.cn/pic_wework/3474110808/7a6344sdadfwehe42060/0"
                },
                "link":{
                    "title":"消息标题",
                    "picurl":"https://example.pic.com/path",
                    "desc":"消息描述",
                    "url":"https://example.link.com/path"
                },
                "miniprogram":{
                    "title":"消息标题",
                    "pic_media_id":"MEDIA_ID",
                    "appid":"wx8bd80126147dfAAA",
                    "page":"/path/index.html"
                }
            }
            try:
                result = client.external_contact.add_msg_template(template=template)
                # 无效或无法发送的external_userid列表
                fail_list = result["fail_list"]
                # 企业群发消息的id，可用于获取群发消息发送结果
                msgid = result["msgid]
            except WeChatClientException as err:
                # 接口调用失败
                ...

        :param template: 参考官方文档和使用示例
        :return: 请求结果（字典类型）

        .. _添加企业群发消息任务: https://work.weixin.qq.com/api/doc/90000/90135/92135
        """
        return self._post("externalcontact/add_msg_template", data=template)

    def get_group_msg_result(self, msgid):
        """
        获取企业群发消息发送结果

        企业和第三方可通过该接口获取到添加企业群发消息模板生成消息的群发发送结果。
        https://work.weixin.qq.com/api/doc#90000/90135/91561

        :param msgid: 群发消息的id，通过添加企业群发消息模板接口返回
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(msgid=msgid)
        return self._post("externalcontact/get_group_msg_result", data=data)

    def get_user_behavior_data(
        self,
        userid: Optional[List[str]],
        start_time: int,
        end_time: int,
        partyid: Optional[List[str]] = None,
    ) -> dict:
        """
        获取「联系客户统计」数据

        企业可通过此接口获取成员联系客户的数据，包括发起申请数、新增客户数、聊天数、发送消息
        数和删除/拉黑成员的客户数等指标。

        详细请查阅企业微信官方文档 `获取「联系客户统计」数据`_ 章节。

        :param userid: userid列表
        :param partyid: 部门ID列表，最多100个
        :param start_time: 数据起始时间
        :param end_time: 数据结束时间
        :return: 返回的 JSON 数据包
        :raises AssertionError: 当userid和partyid同时为空时抛出该移除

        .. warning::

           1. ``userid`` 和 ``partyid`` 不可同时为空;
           2. 此接口提供的数据以天为维度，查询的时间范围为 ``[START_TIME,END_TIME]``，
              即前后均为闭区间，支持的最大查询跨度为30天；
           3. 用户最多可获取最近180天内的数据；
           4. 当传入的时间不为0点时间戳时，会向下取整，如传入
              1554296400(wED aPR 3 21:00:00 cst 2019) 会被自动转换为
              1554220800（wED aPR 3 00:00:00 cst 2019）;
           5. 如传入多个 ``USERID``，则表示获取这些成员总体的联系客户数据。

        .. note::

            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用使用，需具有“企业客户权限->客户联系->获取成员联系客户的数据统计”权限。
            - 第三方/自建应用调用时传入的userid和partyid要在应用的可见范围内;

        .. _获取「联系客户统计」数据: https://work.weixin.qq.com/api/doc/90000/90135/92132
        """
        assert userid or partyid, "userid和partyid不可同时为空"

        data = optionaldict(userid=userid, start_time=start_time, end_time=end_time, partyid=partyid)
        return self._post("externalcontact/get_user_behavior_data", data=data)

    def send_welcome_msg(self, template: dict) -> dict:
        """
        发送新客户欢迎语

        企业微信在向企业推送 `添加外部联系人事件`_ 时，会额外返回一个welcome_code，企业以
        此为凭据调用接口，即可通过成员向新添加的客户发送个性化的欢迎语。

        为了保证用户体验以及避免滥用，企业仅可在收到相关事件后20秒内调用，且只可调用一次。如
        果企业已经在管理端为相关成员配置了可用的欢迎语，则推送添加外部联系人事件时不会返回
        welcome_code。

        每次添加新客户时 **可能有多个企业自建应用/第三方应用收到带有welcome_code的回调事件**，
        但仅有最先调用的可以发送成功。后续调用将返回 **41051（externaluser has started
        chatting）** 错误，请用户根据实际使用需求，合理设置应用可见范围，避免冲突。

        详细请查阅企业微信官方文档 `发送新客户欢迎语`_ 章节。

        使用示例:

        .. code-block:: python

            from wechatpy.exceptions import WeChatClientException
            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            template = {
                "chat_type":"single",
                "external_userid":[
                    "woAJ2GCAAAXtWyujaWJHDDGi0mACAAAA",
                    "wmqfasd1e1927831123109rBAAAA"
                ],
                "sender":"zhangsan",
                "text":{
                    "content":"文本消息内容"
                },
                "image":{
                    "media_id":"MEDIA_ID",
                    "pic_url":"http://p.qpic.cn/pic_wework/3474110808/7a6344sdadfwehe42060/0"
                },
                "link":{
                    "title":"消息标题",
                    "picurl":"https://example.pic.com/path",
                    "desc":"消息描述",
                    "url":"https://example.link.com/path"
                },
                "miniprogram":{
                    "title":"消息标题",
                    "pic_media_id":"MEDIA_ID",
                    "appid":"wx8bd80126147dfAAA",
                    "page":"/path/index.html"
                }
            }
            try:
                client.external_contact.send_welcome_msg(template=template)
            except WeChatClientException as err:
                # 消息发送失败时的处理
                ...

        :param template: 参考官方文档和使用示例
        :return: 消息推送结果（字典类型）

        .. _添加外部联系人事件: https://work.weixin.qq.com/api/doc/90000/90135/921
            37#15260/%E6%B7%BB%E5%8A%A0%E5%A4%96%E9%83%A8%E8%81%94%E7%B3%BB%E4%
            BA%BA%E4%BA%8B%E4%BB%B6

        .. _发送新客户欢迎语: https://work.weixin.qq.com/api/doc/90000/90135/92137

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需要拥有「企业客户」权限，且企业成员处于相关应用的可见范围内。
        """
        return self._post("externalcontact/send_welcome_msg", data=template)

    def get_unassigned_list(self, page_id: int = 0, page_size: int = 1000, cursor: Optional[str] = None) -> dict:
        """
        获取离职成员列表

        企业和第三方可通过此接口，获取所有离职成员的客户列表，并可进一步调用
        `分配在职或离职成员的客户`_ 接口将这些客户重新分配给其他企业成员。

        详细请查阅企业微信官方文档 `获取离职成员列表`_ 章节。

        :param page_id: 分页查询，要查询页号，从0开始
        :param page_size: 每次返回的最大记录数，默认为1000，最大值为1000
        :param cursor: 分页查询游标，字符串类型，适用于数据量较大的情况，如果使用该参数
           则无需填写page_id，该参数由上一次调用返回
        :return: 响应结果

        .. note::
           当 ``page_id`` 为1，``page_size`` 为100时，表示取第101到第200条记录。
           由于每个成员的客户数不超过5万，故 ``page_id * page_size`` 必须小于5万。

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需拥有“企业客户权限->客户联系->分配在职或离职成员的客户”权限

        .. _获取离职成员列表: https://work.weixin.qq.com/api/doc/90000/90135/92124
        """
        data = optionaldict(page_id=page_id, page_size=page_size, cursor=cursor)
        return self._post("externalcontact/get_unassigned_list", data=data)

    def transfer(
        self,
        external_userid: str,
        handover_userid: str,
        takeover_userid: str,
        transfer_success_msg: Optional[str] = None,
    ) -> dict:
        """
        分配在职或离职成员的客户


        企业可通过此接口，转接在职成员的客户或分配离职成员的客户给其他成员。

        详细请查阅企业微信官方文档 `分配在职或离职成员的客户`_ 章节。

        **调用参数注意事项：**

        - 在某些特殊情景下，可能存在已离职的成员和当前在职的企业成员具有相同userid的情况，
          此时优先分配在职成员的客户.
        - ``external_userid`` 必须是 ``handover_userid`` 的客户
          （即 `配置了客户联系功能`_ 的成员所添加的联系人）。
        - 在职成员的每位客户最多被分配2次。客户被转接成功后，将有90个自然日的服务关系保护期，
          保护期内的客户无法再次被分配。

        使用示例:

        .. code-block:: python

            from wechatpy.exceptions import WeChatClientException
            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            try:
                client.external_contact.transfer(
                    external_userid="woAJ2GCAAAXtWyujaWJHDDGi0mACAAAA",
                    handover_userid="zhangsan",
                    takeover_userid="lisi",
                    transfer_success_msg="您好！",您好
                )
            except WeChatClientException as err:
                # 分配失败时的处理
                ...

        :param external_userid: 外部联系人的userid，注意不是企业成员的帐号
        :param handover_userid: 离职成员的userid
        :param takeover_userid: 接替成员的userid
        :param transfer_success_msg: 转移成功后发给客户的消息，最多200个字符，不填则
            使用默认文案，目前只对在职成员分配客户的情况生效
        :return: 分配结果（字典类型）

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需拥有 `企业客户权限`_。
            - 接替成员必须在此第三方应用或自建应用的可见范围内。
            - 接替成员需要配置了 `客户联系功能`_。
            - 接替成员需要在企业微信激活且已经过实名认证。

        .. _分配在职或离职成员的客户: https://work.weixin.qq.com/api/doc/90000/90135/92125

        .. _配置了客户联系功能: https://work.weixin.qq.com/api/doc/90000/90135/
            92125#13473/%E5%BC%80%E5%A7%8B%E5%BC%80%E5%8F%91


        """
        data = optionaldict(
            external_userid=external_userid,
            handover_userid=handover_userid,
            takeover_userid=takeover_userid,
            transfer_success_msg=transfer_success_msg,
        )
        return self._post("externalcontact/transfer", data=data)

    def get_corp_tag_list(self, tag_ids: Optional[List[str]] = None) -> dict:
        """
        获取企业标签库

        企业可通过此接口获取企业客户标签详情。

        **企业客户标签** 是针对企业的外部联系人进行标记和分类的标签，由企业统一配置后，企业
        成员可使用此标签对客户进行标记。

        详细请查阅企业微信官方文档 `获取企业标签库`_ 章节。

        使用示例:

        .. code-block:: python

            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            # 接口数据
            data = client.external_contact.get_corp_tag_list(["tag_id1", "tag_id2"])
            # 标签组列表
            tag_groups = data["tag_group"]  # type: List[dict]

        :param tag_ids: 需要查询的标签id，如果为 ``None`` 则获取该企业的所有客户标签，
            目前暂不支持标签组id。
        :return: 包含标签信息的字典类型数据（详细字段请参考 `获取企业标签库`_）

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 对于添加/删除/编辑企业客户标签接口，目前仅支持使用 `客户联系secret`_ 所获
              取的accesstoken来调用。
            - 第三方仅可读取，且应用需具有 `企业客户权限`_。

        .. _获取企业标签库: https://work.weixin.qq.com/api/doc/90000/90135/92117
            #%E8%8E%B7%E5%8F%96%E4%BC%81%E4%B8%9A%E6%A0%87%E7%AD%BE%E5%BA%93
        """
        data = optionaldict(tag_id=tag_ids)
        return self._post("externalcontact/get_corp_tag_list", data=data)

    def add_corp_tag(
        self,
        group_id: Optional[str],
        group_name: Optional[str],
        order: Optional[int],
        tags: dict,
    ) -> dict:
        """
        添加企业客户标签

        **企业客户标签** 是针对企业的外部联系人进行标记和分类的标签，由企业统一配置后，企业
        成员可使用此标签对客户进行标记。

        企业可通过此接口向客户标签库中添加新的标签组和标签，**每个企业最多可配置3000个企业标签**。

        详细请查阅企业微信官方文档 `添加企业客户标签`_ 章节。

        **参数注意事项:**

        - 如果要向指定的标签组下添加标签，需要提供 ``group_id`` 参数；如果要创建一个全新的
          标签组以及标签，则需要通过 ``group_name`` 参数指定新标签组名称，如果填写的
          ``group_name`` 已经存在，则会在此标签组下新建标签。
        - 如果提供了 ``group_id`` 参数，则 ``group_name`` 和标签组的 ``order`` 参数
          会被忽略。
        - 不支持创建空标签组。
        - 标签组内的标签不可同名，如果传入多个同名标签，则只会创建一个。

        使用示例:

        .. code-block:: python

            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            # 创建标签
            result = client.external_contact.add_corp_tag(
                group_id="GROUP_ID",
                group_name="GROUP_NAME",
                order=1,
                tags=[
                    {"name": "TAG_NAME_1", "order": 1},
                    {"name": "TAG_NAME_2", "order": 2},
                ],
            )
            # 创建成功后的标签组信息
            tag_group = result["tag_group"]  # type: dict

        :param group_id: 标签组id
        :param group_name: 标签组名称，最长为30个字符
        :param order: 标签组次序值。order值大的排序靠前。有效的值范围是[0, 2^32)
        :param tags: 需要添加的标签列表，标签信息是包含 ``name`` （必须）和 ``order``
            （可选）两个字段的字典类型数据，比如: ``[{"name": 'tag_name", "order": 1}]``
            ，或者 ``[{"name": "tag_name"}]``。
        :return: 标签创建结果（字典类型，字段请参考 `添加企业客户标签`_）

        .. _添加企业客户标签: https://work.weixin.qq.com/api/doc/90000/90135/921
            17#%E6%B7%BB%E5%8A%A0%E4%BC%81%E4%B8%9A%E5%AE%A2%E6%88%B7%E6%A0%8
            7%E7%AD%BE

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 对于添加/删除/编辑企业客户标签接口，目前仅支持使用 `客户联系secret`_ 所获
              取的accesstoken来调用。
            - 第三方仅可读取，且应用需具有 `企业客户权限`_。

        .. warning:: 暂不支持第三方调用。
        """
        data = optionaldict(group_id=group_id, group_name=group_name, order=order, tag=tags)

        return self._post("externalcontact/add_corp_tag", data=data)

    def edit_corp_tag(self, id: str, name: Optional[str] = None, order: Optional[int] = None) -> dict:
        """
        编辑企业客户标签

        企业可通过此接口编辑客户标签/标签组的名称或次序值。

        **注意**: 修改后的标签组不能和已有的标签组重名，标签也不能和同一标签组下的其他标签重名。

        详细请查阅企业微信官方文档 `编辑企业客户标签`_ 章节。

        使用示例:

        .. code-block:: python

            from wechatpy.exceptions import WeChatClientException
            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            # 修改标签
            try:
                client.external_contact.edit_corp_tag(id="TAG_ID", name="NEW_TAG_NAME")
            except WeChatClientException as err:
                # 标签修改失败时的处理
                ...

        :param id: 标签或标签组的id列表
        :param name: 新的标签或标签组名称，最长为30个字符
        :param order: 标签/标签组的次序值。order值大的排序靠前。有效的值范围是[0, 2^32)
        :return: 创建结果（字典类型）

        .. _编辑企业客户标签: https://work.weixin.qq.com/api/doc/90000/90135/9211
            7#%E7%BC%96%E8%BE%91%E4%BC%81%E4%B8%9A%E5%AE%A2%E6%88%B7%E6%A0%87%
            E7%AD%BE

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 对于添加/删除/编辑企业客户标签接口，目前仅支持使用 `客户联系secret`_ 所获
              取的accesstoken来调用。
            - 第三方仅可读取，且应用需具有 `企业客户权限`_。

        .. warning:: 暂不支持第三方调用。
        """
        data = optionaldict(id=id, name=name, order=order)
        return self._post("externalcontact/edit_corp_tag", data=data)

    def del_corp_tag(self, tag_id: Optional[str] = None, group_id: Optional[str] = None) -> dict:
        """
        删除企业客户标签

        企业可通过此接口删除客户标签库中的标签，或删除整个标签组。

        详细请查阅企业微信官方文档 `删除企业客户标签`_ 章节。

        **参数注意事项**:

        - ``tag_id`` 和 ``group_id`` 不可同时为空。
        - 如果一个标签组下所有的标签均被删除，则标签组会被自动删除。

        使用示例:

        .. code-block:: python

            from wechatpy.exceptions import WeChatClientException
            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            try:
                client.external_contact.del_corp_tag(tag_id="TAG_ID")
            except WeChatClientException as err:
                # 标签删除失败时的处理
                ...

        :param tag_id: 标签的id列表
        :param group_id: 标签组的id列表
        :return: 删除结果（字典类型）

        .. _删除企业客户标签: https://work.weixin.qq.com/api/doc/90000/90135/9211
            7#%E5%88%A0%E9%99%A4%E4%BC%81%E4%B8%9A%E5%AE%A2%E6%88%B7%E6%A0%87%
            E7%AD%BE

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 对于添加/删除/编辑企业客户标签接口，目前仅支持使用 `客户联系secret`_ 所获
              取的accesstoken来调用。
            - 第三方仅可读取，且应用需具有 `企业客户权限`_。

        .. warning:: 暂不支持第三方调用。
        """
        data = optionaldict(tag_id=tag_id, group_id=group_id)
        return self._post("externalcontact/del_corp_tag", data=data)

    def mark_tag(
        self,
        userid: str,
        external_userid: str,
        add_tag: Optional[List[str]] = None,
        remove_tag: Optional[List[str]] = None,
    ) -> dict:
        """
        编辑客户企业标签

        企业可通过此接口为指定成员的客户添加上由 `企业统一配置的标签`_。

        详细请查阅企业微信官方文档 `编辑客户企业标签`_ 章节。

        **参数注意事项**:

        - 请确保 ``external_userid`` 是 ``userid`` 的外部联系人。
        - ``add_tag`` 和 ``remove_tag`` 不可同时为空。
        - 同一个标签组下现已支持多个标签

        使用示例:

        .. code-block:: python

            from wechatpy.exceptions import WeChatClientException
            from wechatpy.work import WeChatClient

            # 需要注意使用正确的secret，否则会导致在之后的接口调用中失败
            client = WeChatClient("corp_id", "secret_key")
            try:
                client.external_contact.mark_tag(
                    userid="USER_ID",
                    external_userid="EXT_ID",
                    add_tag=["TAG_ID_1", "TAG_ID_2"],
                )
            except WeChatClientException as err:
                # 编辑失败时的处理
                ...

        :param userid: 添加外部联系人的userid
        :param external_userid: 外部联系人userid
        :param add_tag: 要标记的标签列表
        :param remove_tag: 要移除的标签列表
        :return: 处理结果（字典类型）

        .. _企业统一配置的标签: https://work.weixin.qq.com/api/doc/90000/90135/92
            118#17298

        .. _编辑客户企业标签: https://work.weixin.qq.com/api/doc/90000/90135/92118

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方调用时，应用需具有外部联系人管理权限。
        """
        add_tag = add_tag or []
        remove_tag = remove_tag or []
        data = optionaldict(userid=userid, external_userid=external_userid, add_tag=add_tag, remove_tag=remove_tag)
        return self._post("externalcontact/mark_tag", data=data)

    def get_group_chat_list(
        self,
        limit: int,
        status_filter: int = 0,
        owner_filter: Optional[dict] = None,
        cursor: Optional[str] = None,
    ) -> dict:
        """
        获取客户群列表

        该接口用于获取配置过客户群管理的客户群列表。

        详细请查阅企业微信官方文档 `获取客户群列表`_ 章节。

        :param limit: 分页，预期请求的数据量，取值范围 1 ~ 1000
        :param status_filter: 客户群跟进状态过滤（默认为0）。
            0: 所有列表(即不过滤)
            1: 离职待继承
            2: 离职继承中
            3: 离职继承完成
        :param owner_filter: 群主过滤。
            如果不填，表示获取应用可见范围内全部群主的数据
            （但是不建议这么用，如果可见范围人数超过1000人，为了防止数据包过大，会报错 81017）
        :param cursor: 用于分页查询的游标，字符串类型，由上一次调用返回，首次调用不填
        :return: 响应数据

        .. warning::

           如果不指定 ``owner_filter``，会拉取应用可见范围内的所有群主的数据，
           但是不建议这样使用。如果可见范围内人数超过1000人，为了防止数据包过大，
           会报错 81017。此时，调用方需通过指定 ``owner_filter`` 来缩小拉取范围。

           旧版接口以 ``offset+limit`` 分页，要求 ``offset+limit`` 不能超过50000，
           该方案将废弃，请改用 ``cursor+limit`` 分页。

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需具有“企业客户权限->客户基础信息”权限
            - 对于第三方/自建应用，群主必须在应用的可见范围。

        .. _获取客户群列表: https://work.weixin.qq.com/api/doc/90000/90135/92120
        """
        data = optionaldict(status_filter=status_filter, owner_filter=owner_filter, cursor=cursor, limit=limit)
        return self._post("externalcontact/groupchat/list", data=data)

    def get_group_chat_info(self, chat_id: str) -> dict:
        """
        获取客户群详情

        通过客户群ID，获取详情。包括群名、群成员列表、群成员入群时间、入群方式。
        （客户群是由具有客户群使用权限的成员创建的外部群）

        需注意的是，如果发生群信息变动，会立即收到群变更事件，但是部分信息是异步处理，
        可能需要等一段时间调此接口才能得到最新结果

        详细请查阅企业微信官方文档 `获取客户群详情`_ 章节。

        :param chat_id: 客户群ID
        :return: 响应数据

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需具有“企业客户权限->客户基础信息”权限
            - 对于第三方/自建应用，群主必须在应用的可见范围。

        .. _获取客户群详情: https://work.weixin.qq.com/api/doc/90000/90135/92122
        """
        data = optionaldict(chat_id=chat_id)
        return self._post("externalcontact/groupchat/get", data=data)

    def add_group_welcome_template(self, template: dict, agentid: Optional[int] = None) -> dict:
        """
        添加群欢迎语素材

        企业可通过此API向企业的入群欢迎语素材库中添加素材。每个企业的入群欢迎语素材库中，
        最多容纳100个素材。

        详细请查阅企业微信官方文档 `添加群欢迎语素材`_ 章节。

        :param template: 群欢迎语素材内容，详细字段请参考微信文档
        :param agentid: 授权方安装的应用agentid。仅旧的第三方多应用套件需要填此参数
        :return: 响应数据

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需具有“企业客户权限->客户联系->配置入群欢迎语素材”权限

        .. _添加群欢迎语素材: https://work.weixin.qq.com/api/doc/90000/90135/
            92366#%E6%B7%BB%E5%8A%A0%E5%85%A5%E7%BE%A4%E6%AC%A2%E8%BF%8E%E
            8%AF%AD%E7%B4%A0%E6%9D%90

        """
        data = optionaldict()
        data.update(template)
        data["agentid"] = agentid
        return self._post("externalcontact/group_welcome_template/add", data=data)

    def update_group_welcome_template(self, template: dict, template_id: str, agentid: Optional[int] = None) -> dict:
        """
        编辑群欢迎语素材

        企业可通过此API编辑入群欢迎语素材库中的素材，且仅能够编辑调用方自己创建的入群欢迎语素材。


        详细请查阅企业微信官方文档 `编辑群欢迎语素材`_ 章节。

        :param template: 群欢迎语素材内容，详细字段请参考微信文档
        :param template_id: 欢迎语素材id
        :param agentid: 授权方安装的应用agentid。仅旧的第三方多应用套件需要填此参数
        :return: 响应数据

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需具有“企业客户权限->客户联系->配置入群欢迎语素材”权限
            - 仅可编辑本应用创建的入群欢迎语素材

        .. _添编辑群欢迎语素材: https://work.weixin.qq.com/api/doc/90000/90135/
            92366#%E7%BC%96%E8%BE%91%E5%85%A5%E7%BE%A4%E6%AC%A2%E8%BF%8E%E8%
            AF%AD%E7%B4%A0%E6%9D%90
        """
        data = optionaldict()
        data.update(template)
        data["template_id"] = template_id
        data["agentid"] = agentid
        return self._post("externalcontact/group_welcome_template/edit", data=data)

    def get_group_welcome_template(self, template_id: str) -> dict:
        """
        获取入群欢迎语素材

        企业可通过此API获取入群欢迎语素材。

        详细请查阅企业微信官方文档 `获取入群欢迎语素`_ 章节。

        :param template_id: 群欢迎语的素材id
        :return: 响应数据

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需具有“企业客户权限->客户联系->配置入群欢迎语素材”权限

        .. _获取入群欢迎语素材: https://work.weixin.qq.com/api/doc/90000/90135/
            92366#%E8%8E%B7%E5%8F%96%E5%85%A5%E7%BE%A4%E6%AC%A2%E8%BF%8E%E8%
            AF%AD%E7%B4%A0%E6%9D%90
        """
        data = optionaldict(template_id=template_id)
        return self._post("externalcontact/group_welcome_template/get", data=data)

    def del_group_welcome_template(self, template_id: str, agentid: Optional[int] = None) -> dict:
        """
        删除入群欢迎语素材

        企业可通过此API删除入群欢迎语素材，且仅能删除调用方自己创建的入群欢迎语素材。

        详细请查阅企业微信官方文档 `删除入群欢迎语素材`_ 章节。

        :param template_id: 群欢迎语的素材id
        :param agentid: 授权方安装的应用agentid。仅旧的第三方多应用套件需要填此参数
        :return: 响应数据

        .. note::
            **权限说明：**

            - 需要使用 `客户联系secret`_ 或配置到 `可调用应用`_ 列表中的自建应用secret
              来初始化 :py:class:`wechatpy.work.client.WeChatClient` 类。
            - 第三方应用需具有“企业客户权限->客户联系->配置入群欢迎语素材”权限
            - 仅可删除本应用创建的入群欢迎语素材

        .. _删除入群欢迎语素材: https://work.weixin.qq.com/api/doc/90000/90135/
            92366#%E5%88%A0%E9%99%A4%E5%85%A5%E7%BE%A4%E6%AC%A2%E8%BF%8E%E8
            %AF%AD%E7%B4%A0%E6%9D%90
        """
        data = optionaldict(template_id=template_id, agentid=agentid)
        return self._post("externalcontact/group_welcome_template/del", data=data)
