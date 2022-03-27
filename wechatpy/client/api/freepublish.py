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
