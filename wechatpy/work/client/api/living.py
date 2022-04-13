# -*- coding: utf-8 -*-
from typing import Dict

from optionaldict import optionaldict
from wechatpy.client.api.base import BaseWeChatAPI


class WeChatLiving(BaseWeChatAPI):
    """
    企业微信直播接口

    https://developer.work.weixin.qq.com/document/path/93633
    """

    def create(
        self,
        anchor_userid: str,
        theme: str,
        living_start: int,
        living_duration: int,
        type: int = 0,
        description: str = None,
        agentid: int = None,
        remind_time: int = 0,
        activity_cover_mediaid: str = None,
        activity_share_mediaid: str = None,
        activity_detail: Dict = None,
    ):
        """
        创建预约直播

        详情请参考
        https://developer.work.weixin.qq.com/document/path/93637

        :param anchor_userid: 直播发起者的 userid
        :param theme: 直播的标题，最多支持 60 个字节
        :param living_start: 直播开始时间的 unix 时间戳
        :param living_duration: 直播持续时长
        :param type: 直播的类型，默认 0。其中大班课和小班课仅 k12 学校和 IT 行业类型能够发起
            - 0：通用直播
            - 1：小班课
            - 2：大班课
            - 3：企业培训
            - 4：活动直播
        :param description: 直播的简介，最多支持 300 个字节，仅对“通用直播”、“小班课”、“大班课”和“企业培训”生效，“活动直播”简介通过 activity_detail.description 控制
        :param agentid: 授权方安装的应用 agentid。仅旧的第三方多应用套件需要填此参数
        :param remind_time: 指定直播开始前多久提醒用户，相对于 living_start 前的秒数，默认为 0
        :param activity_cover_mediaid: 活动直播特定参数，直播间封面图的 mediaId
        :param activity_share_mediaid: 活动直播特定参数，直播分享卡片图的 mediaId
        :param activity_detail: 活动直播特定参数，活动直播详情信息
        :param activity_detail.description: 活动直播特定参数，活动直播简介
        :param activity_detail.image_list: 活动直播特定参数，活动直播附图的 mediaId 列表，最多支持传 5 张，超过五张取前五张
        :return:
        """
        data = optionaldict(
            anchor_userid=anchor_userid,
            theme=theme,
            living_start=living_start,
            living_duration=living_duration,
            type=type,
            description=description,
            agentid=agentid,
            remind_time=remind_time,
            activity_cover_mediaid=activity_cover_mediaid,
            activity_share_mediaid=activity_share_mediaid,
            activity_detail=activity_detail,
        )

        return self._post("living/create", data=data)

    def modify(
        self,
        livingid: str,
        theme: str = None,
        living_start: int = None,
        living_duration: int = None,
        type: int = None,
        description: str = None,
        remind_time: int = 0,
    ):
        """
        修改预约直播

        详情请参考
        https://developer.work.weixin.qq.com/document/path/93640

        :param livingid: 直播 id，仅允许修改预约状态下的直播 id
        :param theme: 直播的标题，最多支持 60 个字节
        :param living_start: 直播开始时间的 unix 时间戳
        :param living_duration: 直播持续时长
        :param type: 直播的类型，其中大班课和小班课仅k12学校和IT行业类型能够发起
            - 0：通用直播
            - 1：小班课
            - 2：大班课
            - 3：企业培训
            - 4：活动直播
        :param description: 直播的简介，最多支持 300 个字节
        :param remind_time: 指定直播开始前多久提醒用户，相对于 living_start 前的秒数，默认为 0
        :return:
        """
        data = optionaldict(
            livingid=livingid,
            theme=theme,
            living_start=living_start,
            living_duration=living_duration,
            type=type,
            description=description,
            remind_time=remind_time,
        )

        return self._post("living/modify", data=data)

    def cancel(self, livingid: str):
        """
        取消预约直播

        详情请参考
        https://developer.work.weixin.qq.com/document/path/93638

        :param livingid: 直播 id，仅允许取消预约状态下的直播 id
        :return:
        """
        data = optionaldict(
            livingid=livingid,
        )

        return self._post("living/cancel", data=data)

    def delete_replay_data(self, livingid: str):
        """
        删除直播回放

        详情请参考
        https://developer.work.weixin.qq.com/document/path/93874

        :param livingid: 直播 id，仅允许取消预约状态下的直播 id
        :return:
        """
        data = optionaldict(
            livingid=livingid,
        )

        return self._post("living/delete_replay_data", data=data)

    def get_living_code(self, livingid: str, openid: str):
        """
        在微信中观看直播或直播回放，获取微信观看直播凭证

        详情请参考
        https://developer.work.weixin.qq.com/document/path/93641

        :param livingid: 直播 id
        :param openid: 微信用户的openid
        :return:
        """
        data = optionaldict(
            livingid=livingid,
            openid=openid,
        )

        return self._post("living/get_living_code", data=data)

    def get_user_all_livingid(self, userid: str, cursor: str = None, limit: int = 100):
        """
        获取成员直播 ID 列表

        详情请参考
        https://developer.work.weixin.qq.com/document/path/93634

        :param userid: 企业成员的 userid
        :param cursor: 上一次调用时返回的 next_cursor，第一次拉取可以不填
        :param limit: 上次拉取的数据量，默认值和最大值都为 100
        :return:
        """
        data = optionaldict(
            userid=userid,
            cursor=cursor,
            limit=limit,
        )

        return self._post("living/get_user_all_livingid", data=data)

    def get_living_info(self, livingid: str):
        """
        获取直播详情

        详情请参考
        https://developer.work.weixin.qq.com/document/path/93635

        :param livingid: 直播 id，仅允许取消预约状态下的直播 id
        :return:
        """
        params = {"livingid": livingid}

        return self._get("living/get_living_info", params=params)

    def get_watch_stat(self, livingid: str, next_key: str = "0"):
        """
        获取直播观看明细

        详情请参考
        https://developer.work.weixin.qq.com/document/path/93636

        :param livingid: 直播的 id
        :param next_key: 上一次调用时返回的 next_key，初次调用可以填 "0"
        :return:
        """
        data = optionaldict(
            livingid=livingid,
            next_key=next_key,
        )

        return self._post("living/get_watch_stat", data=data)

    def get_living_share_info(self, ww_share_code: str):
        """
        获取跳转小程序商城的直播观众信息

        详情请参考
        https://developer.work.weixin.qq.com/document/path/94442

        :param ww_share_code: “推广产品”直播观众跳转小程序商城时会在小程序 path 中带上 ww_share_code=xxxxx 参数
        :return:
        """
        data = optionaldict(
            ww_share_code=ww_share_code,
        )

        return self._post("living/get_living_share_info", data=data)
