# -*- coding: utf-8 -*-

from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatSemantic(BaseWeChatAPI):
    def search(
        self,
        query,
        category,
        uid=None,
        latitude=None,
        longitude=None,
        city=None,
        region=None,
    ):
        """
        发送语义理解请求
        详情请参考
        http://mp.weixin.qq.com/wiki/0/0ce78b3c9524811fee34aba3e33f3448.html

        :param query: 输入文本串
        :param category: 需要使用的服务类型，多个可传入列表
        :param uid: 可选，用户唯一id（非开发者id），用户区分公众号下的不同用户（建议填入用户openid）
        :param latitude: 可选，纬度坐标，与经度同时传入；与城市二选一传入
        :param longitude: 可选，经度坐标，与纬度同时传入；与城市二选一传入
        :param city: 可选，城市名称，与经纬度二选一传入
        :param region: 可选，区域名称，在城市存在的情况下可省；与经纬度二选一传入
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.semantic.search(
                '查一下明天从北京到上海的南航机票',
                'flight,hotel',
                city='北京'
            )

        """
        if isinstance(category, (tuple, list)):
            category = ",".join(category)

        data = optionaldict()
        data["query"] = query
        data["category"] = category
        data["uid"] = uid
        data["latitude"] = latitude
        data["longitude"] = longitude
        data["city"] = city
        data["region"] = region
        data["appid"] = self._client.appid
        return self._post(url="https://api.weixin.qq.com/semantic/semproxy/search", data=data)
