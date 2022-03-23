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

    def delete(self, media_id: str) -> dict:
        """
        删除草稿
        新增草稿后，开发者可以根据本接口来删除不再需要的草稿，节省空间。此操作无法撤销，请谨慎操作。
        详情参考
        https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Delete_draft.html

        :param media_id: 要删除的草稿的 media_id
        :type media_id: str
        :return: 返回的 JSON 数据包
        """
        return self._post("draft/delete", data={"media_id": media_id})

    def update(self, media_id, index, articles) -> dict:
        """
        修改草稿
        开发者可通过本接口对草稿进行修改。
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Update_draft.html

        :param media_id: 要修改的图文消息的 id
        :param index: 要更新的文章在图文消息中的位置（多图文消息时，此字段才有意义），第一篇为 0
        :param articles: 草稿内容，详情见链接
        :return: 返回的 JSON 数据包
        """
        return self._post("draft/update", data={"media_id": media_id, "index": index, "articles": articles})

    def count(self) -> dict:
        """
        获取草稿总数
        开发者可以根据本接口来获取草稿的总数。此接口只统计数量，不返回草稿的具体内容。
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Count_drafts.html

        :return: 返回的 JSON 数据包
        """
        return self._get("draft/count")

    def batchget(self) -> dict:
        """
        获取草稿列表
        新增草稿之后，开发者可以获取草稿的列表。
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Get_draft_list.html

        :return: 返回的 JSON 数据包
        """
        return self._post("draft/batchget")
