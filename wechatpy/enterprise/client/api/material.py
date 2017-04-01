# encoding: utf-8
from __future__ import absolute_import, unicode_literals
import requests

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMaterial(BaseWeChatAPI):

    def add_articles(self, articles):
        """
        新增永久图文素材
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=%E4%B8%8A%E4%BC%A0%E6%B0%B8%E4%B9%85%E7%B4%A0%E6%9D%90

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
            'material/add_mpnews',
            data={
                "mpnews": {
                    "articles": articles_data
                    }
                }
        )

    def add(self, agent_id, media_type, media_file):
        """
        新增其它类型永久素材
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=%E4%B8%8A%E4%BC%A0%E6%B0%B8%E4%B9%85%E7%B4%A0%E6%9D%90

        :param agent_id: 企业应用的id
        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）普通文件（file）
        :param media_file: 要上传的文件，一个 File-object
        :return: 返回的 JSON 数据包
        """
        params = {
            'agentid': agent_id,
            'type': media_type,
        }
        return self._post(
            url='material/add_material',
            params=params,
            files={
                'media': media_file
            }
        )

    def get_url(self, agent_id, media_id):
        """
        获取永久素材下载地址
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=%E8%8E%B7%E5%8F%96%E6%B0%B8%E4%B9%85%E7%B4%A0%E6%9D%90

        :param agent_id: 企业应用的id
        :param media_id: 媒体文件 ID
        :return: 临时素材下载地址
        """
        parts = (
            'https://qyapi.weixin.qq.com/cgi-bin/material/get',
            '?access_token=',
            self.access_token,
            '&media_id=',
            media_id,
            '&agentid=',
            agent_id,
        )
        return ''.join(parts)

    def get(self, agent_id, media_id):
        """
        获取永久素材
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=%E8%8E%B7%E5%8F%96%E6%B0%B8%E4%B9%85%E7%B4%A0%E6%9D%90

        :param agent_id: 企业应用的id
        :param media_id: 媒体文件 ID
        :return: requests 的 Response 实例
        """
        res = requests.get(self.get_url(agent_id, media_id))

        return res

    def get_articles(self, agent_id, media_id):
        """
        获取永久素材：图文消息素材
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=%E8%8E%B7%E5%8F%96%E6%B0%B8%E4%B9%85%E7%B4%A0%E6%9D%90

        :param agent_id: 企业应用的id
        :param media_id: 媒体文件 ID
        :return: 返回的 JSON 数据包
        """
        return self._get(
            'material/get',
            params={
                'agentid': agent_id,
                'media_id': media_id,
            }
        )

    def delete(self, agent_id, media_id):
        """
        删除永久素材
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=%E5%88%A0%E9%99%A4%E6%B0%B8%E4%B9%85%E7%B4%A0%E6%9D%90

        :param agent_id: 企业应用的id
        :param media_id: 媒体文件 ID
        :return: 返回的 JSON 数据包
        """
        return self._get(
            'material/del',
            params={
                'agentid': agent_id,
                'media_id': media_id,
            }
        )

    def update_articles(self, agent_id, media_id, articles):
        """
        修改永久图文素材
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=%E4%BF%AE%E6%94%B9%E6%B0%B8%E4%B9%85%E5%9B%BE%E6%96%87%E7%B4%A0%E6%9D%90

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
                'agentid': agent_id,
                'media_id': media_id,
                'articles': articles_data
            }
        )

    def get_count(self, agent_id):
        """
        获取素材总数
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=%E8%8E%B7%E5%8F%96%E7%B4%A0%E6%9D%90%E6%80%BB%E6%95%B0

        :param agent_id: 企业应用的id
        :return: 返回的 JSON 数据包
        """
        return self._get(
            'material/get_count',
            params={
                'agent_id': agent_id,
            }
        )

    def batchget(self, agent_id, media_type, offset=0, count=20):
        """
        批量获取永久素材列表
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=%E8%8E%B7%E5%8F%96%E7%B4%A0%E6%9D%90%E5%88%97%E8%A1%A8

        :param agent_id: 企业应用的id
        :param media_type: 媒体文件类型，分别有图文（mpnews）、图片（image）、
                           语音（voice）、视频（video）和文件（file）
        :param offset: 从全部素材的该偏移位置开始返回，0 表示从第一个素材返回
        :param count: 返回素材的数量，取值在1到20之间
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'material/batchget',
            data={
                'agent_id': agent_id,
                'type': media_type,
                'offset': offset,
                'count': count
            }
        )
