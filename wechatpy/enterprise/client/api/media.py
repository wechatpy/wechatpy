# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import requests

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMedia(BaseWeChatAPI):

    def upload(self, media_type, media_file):
        """
        上传临时素材文件
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=%E4%B8%8A%E4%BC%A0%E4%B8%B4%E6%97%B6%E7%B4%A0%E6%9D%90%E6%96%87%E4%BB%B6
        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和普通文件（file）
        :param media_file: 要上传的文件，一个 File-object
        :return: 返回的 JSON 数据包
        """
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
        """
        获取临时素材文件
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=%E8%8E%B7%E5%8F%96%E4%B8%B4%E6%97%B6%E7%B4%A0%E6%9D%90%E6%96%87%E4%BB%B6
        :param media_id: 媒体文件 ID
        :return: requests 的 Response 实例
        """
        return requests.get(self.get_url(media_id))

    def get_url(self, media_id):
        """
        获取临时素材下载地址
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=%E8%8E%B7%E5%8F%96%E4%B8%B4%E6%97%B6%E7%B4%A0%E6%9D%90%E6%96%87%E4%BB%B6
        :param media_id: 媒体文件 ID
        :return: 临时素材下载地址
        """
        parts = (
            'https://qyapi.weixin.qq.com/cgi-bin/media/get',
            '?access_token=',
            self.access_token,
            '&media_id=',
            media_id
        )
        return ''.join(parts)
