# -*- coding: utf-8 -*-

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatPoi(BaseWeChatAPI):
    """微信门店

    https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Store_Interface.html
    """

    def add(self, poi_data):
        """
        创建门店

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Store_Interface.html#7

        :param poi_data: 门店信息字典
        :return: 返回的 JSON 数据包
        """
        return self._post("poi/addpoi", data=poi_data)

    def get(self, poi_id):
        """
        查询门店信息

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Store_Interface.html#9

        :param poi_id: 门店 ID
        :return: 返回的 JSON 数据包
        """
        return self._post("poi/getpoi", data={"poi_id": poi_id})

    def list(self, begin=0, limit=20):
        """
        查询门店列表

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Store_Interface.html#10

        :param begin: 开始位置，0 即为从第一条开始查询
        :param limit: 返回数据条数，最大允许50，默认为20
        :return: 返回的 JSON 数据包
        """
        return self._post("poi/getpoilist", data={"begin": begin, "limit": limit})

    def update(self, poi_data):
        """
        修改门店服务信息

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Store_Interface.html#11

        :param poi_data: 门店信息字典
        :return: 返回的 JSON 数据包
        """
        return self._post("poi/updatepoi", data=poi_data)

    def delete(self, poi_id):
        """
        删除门店

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Store_Interface.html#12

        :param poi_id: 门店 ID
        :return: 返回的 JSON 数据包
        """
        return self._post("poi/delpoi", data={"poi_id": poi_id})

    def get_categories(self):
        """
        获取微信门店类目表

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Store_Interface.html#13

        :return: 门店类目表
        """
        res = self._get("api_getwxcategory", result_processor=lambda x: x["category_list"])
        return res
