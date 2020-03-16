# -*- coding: utf-8 -*-


import requests

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMedia(BaseWeChatAPI):
    """
    素材管理

    https://work.weixin.qq.com/api/doc#90000/90135/91054
    """

    def upload(self, media_type, media_file):
        """
        上传临时素材

        https://work.weixin.qq.com/api/doc#90000/90135/90253

        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和普通文件（file）
        :param media_file: 要上传的文件，一个 File-object
        :return: 返回的 JSON 数据包
        """
        return self._post("media/upload", params={"type": media_type}, files={"media": media_file})

    def upload_img(self, image_file):
        """
        上传永久图片

        https://work.weixin.qq.com/api/doc#90000/90135/90256

        上传图片得到图片URL，该URL永久有效。
        返回的图片URL，仅能用于图文消息（mpnews）正文中的图片展示；若用于非企业微信域名下的页面，图片将被屏蔽。
        每个企业每天最多可上传100张图片。
        图片文件大小应在 5B ~ 2MB 之间。

        :return: 返回的 JSON 数据包
        """
        return self._post("media/uploadimg", files={"media": image_file})

    def get_url(self, media_id):
        """
        获取临时素材

        https://work.weixin.qq.com/api/doc#90000/90135/90254

        :param media_id: 媒体文件id
        :return: 临时素材下载地址
        """
        parts = (
            "https://qyapi.weixin.qq.com/cgi-bin/media/get",
            "?access_token=",
            self.access_token,
            "&media_id=",
            media_id,
        )
        return "".join(parts)

    def get_jssdk_url(self, media_id):
        """
        获取高清语音素材

        https://work.weixin.qq.com/api/doc#90000/90135/90255

        :param media_id: 通过JSSDK的uploadVoice接口上传的语音文件id
        :return: 高清语音素材下载地址
        """
        parts = (
            "https://qyapi.weixin.qq.com/cgi-bin/media/get/jssdk",
            "?access_token=",
            self.access_token,
            "&media_id=",
            media_id,
        )
        return "".join(parts)

    def download(self, media_id):
        """
        获取临时素材文件

        https://work.weixin.qq.com/api/doc#90000/90135/90254

        :param media_id: 媒体文件id
        :return: requests 的 Response 实例
        """
        return requests.get(self.get_url(media_id))
