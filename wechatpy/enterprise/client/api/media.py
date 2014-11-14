# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMedia(BaseWeChatAPI):

    def upload(self, media_type, media_file):
        return self._post(
            'media/upload',
            params={
                'type': media_type
            },
            files={
                'media': media_file
            }
        )

    def download(self, media_id):
        return self._get(
            'media/get',
            params={
                'media_id': media_id
            }
        )
