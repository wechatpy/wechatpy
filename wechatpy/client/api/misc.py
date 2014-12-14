# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import time
import datetime

from .base import BaseWeChatAPI


class WeChatMisc(BaseWeChatAPI):

    def short_url(self, long_url):
        """
        将一条长链接转成短链接
        详情请参考
        http://mp.weixin.qq.com/wiki/10/165c9b15eddcfbd8699ac12b0bd89ae6.html

        :param long_url: 长链接地址
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'shorturl',
            data={
                'action': 'long2short',
                'long_url': long_url
            }
        )

    def get_customservice_record(self, start_time, end_time, page_index,
                                 page_size=10, user_id=None):
        """
        获取客服聊天记录
        详情请参考
        http://mp.weixin.qq.com/wiki/19/7c129ec71ddfa60923ea9334557e8b23.html

        :param start_time: 查询开始时间，UNIX 时间戳
        :param end_time: 查询结束时间，UNIX 时间戳，每次查询不能跨日查询
        :param page_index: 查询第几页，从 1 开始
        :param page_size: 每页大小，每页最多拉取 1000 条
        :param user_id: 普通用户的标识，对当前公众号唯一

        :return: 返回的 JSON 数据包
        """
        if isinstance(start_time, datetime.datetime):
            start_time = time.mktime(start_time.timetuple())
        if isinstance(end_time, datetime.datetime):
            end_time = time.mktime(end_time.timetuple())
        record_data = {
            'starttime': int(start_time),
            'endtime': int(end_time),
            'pageindex': page_index,
            'pagesize': page_size
        }
        if user_id:
            record_data['openid'] = user_id
        return self._post(
            'customservice/getrecord',
            data=record_data
        )

    def get_wechat_ips(self):
        """
        获取微信服务器 IP 地址列表

        :return: IP 地址列表
        """
        res = self._get('getcallbackip')
        return res['ip_list']
