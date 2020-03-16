# -*- coding: utf-8 -*-

from wechatpy.client.api.base import BaseWeChatAPI


class MerchantCommon(BaseWeChatAPI):

    API_BASE_URL = "https://api.weixin.qq.com/"

    def upload_image(self, filename, image_data):
        res = self._post(
            "merchant/common/upload_img",
            params={"filename": filename},
            data=image_data,
            result_processor=lambda x: x["image_url"],
        )
        return res
