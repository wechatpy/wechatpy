# -*- coding: utf-8 -*-

import random
from datetime import datetime

from wechatpy.pay.utils import get_external_ip
from wechatpy.pay.base import BaseWeChatPayAPI


class WeChatMicroPay(BaseWeChatPayAPI):
    def create(
        self,
        body,
        total_fee,
        auth_code,
        client_ip=None,
        out_trade_no=None,
        detail=None,
        attach=None,
        fee_type="CNY",
        goods_tag=None,
        device_info=None,
        limit_pay=None,
    ):
        """
        刷卡支付接口
        :param device_info: 可选，终端设备号(商户自定义，如门店编号)
        :param body: 商品描述
        :param detail: 可选，商品详情
        :param attach: 可选，附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据
        :param client_ip: 可选，APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP
        :param out_trade_no: 可选，商户订单号，默认自动生成
        :param total_fee: 总金额，单位分
        :param fee_type: 可选，符合ISO 4217标准的三位字母代码，默认人民币：CNY
        :param goods_tag: 可选，商品标记，代金券或立减优惠功能的参数
        :param limit_pay: 可选，指定支付方式，no_credit--指定不能使用信用卡支付
        :param auth_code: 授权码，扫码支付授权码，设备读取用户微信中的条码或者二维码信息
        :return: 返回的结果数据
        """
        now = datetime.now()
        if not out_trade_no:
            out_trade_no = f"{self.mch_id}{now.strftime('%Y%m%d%H%M%S')}{random.randint(1000, 10000)}"
        data = {
            "appid": self.appid,
            "device_info": device_info,
            "body": body,
            "detail": detail,
            "attach": attach,
            "out_trade_no": out_trade_no,
            "total_fee": total_fee,
            "fee_type": fee_type,
            "spbill_create_ip": client_ip or get_external_ip(),
            "goods_tag": goods_tag,
            "limit_pay": limit_pay,
            "auth_code": auth_code,
        }
        return self._post("pay/micropay", data=data)

    def query(self, transaction_id=None, out_trade_no=None):
        """
        查询订单

        :param transaction_id: 微信的订单号，优先使用
        :param out_trade_no: 商户系统内部的订单号，当没提供transaction_id时需要传这个。
        :return: 返回的结果数据
        """
        data = {
            "appid": self.appid,
            "transaction_id": transaction_id,
            "out_trade_no": out_trade_no,
        }
        return self._post("pay/orderquery", data=data)
