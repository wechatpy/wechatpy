# -*- coding: utf-8 -*-
import json

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMaterial(BaseWeChatAPI):
    def add_articles(self, articles):
        """
        新增永久图文素材
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Adding_Permanent_Assets.html

        :param articles: 图文素材数组
        :type articles: list[dict]
        :return: 返回的 JSON 数据包
        """
        articles_data = []
        for article in articles:
            articles_data.append(
                {
                    "thumb_media_id": article["thumb_media_id"],
                    "title": article["title"],
                    "content": article["content"],
                    "author": article.get("author", ""),
                    "content_source_url": article.get("content_source_url", ""),
                    "digest": article.get("digest", ""),
                    "show_cover_pic": article.get("show_cover_pic", 0),
                    "need_open_comment": int(article.get("need_open_comment", False)),
                    "only_fans_can_comment": int(article.get("only_fans_can_comment", False)),
                }
            )
        return self._post("material/add_news", data={"articles": articles_data})

    def add(self, media_type, media_file, title=None, introduction=None):
        """
        新增其它类型永久素材
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Adding_Permanent_Assets.html

        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param media_file: 要上传的文件，一个 File-object
        :param title: 视频素材标题，仅上传视频素材时需要
        :param introduction: 视频素材简介，仅上传视频素材时需要
        :return: 返回的 JSON 数据包
        """
        params = {"access_token": self.access_token, "type": media_type}
        if media_type == "video":
            assert title, "Video title must be set"
            assert introduction, "Video introduction must be set"
            description = {"title": title, "introduction": introduction}
            params["description"] = json.dumps(description)
        return self._post("material/add_material", params=params, files={"media": media_file})

    def get(self, media_id):
        """
        获取永久素材
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Getting_Permanent_Assets.html

        :param media_id: 素材的 media_id
        :return: 图文素材返回图文列表，其它类型为素材的内容
        """

        def _processor(res):
            if isinstance(res, dict):
                if "news_item" in res:
                    # 图文素材
                    return res["news_item"]
            return res

        return self._post(
            "material/get_material",
            data={"media_id": media_id},
            result_processor=_processor,
        )

    def delete(self, media_id):
        """
        删除永久素材
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Deleting_Permanent_Assets.html

        :param media_id: 素材的 media_id
        :return: 返回的 JSON 数据包
        """
        return self._post("material/del_material", data={"media_id": media_id})

    def update_article(self, media_id, index, article):
        """
        修改永久图文素材
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Editing_Permanent_Rich_Media_Assets.html

        :param media_id: 要修改的图文消息的 id
        :param index: 要更新的文章在图文消息中的位置（多图文消息时，此字段才有意义），第一篇为 0
        :param article: 图文素材
        :return: 返回的 JSON 数据包
        """
        article_data = {
            "thumb_media_id": article["thumb_media_id"],
            "title": article["title"],
            "content": article["content"],
            "author": article.get("author", ""),
            "content_source_url": article.get("content_source_url", ""),
            "digest": article.get("digest", ""),
            "show_cover_pic": article.get("show_cover_pic", 0),
        }
        return self._post(
            "material/update_news",
            data={"media_id": media_id, "index": index, "articles": article_data},
        )

    def update_articles(self, media_id, index, articles):
        """
        修改永久图文素材
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Editing_Permanent_Rich_Media_Assets.html

        :param media_id: 要修改的图文消息的 id
        :param index: 要更新的文章在图文消息中的位置（多图文消息时，此字段才有意义），第一篇为 0
        :param articles: 图文素材数组
        :return: 返回的 JSON 数据包
        """
        return self.update_article(media_id, index, articles[index])

    def batchget(self, media_type, offset=0, count=20):
        """
        获取素材列表
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Get_materials_list.html

        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（news）
        :param offset: 从全部素材的该偏移位置开始返回，0 表示从第一个素材返回
        :param count: 返回素材的数量，取值在1到20之间
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "material/batchget_material",
            data={"type": media_type, "offset": offset, "count": count},
        )

    def get_count(self):
        """
        获取素材总数
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Get_the_total_of_all_materials.html

        :return: 返回的 JSON 数据包
        """
        return self._get("material/get_materialcount")

    def open_comment(self, msg_data_id, index=1):
        """
        打开已群发文章评论
        https://mp.weixin.qq.com/wiki?id=mp1494572718_WzHIY
        """
        return self._post(
            "comment/open",
            data={
                "msg_data_id": msg_data_id,
                "index": index,
            },
        )

    def close_comment(self, msg_data_id, index=1):
        """
        关闭已群发文章评论
        """
        return self._post(
            "comment/close",
            data={
                "msg_data_id": msg_data_id,
                "index": index,
            },
        )

    def list_comment(self, msg_data_id, index=1, begin=0, count=50, type=0):
        """
        查看指定文章的评论数据
        """
        return self._post(
            "comment/list",
            data={
                "msg_data_id": msg_data_id,
                "index": index,
                "begin": begin,
                "count": count,
                "type": type,
            },
        )

    def markelect_comment(self, msg_data_id, index, user_comment_id):
        """
        将评论标记精选
        """
        return self._post(
            "comment/markelect",
            data={
                "msg_data_id": msg_data_id,
                "index": index,
                "user_comment_id": user_comment_id,
            },
        )

    def unmarkelect_comment(self, msg_data_id, index, user_comment_id):
        """
        将评论取消精选
        """
        return self._post(
            "comment/unmarkelect",
            data={
                "msg_data_id": msg_data_id,
                "index": index,
                "user_comment_id": user_comment_id,
            },
        )

    def delete_comment(self, msg_data_id, index, user_comment_id):
        """
        删除评论
        """
        return self._post(
            "comment/delete",
            data={
                "msg_data_id": msg_data_id,
                "index": index,
                "user_comment_id": user_comment_id,
            },
        )

    def add_reply_comment(self, msg_data_id, index, user_comment_id, content):
        """
        回复评论
        """
        return self._post(
            "comment/reply/add",
            data={
                "msg_data_id": msg_data_id,
                "index": index,
                "user_comment_id": user_comment_id,
                "content": content,
            },
        )

    def delete_reply_comment(self, msg_data_id, index, user_comment_id):
        """
        删除回复
        """
        return self._post(
            "comment/reply/delete",
            data={
                "msg_data_id": msg_data_id,
                "index": index,
                "user_comment_id": user_comment_id,
            },
        )
