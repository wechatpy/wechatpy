# -*- coding: utf-8 -*-

from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatScan(BaseWeChatAPI):
    API_BASE_URL = "https://api.weixin.qq.com/scan/"

    def get_merchant_info(self):
        """
        获取商户信息

        详情请参考
        http://mp.weixin.qq.com/wiki/6/c61604ff6890d386d6227945ad4a68d2.html

        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            info = client.scan.get_merchant_info()
        """
        return self._get("merchantinfo/get")

    def create_product(self, product_data):
        """
        创建商品

        详情请参考
        http://mp.weixin.qq.com/wiki/6/c61604ff6890d386d6227945ad4a68d2.html

        :return: 返回的 JSON 数据包
        """
        return self._post("product/create", data=product_data)

    def modify_product_status(self, standard, key, status):
        """
        提交审核/取消发布商品

        详情请参考
        http://mp.weixin.qq.com/wiki/15/1007691d0f1c10a0588c6517f12ed70f.html

        :param standard: 商品编码标准
        :param key: 商品编码内容
        :param status: 设置发布状态。on 为提交审核，off 为取消发布
        :return: 返回的 JSON 数据包
        """
        data = {
            "keystandard": standard,
            "keystr": key,
            "status": status,
        }
        return self._post("product/modstatus", data=data)

    def publish_product(self, standard, key):
        """
        提交审核商品 shortcut 接口

        等同于调用 ``modify_product_status(standard, key, 'on')``
        """
        return self.modify_product_status(standard, key, "on")

    def unpublish_product(self, standard, key):
        """
        取消发布商品 shortcut 接口

        等同于调用 ``modify_product_status(standard, key, 'off')``
        """
        return self.modify_product_status(standard, key, "off")

    def set_test_whitelist(self, userids=None, usernames=None):
        """
        设置测试人员白名单

        注意：每次设置均被视为一次重置，而非增量设置。openid、微信号合计最多设置10个。

        详情请参考
        http://mp.weixin.qq.com/wiki/15/1007691d0f1c10a0588c6517f12ed70f.html

        :param userids: 可选，测试人员的 openid 列表
        :param usernames: 可选，测试人员的微信号列表
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(openid=userids, username=usernames)
        return self._post("testwhitelist/set", data=data)

    def get_product(self, standard, key):
        """
        查询商品信息

        详情请参考
        http://mp.weixin.qq.com/wiki/15/7fa787701295b884410b5163e13313af.html

        :param standard: 商品编码标准
        :param key: 商品编码内容
        :return: 返回的 JSON 数据包
        """
        data = {
            "keystandard": standard,
            "keystr": key,
        }
        return self._post("product/get", data=data)

    def list_product(self, offset=0, limit=10, status=None, key=None):
        """
        批量查询商品信息

        详情请参考
        http://mp.weixin.qq.com/wiki/15/7fa787701295b884410b5163e13313af.html

        :param offset: 可选，批量查询的起始位置，从 0 开始，包含该起始位置
        :param limit: 可选，批量查询的数量，默认为 10
        :param status: 可选，支持按状态拉取。on为发布状态，off为未发布状态，
                       check为审核中状态，reject为审核未通过状态，all为所有状态
        :param key: 支持按部分编码内容拉取。填写该参数后，可将编码内容中包含所传参数的商品信息拉出
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(
            offset=offset,
            limit=limit,
            status=status,
            keystr=key,
        )
        return self._post("product/getlist", data=data)

    def update_product(self, product_data):
        """
        更新商品信息

        详情请参考
        http://mp.weixin.qq.com/wiki/15/7fa787701295b884410b5163e13313af.html

        :return: 返回的 JSON 数据包
        """
        return self._post("product/update", data=product_data)

    def clear_product(self, standard, key):
        """
        清除商品信息

        详情请参考
        http://mp.weixin.qq.com/wiki/15/7fa787701295b884410b5163e13313af.html

        :param standard: 商品编码标准
        :param key: 商品编码内容
        :return: 返回的 JSON 数据包
        """
        data = {
            "keystandard": standard,
            "keystr": key,
        }
        return self._post("product/clear", data=data)

    def check_ticket(self, ticket):
        """
        检查 wxticket 参数有效性

        详情请参考
        http://mp.weixin.qq.com/wiki/15/7fa787701295b884410b5163e13313af.html

        :param ticket: 请求 URL 中带上的 wxticket 参数
        :return: 返回的 JSON 数据包
        """
        return self._post("scanticket/check", data={"ticket": ticket})
