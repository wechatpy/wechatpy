# -*- coding: utf-8 -*-

from optionaldict import optionaldict
from wechatpy.client.api.base import BaseWeChatAPI


class MerchantOrder(BaseWeChatAPI):

    API_BASE_URL = "https://api.weixin.qq.com/"

    def get(self, order_id):
        res = self._post(
            "merchant/order/getbyid",
            data={"order_id": order_id},
            result_processor=lambda x: x["order"],
        )
        return res

    def get_by_filter(self, status=None, begin_time=None, end_time=None):
        filter_dict = optionaldict(status=status, begintime=begin_time, endtime=end_time)

        res = self._post(
            "merchant/order/getbyfilter",
            data=dict(filter_dict),
            result_processor=lambda x: x["order_list"],
        )
        return res

    def set_delivery(self, order_id, company, track_no, need_delivery=1, is_others=0):
        return self._post(
            "merchant/order/setdelivery",
            data={
                "order_id": order_id,
                "delivery_company": company,
                "delivery_track_no": track_no,
                "need_delivery": need_delivery,
                "is_others": is_others,
            },
        )

    def close(self, order_id):
        return self._post("merchant/order/close", data={"order_id": order_id})
