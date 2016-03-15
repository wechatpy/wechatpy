# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.utils import json
from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMaterial(BaseWeChatAPI):

    def add_articles(self, articles):
        """
        新增永久图文素材
        详情请参考
        http://mp.weixin.qq.com/wiki/14/7e6c03263063f4813141c3e17dd4350a.html

        :param articles: 图文素材数组
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
            'material/add_news',
            data={
                'articles': articles_data
            }
        )

    def add(self, media_type, media_file, title=None, introduction=None):
        """
        新增其它类型永久素材
        详情请参考
        http://mp.weixin.qq.com/wiki/14/7e6c03263063f4813141c3e17dd4350a.html

        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param media_file: 要上传的文件，一个 File-object
        :param title: 视频素材标题，仅上传视频素材时需要
        :param introduction: 视频素材简介，仅上传视频素材时需要
        :return: 返回的 JSON 数据包
        """
        params = {
            'access_token': self.access_token,
            'type': media_type
        }
        if media_type == 'video':
            assert title, 'Video title must be set'
            assert introduction, 'Video introduction must be set'
            description = {
                'title': title,
                'introduction': introduction
            }
            params['description'] = json.dumps(description)
        return self._post(
            'material/add_material',
            params=params,
            files={
                'media': media_file
            }
        )

    def get(self, media_id):
        """
        获取永久素材
        详情请参考
        http://mp.weixin.qq.com/wiki/4/b3546879f07623cb30df9ca0e420a5d0.html

        :param media_id: 素材的 media_id
        :return: 图文素材返回图文列表，其它类型为素材的内容
        """
        def _processor(res):
            if isinstance(res, dict):
                # 图文素材
                return res.get('news_item', [])
            return res

        res = self._post(
            'material/get_material',
            data={
                'media_id': media_id
            },
            result_processor=_processor
        )
        return res

    def delete(self, media_id):
        """
        删除永久素材
        详情请参考
        http://mp.weixin.qq.com/wiki/5/e66f61c303db51a6c0f90f46b15af5f5.html

        :param media_id: 素材的 media_id
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'material/del_material',
            data={
                'media_id': media_id
            }
        )

    def update_articles(self, media_id, index, articles):
        """
        修改永久图文素材
        详情请参考
        http://mp.weixin.qq.com/wiki/4/19a59cba020d506e767360ca1be29450.html

        :param media_id: 要修改的图文消息的 id
        :param index: 要更新的文章在图文消息中的位置（多图文消息时，此字段才有意义），第一篇为 0
        :param articles: 图文素材数组
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
            'material/update_news',
            data={
                'media_id': media_id,
                'index': index,
                'articles': articles_data
            }
        )

    def batchget(self, media_type, offset=0, count=20):
        """
        批量获取永久素材列表
        详情请参考
        http://mp.weixin.qq.com/wiki/12/2108cd7aafff7f388f41f37efa710204.html

        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（news）
        :param offset: 从全部素材的该偏移位置开始返回，0 表示从第一个素材返回
        :param count: 返回素材的数量，取值在1到20之间
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'material/batchget_material',
            data={
                'type': media_type,
                'offset': offset,
                'count': count
            }
        )

    def get_count(self):
        """
        获取素材总数
        详情请参考
        http://mp.weixin.qq.com/wiki/16/8cc64f8c189674b421bee3ed403993b8.html

        :return: 返回的 JSON 数据包
        """
        return self._get('material/get_materialcount')
