# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import datetime

import six

from .base import BaseWeChatAPI


class WeChatDataCube(BaseWeChatAPI):

    @classmethod
    def _to_date_str(cls, date):
        if isinstance(date, (datetime.datetime, datetime.date)):
            return date.strftime('%Y-%m-%d')
        elif isinstance(date, six.string_types):
            return date
        else:
            raise ValueError('Can not convert %s type to str', type(date))

    def get_user_summary(self, begin_date, end_date):
        """
        获取用户增减数据
        详情请参考
        http://mp.weixin.qq.com/wiki/3/ecfed6e1a0a03b5f35e5efac98e864b7.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getusersummary',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_user_cumulate(self, begin_date, end_date):
        """
        获取累计用户数据
        详情请参考
        http://mp.weixin.qq.com/wiki/3/ecfed6e1a0a03b5f35e5efac98e864b7.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getusercumulate',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_interface_summary(self, begin_date, end_date):
        """
        获取接口分析数据
        详情请参考
        http://mp.weixin.qq.com/wiki/8/30ed81ae38cf4f977194bf1a5db73668.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getinterfacesummary',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_interface_summary_hour(self, begin_date, end_date):
        """
        获取接口分析分时数据
        详情请参考
        http://mp.weixin.qq.com/wiki/8/30ed81ae38cf4f977194bf1a5db73668.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getinterfacesummaryhour',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_article_summary(self, begin_date, end_date):
        """
        获取图文群发每日数据
        详情请参考
        http://mp.weixin.qq.com/wiki/8/c0453610fb5131d1fcb17b4e87c82050.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getarticlesummary',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_article_total(self, begin_date, end_date):
        """
        获取图文群发总数据
        详情请参考
        http://mp.weixin.qq.com/wiki/8/c0453610fb5131d1fcb17b4e87c82050.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getarticletotal',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_user_read(self, begin_date, end_date):
        """
        获取图文统计数据
        详情请参考
        http://mp.weixin.qq.com/wiki/8/c0453610fb5131d1fcb17b4e87c82050.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getuserread',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_user_read_hour(self, begin_date, end_date):
        """
        获取图文分时统计数据
        详情请参考
        http://mp.weixin.qq.com/wiki/8/c0453610fb5131d1fcb17b4e87c82050.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getuserreadhour',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_user_share(self, begin_date, end_date):
        """
        获取图文分享转发数据
        详情请参考
        http://mp.weixin.qq.com/wiki/8/c0453610fb5131d1fcb17b4e87c82050.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getusershare',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_user_share_hour(self, begin_date, end_date):
        """
        获取图文分享转发分时数据
        详情请参考
        http://mp.weixin.qq.com/wiki/8/c0453610fb5131d1fcb17b4e87c82050.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getusersharehour',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_upstream_msg(self, begin_date, end_date):
        """
        获取消息发送概况数据
        详情请参考
        http://mp.weixin.qq.com/wiki/12/32d42ad542f2e4fc8a8aa60e1bce9838.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getupstreammsg',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_upstream_msg_hour(self, begin_date, end_date):
        """
        获取消息发送分时数据
        详情请参考
        http://mp.weixin.qq.com/wiki/12/32d42ad542f2e4fc8a8aa60e1bce9838.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getupstreammsghour',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_upstream_msg_week(self, begin_date, end_date):
        """
        获取消息发送周数据
        详情请参考
        http://mp.weixin.qq.com/wiki/12/32d42ad542f2e4fc8a8aa60e1bce9838.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getupstreammsgweek',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

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
            'datacube/getupstreammsgmonth',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_upstream_msg_dist(self, begin_date, end_date):
        """
        获取消息发送分布数据
        详情请参考
        http://mp.weixin.qq.com/wiki/12/32d42ad542f2e4fc8a8aa60e1bce9838.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getupstreammsgdist',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_upstream_msg_dist_week(self, begin_date, end_date):
        """
        获取消息发送分布数据
        详情请参考
        http://mp.weixin.qq.com/wiki/12/32d42ad542f2e4fc8a8aa60e1bce9838.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getupstreammsgdistweek',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']

    def get_upstream_msg_dist_month(self, begin_date, end_date):
        """
        获取消息发送分布数据
        详情请参考
        http://mp.weixin.qq.com/wiki/12/32d42ad542f2e4fc8a8aa60e1bce9838.html

        :param begin_date: 起始日期
        :param end_date: 结束日期
        :return: 统计数据列表
        """
        res = self._post(
            'datacube/getupstreammsgdistmonth',
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list']
