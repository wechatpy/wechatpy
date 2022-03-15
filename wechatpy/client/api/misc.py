# -*- coding: utf-8 -*-
from operator import itemgetter

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMisc(BaseWeChatAPI):
    def short_url(self, long_url):
        """
        将一条长链接转成短链接

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Account_Management/URL_Shortener.html

        该接口即将废弃，详情见公告：
        https://mp.weixin.qq.com/cgi-bin/announce?action=getannouncement&announce_id=11615366683l3hgk&version=63010043&lang=zh_CN&token=

        :param long_url: 长链接地址
        :return: 返回的 JSON 数据包

        使用示例::

        >>>    from wechatpy import WeChatClient
        >>>
        >>>    client = WeChatClient('appid', 'secret')
        >>>    res = client.misc.short_url('http://www.qq.com')

        """
        return self._post("shorturl", data={"action": "long2short", "long_url": long_url})

    def get_wechat_ips(self):
        """
        获取微信服务器 IP 地址列表

        详情请参考：
        https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Get_the_WeChat_server_IP_address.html

        :return: IP 地址列表

        使用示例::

        >>>    from wechatpy import WeChatClient
        >>>
        >>>    client = WeChatClient('appid', 'secret')
        >>>    ips = client.misc.get_wechat_ips()

        """
        res = self._get("getcallbackip", result_processor=itemgetter("ip_list"))
        return res

    def check_network(self, action="all", operator="DEFAULT"):
        """
        网络检测

        详情请参阅
        https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Network_Detection.html

        :param action: 执行的检测动作，允许的值：dns（做域名解析）、ping（做ping检测）、all（dns和ping都做）
        :param operator: 指定平台从某个运营商进行检测，允许的值：CHINANET（电信出口）、UNICOM（联通出口）、CAP（腾讯自建出口）、DEFAULT（根据ip来选择运营商）
        :return: 返回的 JSON 数据包
        """
        return self._post("callback/check", data={"action": action, "check_operator": operator})
