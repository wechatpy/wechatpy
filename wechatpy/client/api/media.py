# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import requests

from .base import BaseWeChatAPI


class WeChatMedia(BaseWeChatAPI):

    def upload(self, media_type, media_file):
        """
        上传多媒体文件。
        详情请参考
        http://mp.weixin.qq.com/wiki/10/78b15308b053286e2a66b33f0f0f5fb6.html

        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param media_file: 要上传的文件，一个 File-object

        :return: 返回的 JSON 数据包
        """
        return self._post(
            url='http://file.api.weixin.qq.com/cgi-bin/media/upload',
            params={
                'access_token': self.access_token,
                'type': media_type
            },
            files={
                'media': media_file
            }
        )

    def download(self, media_id):
        """
        下载多媒体文件。
        详情请参考
        http://mp.weixin.qq.com/wiki/10/78b15308b053286e2a66b33f0f0f5fb6.html

        :param media_id: 媒体文件 ID

        :return: requests 的 Response 实例
        """
        return requests.get(
            'http://file.api.weixin.qq.com/cgi-bin/media/get',
            params={
                'access_token': self.access_token,
                'media_id': media_id
            }
        )

    def upload_video(self, media_id, title, description):
        """
        群发视频消息时获取视频 media_id
        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param media_id: 需通过基础支持中的上传下载多媒体文件 :func:`upload` 来得到
        :param title: 视频标题
        :param description: 视频描述

        :return: 返回的 JSON 数据包
        """
        return self._post(
            url='https://file.api.weixin.qq.com/cgi-bin/media/uploadvideo',
            params={
                'access_token': self.access_token
            },
            data={
                'media_id': media_id,
                'title': title,
                'description': description
            }
        )

    def upload_articles(self, articles):
        """
        上传图文消息素材
        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param articles: 图文消息数组
        :return: 返回的 JSON 数据包
        """
        articles_data = []
        for article in articles:
            articles_data.append({
                'thumb_media_id': article['thumb_media_id'],
                'title': article['title'],
                'content': article['content'],
                'author': article.get('author', ''),
                'content_source_url': article.get('content_source_url', ''),
                'digest': article.get('digest', ''),
                'show_cover_pic': article.get('show_cover_pic', 0)
            })
        return self._post(
            'media/uploadnews',
            data={
                'articles': articles_data
            }
        )
