# -*- coding: utf-8 -*-


import json
import datetime

from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMarketing(BaseWeChatAPI):
    API_BASE_URL = "https://api.weixin.qq.com/marketing/"

    def add_user_action_sets(self, _type, name, description, version="v1.0"):
        """
        创建数据源
        https://wximg.qq.com/wxp/pdftool/get.html?id=rkalQXDBM&pa=39

        :param _type: 用户行为源类型
        :param name: 用户行为源名称 必填
        :param description: 用户行为源描述，字段长度最小 1 字节，长度最大 128 字节
        :param version: 版本号 v1.0
        :return: 数据源唯一ID
        """
        return self._post(
            "user_action_sets/add",
            params={"version": version},
            json=optionaldict(type=_type, name=name, description=description, version=version),
            result_processor=lambda x: x["data"]["user_action_set_id"],
        )

    def get_user_action_sets(self, user_action_set_id, version="v1.0"):
        """
        获取数据源信息

        :param user_action_set_id: 数据源唯一ID
        :param version: 版本号 v1.0
        """
        return self._get(
            "user_action_sets/get",
            params={"version": version, "user_action_set_id": user_action_set_id},
            result_processor=lambda x: x["data"]["list"],
        )

    def add_user_actions(self, actions=(), version="v1.0"):
        """
        回传数据

        https://wximg.qq.com/wxp/pdftool/get.html?id=rkalQXDBM&pa=39

        :param actions: 用户行为源类型
        :param version: 版本号 v1.0
        """
        return self._post("user_actions/add", params={"version": version}, json={"actions": actions})

    def get_ad_leads(
        self,
        start_date=None,
        end_date=None,
        filtering=(),
        page=1,
        page_size=100,
        version="v1.0",
    ):
        """
         获取朋友圈销售线索数据接口

        :param start_date: 开始日期 默认今天
        :param end_date: 结束日期 默认今天
        :param filtering: 过滤条件 [{field: 过滤字段, operator: 操作符, values: 字段取值}]
        :param page: 页码，获取指定页数据
        :param page_size: 一页获取的数据条数(1-100)
        :param version: 版本号 v1.0
        """
        today = datetime.date.today()
        if start_date is None:
            start_date = today
        if end_date is None:
            end_date = today
        if isinstance(start_date, datetime.date):
            start_date = start_date.strftime("%Y-%m-%d")
        if isinstance(end_date, datetime.date):
            end_date = end_date.strftime("%Y-%m-%d")

        return self._get(
            "wechat_ad_leads/get",
            params=optionaldict(
                date_range=json.dumps({"start_date": start_date, "end_date": end_date}),
                filtering=json.dumps(filtering) if filtering else None,
                page=page,
                page_size=page_size,
                version=version,
            ),
            result_processor=lambda x: x["data"],
        )
