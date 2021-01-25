# -*- coding: utf-8 -*-

from datetime import datetime, date

from wechatpy.pay.api.base import BaseWeChatPayAPI


class WeChatTools(BaseWeChatPayAPI):
    def short_url(self, long_url):
        """
        长链接转短链接

        :param long_url: 长链接
        :return: 返回的结果数据
        """
        data = {
            "appid": self.appid,
            "long_url": long_url,
        }
        return self._post("tools/shorturl", data=data)

    def download_bill(self, bill_date, bill_type="ALL", device_info=None):
        """
        下载对账单

        :param bill_date: 下载对账单的日期
        :param bill_type: 账单类型，ALL，返回当日所有订单信息，默认值
                          SUCCESS，返回当日成功支付的订单,
                          REFUND，返回当日退款订单,
                          REVOKED，已撤销的订单
        :param device_info: 微信支付分配的终端设备号，填写此字段，只下载该设备号的对账单
        :return: 返回的结果数据
        """
        if isinstance(bill_date, (datetime, date)):
            bill_date = bill_date.strftime("%Y%m%d")

        data = {
            "appid": self.appid,
            "bill_date": bill_date,
            "bill_type": bill_type,
            "device_info": device_info,
        }
        return self._post("pay/downloadbill", data=data)

    def download_fundflow(self, bill_date, account_type="Basic", tar_type=None):
        """
        下载资金账单
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_18&index=7

        :param bill_date: 下载对账单的日期
        :param account_type: 账单的资金来源账户
                             Basic  基本账户
                             Operation 运营账户
                             Fees 手续费账户
        :param tar_type: 非必传参数，固定值：GZIP，返回格式为.gzip的压缩包账单。
                         不传则默认为数据流形式。
        """
        if isinstance(bill_date, (datetime, date)):
            bill_date = bill_date.strftime("%Y%m%d")

        data = {
            "appid": self.appid,
            "bill_date": bill_date,
            "account_type": account_type,
            "sign_type": "HMAC-SHA256",
        }
        if tar_type is not None:
            data["tar_type"] = tar_type
        return self._post("pay/downloadfundflow", data=data)

    def auto_code_to_openid(self, auth_code):
        """
        授权码查询 openid 接口

        :param auth_code: 扫码支付授权码，设备读取用户微信中的条码或者二维码信息
        :return: 返回的结果数据
        """
        data = {
            "appid": self.appid,
            "auth_code": auth_code,
        }
        return self._post("tools/authcodetoopenid", data=data)
