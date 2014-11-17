# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.client.api.base import BaseWeChatAPI
from wechatpy.utils import NotNoneDict


class MerchantOrder(BaseWeChatAPI):

    def get(self, order_id):
        res = self._post(
            'merchant/order/getbyid',
            data={
                'order_id': order_id
            }
        )
        return res['order']

    def get_by_filter(self, status=None, begin_time=None, end_time=None):
        filter_dict = NotNoneDict()
        filter_dict['status'] = status
        filter_dict['begintime'] = begin_time
        filter_dict['endtime'] = end_time

        res = self._post(
            'merchant/order/getbyfilter',
            data=dict(filter_dict)
        )
        return res['order_list']

    def set_delivery(self, order_id, company, track_no,
                     need_delivery=1, is_others=0):
        return self._post(
            'merchant/order/setdelivery',
            data={
                'order_id': order_id,
                'delivery_company': company,
                'delivery_track_no': track_no,
                'need_delivery': need_delivery,
                'is_others': is_others
            }
        )

    def close(self, order_id):
        return self._post(
            'merchant/order/close',
            data={
                'order_id': order_id
            }
        )
