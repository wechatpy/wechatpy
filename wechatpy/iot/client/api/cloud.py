# -*- coding: utf-8 -*-


from wechatpy.client.api.base import BaseWeChatAPI


class IotCloud(BaseWeChatAPI):
    def cloud_register_device(self, product_id, iot_device_list):
        """
        注册设备
        https://iot.weixin.qq.com/doc?page=3-2

        :param product_id: 产品id
        :param iot_device_list: 设备sn列表
        :return: 设备ilink_im_sdk_id列表
        """
        data = {"product_id": product_id, "iot_device_list": iot_device_list}
        result = self._post("cloud_register_device", json=data)
        return result
