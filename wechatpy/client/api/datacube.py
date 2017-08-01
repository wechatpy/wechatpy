# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import datetime

import six

from wechatpy.client.api.base import BaseWeChatAPI

"""
用户分析数据接口: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421141082
图文分析数据接口: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421141084
消息分析数据接口: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421141085
接口分析数据接口: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421141086
小程分析数据接口: https://mp.weixin.qq.com/debug/wxadoc/dev/api/analysis.html

# How to usage:
from wechatpy import WeChatClient
client = WeChatClient(appid="your app id", secret="your secret")
result = client.datacube.getweanalysisappiddailysummarytrend(begin_time="2017-07-31", end_time="2017-08-01")
result = client.datacube.getusersummary(begin_time="2017-07-31", end_time="2017-08-01")
"""


class WeChatDataCube(BaseWeChatAPI):

    API_BASE_URL = 'https://api.weixin.qq.com/datacube/'

    @classmethod
    def _to_date_str(cls, date):
        if isinstance(date, (datetime.datetime, datetime.date)):
            return date.strftime('%Y-%m-%d')
        elif isinstance(date, six.string_types):
            return date
        else:
            raise ValueError('Can not convert %s type to str', type(date))

    def __getattr__(self, item):
        return DataCubeObject(item, self)


class DataCubeObject(object):
    def __init__(self, name, proxy):
        self.name = name
        self.proxy = proxy

    def __call__(self, *args, **kwargs):
        begin_date = kwargs.get('begin_date', None)
        end_date = kwargs.get('end_date', None)
        res = self.proxy._post(
            self.name,
            data={
                'begin_date': self._to_date_str(begin_date),
                'end_date': self._to_date_str(end_date)
            }
        )
        return res['list'] if 'list' in res else res
