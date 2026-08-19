# -*- coding: utf-8 -*-


from wechatpy.client.api.base import BaseWeChatAPI


class IotDevice(BaseWeChatAPI):
    def get_device_ticket(self, ilink_im_sdk_id, user_openid, ticket_scene=0):
        """
        获取设备ticket
        https://iot.weixin.qq.com/doc?page=3-3

        :param ilink_im_sdk_id: 设备sdk id
        :param user_openid: 用户openid
        :param ticket_scene: 0:私人模式绑定场景. 4:公共模式绑定场景. 不填默认为0
        :return: ilink_device_ticket
        """
        data = {"ilink_im_sdk_id": ilink_im_sdk_id, "user_openid": user_openid, "ticket_scene": ticket_scene}
        result = self._post("get_device_ticket", json=data)
        return result

    def reset_device(self, ilink_im_sdk_id):
        """
        重置设备
        https://iot.weixin.qq.com/doc?page=3-5

        :param ilink_im_sdk_id: 设备sdk id
        :return:
        """
        data = {"ilink_im_sdk_id": ilink_im_sdk_id}
        result = self._post("reset_device", json=data)
        return result

    def reset_public_device(self, ilink_im_sdk_id):
        """
        重置公共设备
        https://iot.weixin.qq.com/doc?page=3-5

        :param ilink_im_sdk_id: 设备sdk id
        :return:
        """
        data = {"ilink_im_sdk_id": ilink_im_sdk_id}
        result = self._post("mmiot/reset_public_device", json=data)
        return result

    def get_device_qrcode(self, ilink_im_sdk_id, ticket_scene=0):
        """
        重置设备
        https://iot.weixin.qq.com/doc?page=3-5

        :param ilink_im_sdk_id: 设备sdk id
        :param ticket_scene: 0:私人模式绑定场景. 4:公共模式绑定场景. 不填默认为0
        :return:
        """
        data = {"ilink_im_sdk_id": ilink_im_sdk_id, "payload": {"ticket_scene": ticket_scene}}
        result = self._post("mmiot/get_device_qrcode", json=data)
        return result
