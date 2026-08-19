# -*- coding: utf-8 -*-

from wechatpy.client.api.base import BaseWeChatAPI

from wechatpy.client.api.merchant.category import MerchantCategory
from wechatpy.client.api.merchant.stock import MerchantStock
from wechatpy.client.api.merchant.express import MerchantExpress
from wechatpy.client.api.merchant.group import MerchantGroup
from wechatpy.client.api.merchant.shelf import MerchantShelf
from wechatpy.client.api.merchant.order import MerchantOrder
from wechatpy.client.api.merchant.common import MerchantCommon


class WeChatMerchant(BaseWeChatAPI):
    API_BASE_URL = "https://api.weixin.qq.com/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # sub APIs
        self.category = MerchantCategory(self._client)
        self.stock = MerchantStock(self._client)
        self.express = MerchantExpress(self._client)
        self.group = MerchantGroup(self._client)
        self.shelf = MerchantShelf(self._client)
        self.order = MerchantOrder(self._client)
        self.common = MerchantCommon(self._client)

    def create(self, product_data):
        """增加商品"""
        return self._post("merchant/create", data=product_data)

    def delete(self, product_id):
        """删除商品"""
        return self._post("merchant/del", data={"product_id": product_id})

    def update(self, product_id, product_data):
        """修改商品"""
        product_data["product_id"] = product_id
        return self._post("merchant/update", data=product_data)

    def get(self, product_id):
        """查询商品"""
        return self._post("merchant/get", data={"product_id": product_id})

    def get_by_status(self, status):
        """获取指定状态的所有商品"""
        return self._post("merchant/getbystatus", data={"status": status})

    def update_product_status(self, product_id, status):
        """商品上下架"""
        return self._post(
            "merchant/modproductstatus",
            data={"product_id": product_id, "status": status},
        )

    def get_subcategories(self, cate_id):
        """
        获取指定分类的所有子分类

        :param cate_id: 大分类ID(根节点分类id为1)
        :return: 返回的 JSON 数据包
        """
        return self._post("merchant/category/getsub", data={"cate_id": cate_id})

    def get_category_sku(self, cate_id):
        """
        获取指定子分类的所有SKU

        :param cate_id: 商品子分类ID
        :return: 返回的 JSON 数据包
        """
        return self._post("merchant/category/getsku", data={"cate_id": cate_id})

    def get_category_property(self, cate_id):
        """
        获取指定分类的所有属性

        :param cate_id: 商品子分类ID
        :return: 返回的 JSON 数据包
        """
        return self._post("merchant/category/getproperty", data={"cate_id": cate_id})

    def add_stock(self, product_id, sku_info, quantity):
        """
        增加库存

        :param product_id: 商品ID
        :param sku_info: sku信息,格式"id1:vid1;id2:vid2",如商品为统一规格，则此处赋值为空字符串即可
        :param quantity: 增加的库存数量
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "merchant/stock/add",
            data={"product_id": product_id, "sku_info": sku_info, "quantity": quantity},
        )

    def reduce_stock(self, product_id, sku_info, quantity):
        """
        减少库存

        :param product_id: 商品ID
        :param sku_info: sku信息,格式"id1:vid1;id2:vid2",如商品为统一规格，则此处赋值为空字符串即可
        :param quantity: 减少的库存数量
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "merchant/stock/reduce",
            data={"product_id": product_id, "sku_info": sku_info, "quantity": quantity},
        )

    def add_express(self, product_data):
        """
        增加邮费模板

        :param product_data: 邮费信息
        :return: 返回的 JSON 数据包
        """
        return self._post("merchant/express/add", data=product_data)

    def del_express(self, template_id):
        """
        增加邮费模板

        :param template_id: 邮费模板ID
        :return: 返回的 JSON 数据包
        """
        return self._post("merchant/express/del", data={"template_id": template_id})

    def update_express(self, template_id, delivery_template):
        """
        增加邮费模板

        :param template_id: 邮费模板ID
        :param delivery_template: 邮费模板信息(字段说明详见增加邮费模板)
        :return: 返回的 JSON 数据包
        """
        delivery_template["template_id"] = template_id
        return self._post("merchant/express/update", data=delivery_template)

    def get_express(self, template_id):
        """
        获取指定ID的邮费模板

        :param template_id: 邮费模板ID
        :return: 返回的 JSON 数据包
        """
        return self._post("merchant/express/getbyid", data={"template_id": template_id})

    def get_all_express(self):
        """
        获取所有邮费模板

        :param template_id: 邮费模板ID
        :return: 返回的 JSON 数据包
        """
        return self._get("merchant/express/getall")

    def add_group(self, group_detail):
        """
        增加分组

        :param group_detail: 商品分组信息
        :return: 返回的 JSON 数据包
        """
        return self._post("merchant/group/add", data=group_detail)

    def del_group(self, group_id):
        """
        删除分组

        :param group_id: 商品分组ID
        :return: 返回的 JSON 数据包
        """
        return self._post("merchant/group/del", data={"group_id": group_id})

    def update_group_property(self, group_id, group_properties):
        """
        修改分组属性

        :param group_id: 商品分组ID
        :param group_properties: 商品分组属性
        :return: 返回的 JSON 数据包
        """
        group_properties["group_id"] = group_id
        return self._post("merchant/group/propertymod", data=group_properties)

    def update_group_product(self, group_id, product_data):
        """
        修改分组商品

        :param group_id: 商品分组ID
        :param product_data: 分组商品信息
        :return: 返回的 JSON 数据包
        """
        product_data["group_id"] = group_id
        return self._post("merchant/group/productmod", data=product_data)

    def get_all_groups(self):
        """
        获取所有分组

        :return: 返回的 JSON 数据包
        """
        return self._get("merchant/group/getall")

    def get_group(self, group_id):
        """
        根据分组ID获取分组信息

        :param group_id: 商品分组ID
        :return: 返回的 JSON 数据包
        """
        return self._post("merchant/group/getbyid", data={"group_id": group_id})

    def add_shelf(self, shelf_data):
        """
        增加货架

        :param shelf_data: 货架详情信息
        :return: 返回的 JSON 数据包
        """
        return self._post("merchant/shelf/add", data=shelf_data)

    def del_shelf(self, shelf_id):
        """
        删除货架

        :param shelf_id: 货架ID
        :return: 返回的 JSON 数据包
        """
        return self._post("merchant/shelf/del", data={"shelf_id": shelf_id})

    def update_shelf(self, shelf_id, shelf_data):
        """
        修改货架

        :param shelf_id: 货架ID
        :param shelf_data: 货架详情
        :return: 返回的 JSON 数据包
        """
        shelf_data["shelf_id"] = shelf_id
        return self._post("merchant/shelf/mod", data=shelf_data)

    def get_all_shelves(self):
        """
        获取所有货架

        :return: 返回的 JSON 数据包
        """
        return self._get("merchant/shelf/getall")

    def get_shelf(self, shelf_id):
        """
        根据货架ID获取货架信息

        :param shelf_id: 货架ID
        :return: 返回的 JSON 数据包
        """
        return self._post("merchant/shelf/getbyid", data={"shelf_id": shelf_id})

    def get_order(self, order_id):
        """
        根据订单ID获取订单详情

        :param order_id: 订单ID
        :return: 返回的 JSON 数据包
        """
        return self._post("merchant/order/getbyid", data={"order_id": order_id})

    def query_order(self, status=None, begintime=None, endtime=None):
        """
        根据订单状态/创建时间获取订单详情

        :param status: 订单状态(不带该字段-全部状态, 2-待发货, 3-已发货, 5-已完成, 8-维权中, )
        :param begintime: 订单创建时间起始时间(不带该字段则不按照时间做筛选)
        :param endtime: 订单创建时间终止时间(不带该字段则不按照时间做筛选)
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "merchant/order/getbyfilter",
            data={"status": status, "begintime": begintime, "endtime": endtime},
        )

    def set_delivery(self, order_id, delivery_data):
        """
        修改货架

        :param order_id: 订单ID
        :param delivery_data: 商品物流信息
        :return: 返回的 JSON 数据包
        """
        delivery_data["order_id"] = order_id
        return self._post("merchant/shelf/setdeliverymod", data=delivery_data)

    def upload_image(self, media_file):
        """
        上传图片

        :param media_file: 要上传的文件，一个 File-object
        :return: 上传成功时返回图片 URL
        """
        res = self._post(
            url="merchant/common/upload_img",
            files={"media": media_file},
            result_processor=lambda x: x["url"],
        )
        return res
