# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.client.api.base import BaseWeChatAPI


class MerchantCommon(BaseWeChatAPI):

    def upload_image(self, filename, image_data):
        res = self._post(
            'merchant/common/upload_img',
            params={
                'filename': filename
            },
            data=image_data,
            result_processor=lambda x: x['image_url']
        )
        return res
