# -*- coding: utf-8 -*-


from wechatpy.client.api.base import BaseWeChatAPI


class IotDevice(BaseWeChatAPI):

    def get_device_ticket(self, ilink_im_sdk_id, user_openid):
        """
        获取设备ticket
        https://iot.weixin.qq.com/doc?page=3-3

        :param ilink_im_sdk_id: 设备sdk id
        :param user_openid: 用户openid
        :return: ilink_device_ticket
        """
        data = {
            "ilink_im_sdk_id": ilink_im_sdk_id,
            "user_openid": user_openid
        }
        result = self._post("get_device_ticket", json=data)
        return result

    def reset_device(self, ilink_im_sdk_id):
        """
        重置设备
        https://iot.weixin.qq.com/doc?page=3-5

        :param ilink_im_sdk_id: 设备sdk id
        :return:
        """
        data = {
            "ilink_im_sdk_id": ilink_im_sdk_id
        }
        result = self._post("reset_device", json=data)
        return result
