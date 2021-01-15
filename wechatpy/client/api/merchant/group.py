# -*- coding: utf-8 -*-

from wechatpy.client.api.base import BaseWeChatAPI


class MerchantGroup(BaseWeChatAPI):

    API_BASE_URL = "https://api.weixin.qq.com/"

    def add(self, name, product_list):
        return self._post(
            "merchant/group/add",
            data={"group_detail": {"group_name": name, "product_list": product_list}},
        )

    def delete(self, group_id):
        return self._post("merchant/group/del", data={"group_id": group_id})

    def update(self, group_id, name):
        return self._post(
            "merchant/group/propertymod",
            data={"group_id": group_id, "group_name": name},
        )

    def update_product(self, group_id, product):
        return self._post("merchant/group/productmod", data={"group_id": group_id, "product": product})

    def get_all(self):
        res = self._get("merchant/group/getall", result_processor=lambda x: x["groups_detail"])
        return res

    def get(self, group_id):
        res = self._post(
            "merchant/group/getbyid",
            data={"group_id": group_id},
            result_processor=lambda x: x["group_detail"],
        )
        return res
