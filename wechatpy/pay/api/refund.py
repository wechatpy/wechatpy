# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.pay.base import BaseWeChatPayAPI


class WeChatRefund(BaseWeChatPayAPI):

    def apply(self, total_fee, refund_fee, out_refund_no, transaction_id=None,
              out_trade_no=None, fee_type='CNY', op_user_id=None,
              device_info=None):
        """
        申请退款

        :param total_fee: 订单总金额，单位为分
        :param refund_fee: 退款总金额，单位为分
        :param out_refund_no: 商户系统内部的退款单号，商户系统内部唯一，同一退款单号多次请求只退一笔
        :param transaction_id: 可选，微信订单号
        :param out_trade_no: 可选，商户系统内部的订单号，与 transaction_id 二选一
        :param fee_type: 可选，货币类型，符合ISO 4217标准的三位字母代码，默认人民币：CNY
        :param op_user_id: 可选，操作员帐号, 默认为商户号
        :param device_info: 可选，终端设备号
        :return: 返回的结果数据
        """
        data = {
            'appid': self.appid,
            'device_info': device_info,
            'transaction_id': transaction_id,
            'out_trade_no': out_trade_no,
            'out_refund_no': out_refund_no,
            'total_fee': total_fee,
            'refund_fee': refund_fee,
            'refund_fee_type': fee_type,
            'op_user_id': op_user_id,
            'device_info': device_info,
        }
        return self._post('secapi/pay/refund', data=data)

    def query(self, refund_id=None, out_refund_no=None, transaction_id=None,
              out_trade_no=None, device_info=None):
        """
        查询退款

        :param refund_id: 微信退款单号
        :param out_refund_no: 商户退款单号
        :param transaction_id: 微信订单号
        :param out_trade_no: 商户系统内部的订单号
        :param device_info: 可选，终端设备号
        :return: 返回的结果数据
        """
        data = {
            'appid': self.appid,
            'device_info': device_info,
            'transaction_id': transaction_id,
            'out_trade_no': out_trade_no,
            'out_refund_no': out_refund_no,
            'refund_id': refund_id,
        }
        return self._post('pay/refundquery', data=data)
