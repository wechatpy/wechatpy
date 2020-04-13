# -*- coding: utf-8 -*-

import random
from datetime import datetime

from wechatpy.pay.utils import get_external_ip, rsa_encrypt
from wechatpy.pay.base import BaseWeChatPayAPI


class WeChatTransfer(BaseWeChatPayAPI):
    def transfer(
        self,
        user_id,
        amount,
        desc,
        client_ip=None,
        check_name="OPTION_CHECK",
        real_name=None,
        out_trade_no=None,
        device_info=None,
    ):
        """
        企业付款接口

        :param user_id: 接受收红包的用户在公众号下的 openid
        :param amount: 付款金额，单位分
        :param desc: 付款说明
        :param client_ip: 可选，调用接口机器的 IP 地址
        :param check_name: 可选，校验用户姓名选项，
                           NO_CHECK：不校验真实姓名,
                           FORCE_CHECK：强校验真实姓名（未实名认证的用户会校验失败，无法转账）,
                           OPTION_CHECK：针对已实名认证的用户才校验真实姓名（未实名认证用户不校验，可以转账成功）,
                           默认为 OPTION_CHECK
        :param real_name: 可选，收款用户真实姓名，
                          如果check_name设置为FORCE_CHECK或OPTION_CHECK，则必填用户真实姓名
        :param out_trade_no: 可选，商户订单号，需保持唯一性，默认自动生成
        :param device_info: 可选，微信支付分配的终端设备号
        :return: 返回的结果信息
        """
        if not out_trade_no:
            now = datetime.now()
            out_trade_no = f"{self.mch_id}{now.strftime('%Y%m%d%H%M%S')}{random.randint(1000, 10000)}"
        data = {
            "mch_appid": self.appid,
            "mchid": self.mch_id,
            "device_info": device_info,
            "partner_trade_no": out_trade_no,
            "openid": user_id,
            "check_name": check_name,
            "re_user_name": real_name,
            "amount": amount,
            "desc": desc,
            "spbill_create_ip": client_ip or get_external_ip(),
        }
        return self._post("mmpaymkttransfers/promotion/transfers", data=data)

    def query(self, out_trade_no):
        """
        企业付款查询接口

        :param out_trade_no: 商户调用企业付款API时使用的商户订单号
        :return: 返回的结果数据
        """
        data = {
            "appid": self.appid,
            "partner_trade_no": out_trade_no,
        }
        return self._post("mmpaymkttransfers/gettransferinfo", data=data)

    def transfer_bankcard(self, true_name, bank_card_no, bank_code, amount, desc=None, out_trade_no=None):
        """
        企业付款到银行卡接口

        :param true_name: 开户人名称
        :param bank_card_no: 银行卡号
        :param bank_code: 银行编号
        :param amount: 付款金额，单位分
        :param desc: 付款说明
        :param out_trade_no: 可选，商户订单号，需保持唯一性，默认自动生成
        :return: 返回的结果信息
        """
        if not out_trade_no:
            now = datetime.now()
            out_trade_no = f"{self.mch_id}{now.strftime('%Y%m%d%H%M%S')}{random.randint(1000, 10000)}"
        data = {
            "mch_id": self.mch_id,
            "partner_trade_no": out_trade_no,
            "amount": amount,
            "desc": desc,
            "enc_bank_no": self._rsa_encrypt(bank_card_no),
            "enc_true_name": self._rsa_encrypt(true_name),
            "bank_code": bank_code,
        }
        return self._post("mmpaysptrans/pay_bank", data=data)

    def query_bankcard(self, out_trade_no):
        """
        企业付款查询接口

        :param out_trade_no: 商户调用企业付款API时使用的商户订单号
        :return: 返回的结果数据
        """
        data = {
            "mch_id": self.mch_id,
            "partner_trade_no": out_trade_no,
        }
        return self._post("mmpaysptrans/query_bank", data=data)

    def get_rsa_public_key(self):
        data = {
            "mch_id": self.mch_id,
            "sign_type": "MD5",
        }
        return self._post("https://fraud.mch.weixin.qq.com/risk/getpublickey", data=data)

    def _rsa_encrypt(self, data):
        if not getattr(self, "_rsa_public_key", None):
            self._rsa_public_key = self.get_rsa_public_key()["pub_key"]
        return rsa_encrypt(data, self._rsa_public_key)
