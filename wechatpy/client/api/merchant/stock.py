# -*- coding: utf-8 -*-

from wechatpy.client.api.base import BaseWeChatAPI


class MerchantStock(BaseWeChatAPI):

    API_BASE_URL = "https://api.weixin.qq.com/"

    def add(self, product_id, quantity, sku_info=""):
        return self._post(
            "merchant/stock/add",
            data={"product_id": product_id, "quantity": quantity, "sku_info": sku_info},
        )

    def reduce(self, product_id, quantity, sku_info=""):
        return self._post(
            "merchant/stock/reduce",
            data={"product_id": product_id, "quantity": quantity, "sku_info": sku_info},
        )
