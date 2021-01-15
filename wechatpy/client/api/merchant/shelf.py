# -*- coding: utf-8 -*-

from wechatpy.client.api.base import BaseWeChatAPI


class MerchantShelf(BaseWeChatAPI):

    API_BASE_URL = "https://api.weixin.qq.com/"

    def add(self, name, banner, shelf_data):
        return self._post(
            "merchant/shelf/add",
            data={"shelf_name": name, "shelf_banner": banner, "shelf_data": shelf_data},
        )

    def delete(self, shelf_id):
        return self._post("merchant/shelf/del", data={"shelf_id": shelf_id})

    def update(self, shelf_id, name, banner, shelf_data):
        return self._post(
            "merchant/shelf/add",
            data={
                "shelf_id": shelf_id,
                "shelf_name": name,
                "shelf_banner": banner,
                "shelf_data": shelf_data,
            },
        )

    def get_all(self):
        res = self._get("merchant/shelf/getall", result_processor=lambda x: x["shelves"])
        return res

    def get(self, shelf_id):
        return self._post("merchant/shelf/getbyid", data={"shelf_id": shelf_id})
