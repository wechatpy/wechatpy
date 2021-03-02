# -*- coding: utf-8 -*-
import operator
from typing import Dict, List, Tuple

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatTemplate(BaseWeChatAPI):
    """包含了模板消息(旧)以及订阅通知(新)的接口，以

    模板消息: https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html
    订阅通知: https://developers.weixin.qq.com/doc/offiaccount/Subscription_Messages/intro.html

    旧的模板消息，接口不变
    新的订阅通知模板，类似官方对订阅消息的取名 SubscribeMsg, 我们以 subscribe_message_template 命名予以区分
    """

    API_BASE_URL = "https://api.weixin.qq.com/"

    def set_industry(self, industry_id1, industry_id2):
        """
        【模板消息】设置所属行业
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html#0

        :param industry_id1: 公众号模板消息所属行业编号
        :param industry_id2: 公众号模板消息所属行业编号
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "cgi-bin/template/api_set_industry",
            data={"industry_id1": industry_id1, "industry_id2": industry_id2},
        )

    def get_industry(self):
        """
        【模板消息】获取设置的行业信息
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html#1

        :return: 返回的 JSON 数据包
        """
        return self._get("cgi-bin/template/get_industry")

    def get(self, template_id_short):
        """
        【模板消息】获得模板ID
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html#2

        :param template_id_short: 模板库中模板的编号，有“TM**”和“OPENTMTM**”等形式
        :return: 模板 ID
        """
        res = self._post(
            "cgi-bin/template/api_add_template",
            data={"template_id_short": template_id_short},
            result_processor=operator.itemgetter("template_id"),
        )
        return res

    add = get

    def get_all_private_template(self):
        """
        【模板消息】获取模板列表
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html#3

        :return: 返回的 JSON 数据包
        """
        return self._get("cgi-bin/template/get_all_private_template")

    def del_private_template(self, template_id):
        """
        【模板消息】删除模板
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html#4

        :param template_id: 公众帐号下模板消息ID
        :return: 返回的 JSON 数据包
        """
        return self._post("cgi-bin/template/del_private_template", data={"template_id": template_id})

    def add_subscribe_message_template(self, tid: str, keywords: List[int], description: str) -> str:
        """
        【订阅通知】选用模板 (使用 tid 换取 template_id)
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Subscription_Messages/api.html#addTemplate%E9%80%89%E7%94%A8%E6%A8%A1%E6%9D%BF

        返回：添加至帐号下的模板 template_id，发送订阅通知时所需
        """
        return self._post(
            "wxaapi/newtmpl/addtemplate",
            data={
                "tid": tid,
                "kidList": keywords,
                "sceneDesc": description,
            },
            result_processor=operator.itemgetter("priTmplId"),
        )

    def del_subscribe_message_template(self, template_id: str):
        """
        【订阅通知】删除模板 (删除 template_id)
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Subscription_Messages/api.html#addTemplate%E9%80%89%E7%94%A8%E6%A8%A1%E6%9D%BF
        """
        return self._post("wxaapi/newtmpl/deltemplate", data={"priTmplId": template_id})

    def get_category(self) -> List[Dict]:
        """
        【订阅通知】获取公众号类目
        详情请参考:
        https://developers.weixin.qq.com/doc/offiaccount/Subscription_Messages/api.html#addTemplate%E9%80%89%E7%94%A8%E6%A8%A1%E6%9D%BF

        返回数据参考:
        [
          { "id": 616, "name": "公交" }
        ]
        """
        return self._get("wxaapi/newtmpl/getcategory", result_processor=operator.itemgetter("data"))

    def get_subscribe_message_template_keywords(self, tid: str) -> Tuple[int, List[Dict]]:
        """
        【订阅通知】获取模板中的关键词
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Subscription_Messages/api.html#addTemplate%E9%80%89%E7%94%A8%E6%A8%A1%E6%9D%BF

        返回数据参考:
        (
          10,  # 公共模板列表总数
          [    # 关键词列表
            { "kid": 1, "name": "物品名称", "example": "名称", "rule": "thing" }
          ]
        )
        """
        return self._get(
            "wxaapi/newtmpl/getpubtemplatekeywords",
            params={"tid": tid},
            result_processor=operator.itemgetter("count", "data"),
        )

    def get_subscribe_message_template_titles(self, start: int = 0, limit: int = 30) -> Tuple[int, List[Dict]]:
        """
        【订阅通知】获取所属类目的公共模板
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Subscription_Messages/api.html#addTemplate%E9%80%89%E7%94%A8%E6%A8%A1%E6%9D%BF

        返回数据参考:
        (
          10,  # 公共模板列表总数
          [    # 模板标题列表
            { "tid": 99, "title": "付款成功通知", "type": 2, "categoryId": "616" }
          ]
        )
        """
        return self._get(
            "wxaapi/newtmpl/getpubtemplatetitles",
            params={"start": start, "limit": limit},
            result_processor=operator.itemgetter("count", "data"),
        )

    def get_subscribe_message_templates(self) -> List[Dict]:
        """
        【订阅通知】获取私有模板列表
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Subscription_Messages/api.html#addTemplate%E9%80%89%E7%94%A8%E6%A8%A1%E6%9D%BF

        返回数据参考:
        [
          {
            "priTmplId": "9Aw5ZV1j9xdWTFEkqCpZ7mIBbSC34khK55OtzUPl0rU",
            "title": "报名结果通知",
            "content": "会议时间:{{date2.DATA}}\n会议地点:{{thing1.DATA}}\n",
            "example": "会议时间:2016年8月8日\n会议地点:TIT会议室\n",
            "type": 2
          }
        ]
        """
        return self._get("wxaapi/newtmpl/gettemplate", result_processor=operator.itemgetter("data"))

    # send 接口参见 wechatpy.client.api.message.WeChatMessage.send_subscribe_message
