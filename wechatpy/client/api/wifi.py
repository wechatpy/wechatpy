# -*- coding: utf-8 -*-

from datetime import datetime, date

from optionaldict import optionaldict
from wechatpy.client.api.base import BaseWeChatAPI


class WeChatWiFi(BaseWeChatAPI):

    API_BASE_URL = "https://api.weixin.qq.com/bizwifi/"

    def list_shops(self, page_index=1, page_size=20):
        """
        获取门店列表

        详情请参考
        http://mp.weixin.qq.com/wiki/15/bcfb5d4578ea818b89913472cf2bbf8f.html

        :param page_index: 可选，分页下标，默认从1开始
        :param page_size: 可选，每页的个数，默认20个，最大20个
        :return: 返回的 JSON 数据包
        """
        res = self._post(
            "shop/list",
            data={
                "pageindex": page_index,
                "pagesize": page_size,
            },
            result_processor=lambda x: x["data"],
        )
        return res

    def get_shop(self, shop_id=0):
        """
        查询门店的WiFi信息
        http://mp.weixin.qq.com/wiki/15/bcfb5d4578ea818b89913472cf2bbf8f.html

        :param shop_id: 门店 ID
        :return: 返回的 JSON 数据包
        """
        res = self._post(
            "shop/get",
            data={
                "shop_id": shop_id,
            },
            result_processor=lambda x: x["data"],
        )
        return res

    def add_device(self, shop_id, ssid, password, bssid):
        """
        添加设备

        详情请参考
        http://mp.weixin.qq.com/wiki/10/6232005bdc497f7cf8e19d4e843c70d2.html

        :param shop_id: 门店 ID
        :param ssid: 无线网络设备的ssid。非认证公众号添加的ssid必需是“WX”开头(“WX”为大写字母)，
                     认证公众号和第三方平台无此限制；所有ssid均不能包含中文字符
        :param password: 无线网络设备的密码，大于8个字符，不能包含中文字符
        :param bssid: 无线网络设备无线mac地址，格式冒号分隔，字符长度17个，并且字母小写
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "device/add",
            data={
                "shop_id": shop_id,
                "ssid": ssid,
                "password": password,
                "bssid": bssid,
            },
        )

    def list_devices(self, shop_id=None, page_index=1, page_size=20):
        """
        查询设备

        详情请参考
        http://mp.weixin.qq.com/wiki/10/6232005bdc497f7cf8e19d4e843c70d2.html

        :param shop_id: 可选，门店 ID
        :param page_index: 可选，分页下标，默认从1开始
        :param page_size: 可选，每页的个数，默认20个，最大20个
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(shop_id=shop_id, pageindex=page_index, pagesize=page_size)
        res = self._post("device/list", data=data, result_processor=lambda x: x["data"])
        return res

    def delete_device(self, bssid):
        """
        删除设备

        详情请参考
        http://mp.weixin.qq.com/wiki/10/6232005bdc497f7cf8e19d4e843c70d2.html

        :param bssid: 无线网络设备无线mac地址，格式冒号分隔，字符长度17个，并且字母小写
        :return: 返回的 JSON 数据包
        """
        return self._post("device/delete", data={"bssid": bssid})

    def get_qrcode_url(self, shop_id, img_id):
        """
        获取物料二维码图片网址

        详情请参考
        http://mp.weixin.qq.com/wiki/7/fcd0378ef00617fc276be2b3baa80973.html

        :param shop_id: 门店 ID
        :param img_id: 物料样式编号：0-二维码，可用于自由设计宣传材料；
                       1-桌贴（二维码），100mm×100mm(宽×高)，可直接张贴
        :return: 二维码图片网址
        """
        res = self._post(
            "qrcode/get",
            data={
                "shop_id": shop_id,
                "img_id": img_id,
            },
            result_processor=lambda x: x["data"]["qrcode_url"],
        )
        return res

    def set_homepage(self, shop_id, template_id, url=None):
        """
        设置商家主页

        详情请参考
        http://mp.weixin.qq.com/wiki/6/2732f3cf83947e0e4971aa8797ee9d6a.html

        :param shop_id: 门店 ID
        :param template_id: 模板ID，0-默认模板，1-自定义url
        :param url: 自定义链接，当template_id为1时必填
        :return: 返回的 JSON 数据包
        """
        data = {
            "shop_id": shop_id,
            "template_id": template_id,
        }
        if url:
            data["struct"] = {"url": url}
        return self._post("homepage/set", data=data)

    def get_homepage(self, shop_id):
        """
        查询商家主页

        详情请参考
        http://mp.weixin.qq.com/wiki/6/2732f3cf83947e0e4971aa8797ee9d6a.html

        :param shop_id: 门店 ID
        :return: 返回的 JSON 数据包
        """
        res = self._post(
            "homepage/get",
            data={"shop_id": shop_id},
            result_processor=lambda x: x["data"],
        )
        return res

    def list_statistics(self, begin_date, end_date, shop_id=-1):
        """
        Wi-Fi数据统计

        详情请参考
        http://mp.weixin.qq.com/wiki/8/dfa2b756b66fca5d9b1211bc18812698.html

        :param begin_date: 起始日期时间，最长时间跨度为30天
        :param end_date: 结束日期时间戳，最长时间跨度为30天
        :param shop_id: 可选，门店 ID，按门店ID搜索，-1为总统计
        :return: 返回的 JSON 数据包
        """
        if isinstance(begin_date, (datetime, date)):
            begin_date = begin_date.strftime("%Y-%m-%d")
        if isinstance(end_date, (datetime, date)):
            end_date = end_date.strftime("%Y-%m-%d")
        res = self._post(
            "statistics/list",
            data={"begin_date": begin_date, "end_date": end_date, "shop_id": shop_id},
            result_processor=lambda x: x["data"],
        )
        return res
