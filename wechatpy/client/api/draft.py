# -*- coding: utf-8 -*-
import json

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatDraft(BaseWeChatAPI):
    def add(self, articles):
        """
        新增草稿素材, 原 新增永久图文素材
        用于替换原本的新增永久图文素材 add_articles 方法
        详情参考
        https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html

        :param articles: 图文素材数组
        :type articles: list[dict]
        :return: 返回的 JSON 数据包
        """
        articles_data = []
        for article in articles:
            articles_data.append(
                {
                    "title": article["title"],
                    "author": article.get("author", ""),
                    "digest": article.get("digest", ""),
                    "content": article["content"],
                    "content_source_url": article.get("content_source_url", ""),
                    "thumb_media_id": article["thumb_media_id"],
                    "need_open_comment": int(article.get("need_open_comment", False)),
                    "only_fans_can_comment": int(article.get("only_fans_can_comment", False)),
                }
            )
        return self._post("draft/add", data={"articles": articles_data})

    def get(self, media_id: str) -> dict:
        """
        获取草稿
        新增草稿后，开发者可以根据草稿指定的字段来下载草稿。
        详情参考
        https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Get_draft.html

        :param media_id: 要获取的草稿的 media_id
        :type media_id: str
        :return: 返回的 JSON 数据包
        """
        return self._post("draft/get", data={"media_id": media_id})
