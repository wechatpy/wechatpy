# -*- coding: utf-8 -*-
import json
from wechatpy.pay.api.base import BaseWeChatPayAPI


class WechatProfitSharing(BaseWeChatPayAPI):
    def profit_sharing(
        self,
        transaction_id,
        out_order_no,
        receivers,
    ):
        """
        请求单次分账（需要双向证书）

        :param transaction_id: 微信支付订单号（待分账订单号）
        :param out_trade_no: 商户系统内部的分账单号，在商户系统内部唯一
        :param receivers: 分账接收方列表，不超过50个json对象，不能设置分账方作为分账接受方
        :return: 返回的结果数据
        """
        data = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "sign_type": "HMAC-SHA256",
            "transaction_id": transaction_id,
            "out_order_no": out_order_no,
            "receivers": json.dumps(receivers),
        }
        return self._post("secapi/pay/profitsharing", data=data)

    def multi_profit_sharing(
        self,
        transaction_id,
        out_order_no,
        receivers,
    ):
        """
        请求多次分账（需要双向证书）

        :param transaction_id: 微信支付订单号（待分账订单号）
        :param out_trade_no: 商户系统内部的分账单号，在商户系统内部唯一
        :param receivers: 分账接收方列表，不超过50个json对象，不能设置分账方作为分账接受方
        :return: 返回的结果数据
        """
        data = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "sign_type": "HMAC-SHA256",
            "transaction_id": transaction_id,
            "out_order_no": out_order_no,
            "receivers": json.dumps(receivers),
        }
        return self._post("secapi/pay/multiprofitsharing", data=data)

    def query(
        self,
        transaction_id,
        out_order_no,
    ):
        """
        查询分账结果

        :param transaction_id: 微信支付订单号
        :param out_trade_no: 商户分账单号
        :return: 返回的结果数据
        """
        data = {
            "mch_id": self.mch_id,
            "transaction_id": transaction_id,
            "out_order_no": out_order_no,
            "sign_type": "HMAC-SHA256",
        }
        return self._post("pay/profitsharingquery", data=data)

    def add_receiver(
        self,
        receiver,
    ):
        """
        添加分账接收方

        :param receiver: 分账接收方对象
        :return: 返回的结果数据
        """
        data = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "sign_type": "HMAC-SHA256",
            "receivers": json.dumps(receiver),
        }
        return self._post("pay/profitsharingaddreceiver", data=data)

    def remove_receiver(
        self,
        receiver,
    ):
        """
        删除分账接收方

        :param receiver: 分账接收方对象
        :return: 返回的结果数据
        """
        data = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "sign_type": "HMAC-SHA256",
            "receivers": json.dumps(receiver),
        }
        return self._post("pay/profitsharingremovereceiver", data=data)

    def finish(
        self,
        transaction_id,
        out_order_no,
        description,
    ):
        """
        完结分账（需要双向证书）

        :param transaction_id: 微信支付订单号
        :param out_order_no: 商户系统内部的分账单号，在商户系统内部唯一
        :param description: 分账完结的原因描述
        :return: 返回的结果数据
        """
        data = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "sign_type": "HMAC-SHA256",
            "transaction_id": transaction_id,
            "out_order_no": out_order_no,
            "description": description,
        }
        return self._post("secapi/pay/profitsharingfinish", data=data)

    def order_amount_query(
        self,
        transaction_id,
    ):
        """
        查询订单待分账金额

        :param transaction_id: 微信支付订单号
        :return: 返回的结果数据
        """
        data = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "sign_type": "HMAC-SHA256",
            "transaction_id": transaction_id,
        }
        return self._post("pay/profitsharingorderamountquery", data=data)

    def profit_sharing_return(
        self,
        order_id,
        out_order_no,
        out_return_no,
        return_account_type,
        return_account,
        return_amount,
        description,
    ):
        """
        分账回退（需要双向证书）

        :param order_id: 原发起分账请求时，微信返回的微信分账单号，与商户分账单号一一对应。与 out_trade_no 二选一
        :param out_order_no: 原发起分账请求时使用的商户系统内部的分账单号。与 order_id 二选一
        :param out_return_no: 商户系统内部的回退单号，商户系统内部唯一，同一回退单号多次请求等同一次
        :param return_account_type: 回退方类型
        :param return_account: 回退方账号
        :param return_amount: 需要从分账接收方回退的金额，单位为分，只能为整数，不能超过原始分账单分出给该接收方的金额
        :param description: 回退描述
        :return: 返回的结果数据
        """
        data = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "sign_type": "HMAC-SHA256",
            "order_id": order_id,
            "out_order_no": out_order_no,
            "out_return_no": out_return_no,
            "return_account_type": return_account_type,
            "return_account": return_account,
            "return_amount": return_amount,
            "description": description,
        }
        return self._post("secapi/pay/profitsharingreturn", data=data)

    def return_query(
        self,
        order_id,
        out_order_no,
        out_return_no,
    ):
        """
        回退结果查询

        :param order_id: 原发起分账请求时，微信返回的微信分账单号，与商户分账单号一一对应。与 out_trade_no 二选一
        :param out_order_no: 原发起分账请求时使用的商户系统内部的分账单号。与 order_id 二选一
        :param out_return_no: 商户系统内部的回退单号，商户系统内部唯一，同一回退单号多次请求等同一次
        :return: 返回的结果数据
        """
        data = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "sign_type": "HMAC-SHA256",
            "order_id": order_id,
            "out_order_no": out_order_no,
            "out_return_no": out_return_no,
        }
        return self._post("pay/profitsharingreturnquery", data=data)
