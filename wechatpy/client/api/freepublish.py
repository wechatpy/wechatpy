from wechatpy.client.api.base import BaseWeChatAPI


class WeChatFreePublish(BaseWeChatAPI):
    def submit(self, media_id: str) -> dict:
        """
        发布接口

        详情请参考：
        https://developers.weixin.qq.com/doc/offiaccount/Publish/Publish.html

        :param media_id: 要发布的草稿的media_id
        :return: 返回的 JSON 数据包
        """
        return self._post("freepublish/submit", data={"media_id": media_id})

    def get(self, publish_id: str) -> dict:
        """
        发布状态轮询接口
        开发者可以尝试通过下面的发布状态轮询接口获知发布情况。

        详情请参考：
        https://developers.weixin.qq.com/doc/offiaccount/Publish/Get_status.html

        :param publish_id: 发布任务id
        :return: 返回的 JSON 数据包
        """
        return self._post("freepublish/get", data={"publish_id": publish_id})

    def delete(self, article_id: str, index: int = 0) -> dict:
        """
        删除发布
        发布成功之后，随时可以通过该接口删除。此操作不可逆，请谨慎操作。

        详情请参考：
        https://developers.weixin.qq.com/doc/offiaccount/Publish/Delete_posts.html

        :param article_id: 成功发布时返回的 article_id
        :param index: 要删除的文章在图文消息中的位置，第一篇编号为1，该字段不填或填 0 会删除全部文章
        :return: 返回的 JSON 数据包
        """
        return self._post("freepublish/delete", data={"article_id": article_id, "index": index})
