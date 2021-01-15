# -*- coding: utf-8 -*-


import base64
import urllib

from wechatpy.client.api.base import BaseWeChatAPI
from wechatpy.utils import to_binary, to_text


class WeChatDevice(BaseWeChatAPI):
    API_BASE_URL = "https://api.weixin.qq.com/device/"

    def send_message(self, device_type, device_id, user_id, content):
        """
        主动发送消息给设备
        详情请参考
        https://iot.weixin.qq.com/wiki/new/index.html?page=3-4-3

        :param device_type: 设备类型，目前为“公众账号原始ID”
        :param device_id: 设备ID
        :param user_id: 微信用户账号的openid
        :param content: 消息内容，BASE64编码
        :return: 返回的 JSON 数据包
        """
        content = to_text(base64.b64encode(to_binary(content)))
        return self._post(
            "transmsg",
            data={
                "device_type": device_type,
                "device_id": device_id,
                "open_id": user_id,
                "content": content,
            },
        )

    def send_status_message(self, device_type, device_id, user_id, msg_type, device_status):
        """
        第三方主动发送设备状态消息给微信终端
        详情请参考
        https://iot.weixin.qq.com/wiki/document-2_10.html

        :param device_type: 设备类型，目前为“公众账号原始ID”
        :param device_id: 设备ID
        :param user_id: 微信用户账号的openid
        :param msg_type: 消息类型：2--设备状态消息
        :param status: 设备状态：0--未连接， 1--已连接
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "transmsg",
            data={
                "device_type": device_type,
                "device_id": device_id,
                "open_id": user_id,
                "msg_type": msg_type,
                "device_status": device_status,
            },
        )

    def create_qrcode(self, device_ids):
        """
        获取设备二维码
        详情请参考
        https://iot.weixin.qq.com/wiki/new/index.html?page=3-4-4

        :param device_ids: 设备id的列表
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "create_qrcode",
            data={"device_num": len(device_ids), "device_id_list": device_ids},
        )

    def get_qrcode_url(self, ticket, data=None):
        """
        通过 ticket 换取二维码地址
        详情请参考
        https://iot.weixin.qq.com/wiki/new/index.html?page=3-4-4

        :param ticket: 二维码 ticket
        :param data: 额外数据
        :return: 二维码地址
        """
        url = f"https://we.qq.com/d/{ticket}"
        if data:
            if isinstance(data, (dict, tuple, list)):
                data = urllib.urlencode(data)
            data = to_text(base64.b64encode(to_binary(data)))
            url = f"{url}#{data}"
        return url

    def bind(self, ticket, device_id, user_id):
        """
        绑定设备
        详情请参考
        https://iot.weixin.qq.com/wiki/new/index.html?page=3-4-7

        :param ticket: 绑定操作合法性的凭证（由微信后台生成，第三方H5通过客户端jsapi获得）
        :param device_id: 设备id
        :param user_id: 用户对应的openid
        :return: 返回的 JSON 数据包
        """
        return self._post("bind", data={"ticket": ticket, "device_id": device_id, "openid": user_id})

    def unbind(self, ticket, device_id, user_id):
        """
        解绑设备
        详情请参考
        https://iot.weixin.qq.com/wiki/new/index.html?page=3-4-7

        :param ticket: 绑定操作合法性的凭证（由微信后台生成，第三方H5通过客户端jsapi获得）
        :param device_id: 设备id
        :param user_id: 用户对应的openid
        :return: 返回的 JSON 数据包
        """
        return self._post("unbind", data={"ticket": ticket, "device_id": device_id, "openid": user_id})

    def compel_bind(self, device_id, user_id):
        """
        强制绑定用户和设备
        详情请参考
        https://iot.weixin.qq.com/wiki/new/index.html?page=3-4-7

        :param device_id: 设备id
        :param user_id: 用户对应的openid
        :return: 返回的 JSON 数据包
        """
        return self._post("compel_bind", data={"device_id": device_id, "openid": user_id})

    force_bind = compel_bind

    def compel_unbind(self, device_id, user_id):
        """
        强制解绑用户和设备
        详情请参考
        https://iot.weixin.qq.com/wiki/new/index.html?page=3-4-7

        :param device_id: 设备id
        :param user_id: 用户对应的openid
        :return: 返回的 JSON 数据包
        """
        return self._post("compel_unbind", data={"device_id": device_id, "openid": user_id})

    force_unbind = compel_unbind

    def get_stat(self, device_id):
        """
        设备状态查询
        详情请参考
        https://iot.weixin.qq.com/wiki/new/index.html?page=3-4-8

        :param device_id: 设备id
        :return: 返回的 JSON 数据包
        """
        return self._get("get_stat", params={"device_id": device_id})

    def verify_qrcode(self, ticket):
        """
        验证二维码
        详情请参考
        https://iot.weixin.qq.com/wiki/new/index.html?page=3-4-9

        :param ticket: 设备二维码的ticket
        :return: 返回的 JSON 数据包
        """
        return self._post("verify_qrcode", data={"ticket": ticket})

    def get_user_id(self, device_type, device_id):
        """
        获取设备绑定openID
        详情请参考
        https://iot.weixin.qq.com/wiki/new/index.html?page=3-4-11

        :param device_type: 设备类型，目前为“公众账号原始ID”
        :param device_id: 设备id
        :return: 返回的 JSON 数据包
        """
        return self._get("get_openid", params={"device_type": device_type, "device_id": device_id})

    get_open_id = get_user_id

    def get_binded_devices(self, user_id):
        """
        通过openid获取用户在当前devicetype下绑定的deviceid列表
        详情请参考
        https://iot.weixin.qq.com/wiki/new/index.html?page=3-4-12

        :param user_id: 要查询的用户的openid
        :return: 返回的 JSON 数据包
        """
        return self._get("get_bind_device", params={"openid": user_id})

    get_bind_device = get_binded_devices

    def get_qrcode(self, product_id=1):
        """
        获取deviceid和二维码
        详情请参考
        https://iot.weixin.qq.com/wiki/new/index.html?page=3-4-4

        :param product_id: 设备的产品编号
        :return: 返回的 JSON 数据包
        """
        if product_id == "1" or product_id == 1:
            params = None
        else:
            params = {"product_id": product_id}

        return self._get("getqrcode", params=params)

    def authorize(self, devices, op_type=1):
        """
        设备授权
        详情请参考
        https://iot.weixin.qq.com/wiki/new/index.html?page=3-4-5

        :param devices: 设备信息的列表
        :param op_type: 请求操作的类型，限定取值为：0：设备授权 1：设备更新
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "authorize_device",
            data={
                "device_num": len(devices),
                "device_list": devices,
                "op_type": op_type,
            },
        )
