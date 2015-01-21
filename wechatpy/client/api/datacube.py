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
