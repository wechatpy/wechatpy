# -*- coding: utf-8 -*-

import datetime
from operator import itemgetter

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatDataCube(BaseWeChatAPI):

    API_BASE_URL = "https://api.weixin.qq.com/datacube/"

    @classmethod
    def _to_date_str(cls, date):
        if isinstance(date, datetime.date):
            return date.strftime("%Y-%m-%d")
        elif isinstance(date, str):
            return date
        else:
            raise ValueError("Can not convert %s type to str", type(date))

    def get_user_summary(self, begin_date, end_date):
        """
        获取用户增减数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/User_Analysis_Data_Interface.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getusersummary",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
        )
        return res["list"]

    def get_user_cumulate(self, begin_date, end_date):
        """
        获取累计用户数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/User_Analysis_Data_Interface.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getusercumulate",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_interface_summary(self, begin_date, end_date):
        """
        获取接口分析数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/Analytics_API.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getinterfacesummary",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_interface_summary_hour(self, begin_date, end_date):
        """
        获取接口分析分时数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/Analytics_API.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getinterfacesummaryhour",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_article_summary(self, begin_date, end_date):
        """
        获取图文群发每日数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/Graphic_Analysis_Data_Interface.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getarticlesummary",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_article_total(self, begin_date, end_date):
        """
        获取图文群发总数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/Graphic_Analysis_Data_Interface.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getarticletotal",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_user_read(self, begin_date, end_date):
        """
        获取图文统计数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/Graphic_Analysis_Data_Interface.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getuserread",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_user_read_hour(self, begin_date, end_date):
        """
        获取图文分时统计数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/Graphic_Analysis_Data_Interface.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getuserreadhour",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_user_share(self, begin_date, end_date):
        """
        获取图文分享转发数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/Graphic_Analysis_Data_Interface.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getusershare",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_user_share_hour(self, begin_date, end_date):
        """
        获取图文分享转发分时数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/Graphic_Analysis_Data_Interface.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getusersharehour",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_upstream_msg(self, begin_date, end_date):
        """
        获取消息发送概况数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/Message_analysis_data_interface.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getupstreammsg",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_upstream_msg_hour(self, begin_date, end_date):
        """
        获取消息发送分时数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/Message_analysis_data_interface.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getupstreammsghour",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_upstream_msg_week(self, begin_date, end_date):
        """
        获取消息发送周数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/Message_analysis_data_interface.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getupstreammsgweek",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_upstream_msg_month(self, begin_date, end_date):
        """
        获取消息发送月数据
        详情请参考
        http://mp.weixin.qq.com/wiki/12/32d42ad542f2e4fc8a8aa60e1bce9838.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getupstreammsgmonth",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_upstream_msg_dist(self, begin_date, end_date):
        """
        获取消息发送分布数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/Message_analysis_data_interface.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getupstreammsgdist",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_upstream_msg_dist_week(self, begin_date, end_date):
        """
        获取消息发送分布周数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/Message_analysis_data_interface.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getupstreammsgdistweek",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res

    def get_upstream_msg_dist_month(self, begin_date, end_date):
        """
        获取消息发送分布月数据
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Analytics/Message_analysis_data_interface.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            "getupstreammsgdistmonth",
            data={
                "begin_date": self._to_date_str(begin_date),
                "end_date": self._to_date_str(end_date),
            },
            result_processor=itemgetter("list"),
        )
        return res
