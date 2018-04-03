# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import random
from datetime import datetime

from wechatpy.pay.base import BaseWeChatPayAPI
from wechatpy.pay.utils import rsa_encrypt


class WeChatTransferBankCard(BaseWeChatPayAPI):

    def transfer(self, true_name, bank_card_no, bank_code, amount, desc=None, out_trade_no=None):
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
            out_trade_no = '{0}{1}{2}'.format(
                self.mch_id,
                now.strftime('%Y%m%d%H%M%S'),
                random.randint(1000, 10000)
            )
        data = {
            'mch_id': self.mch_id,
            'partner_trade_no': out_trade_no,
            'amount': amount,
            'desc': desc,
            'enc_bank_no': self._rsa_encrypt(bank_card_no),
            'enc_true_name': self._rsa_encrypt(true_name),
            'bank_code': bank_code,
        }
        return self._post('mmpaysptrans/pay_bank', data=data)

    def query(self, out_trade_no):
        """
        企业付款查询接口

        :param out_trade_no: 商户调用企业付款API时使用的商户订单号
        :return: 返回的结果数据
        """
        data = {
            'mch_id': self.mch_id,
            'partner_trade_no': out_trade_no,
        }
        return self._post('mmpaysptrans/query_bank', data=data)

    def get_rsa_key(self):
        data = {
            'mch_id': self.mch_id,
            'sign_type': 'MD5',
        }
        return self._post('https://fraud.mch.weixin.qq.com/risk/getpublickey', data=data)

    def _rsa_encrypt(self, data):
        if not self.rsa_key:
            self._client.rsa_key = self.get_rsa_key()['pub_key']
        return rsa_encrypt(data, self.rsa_key)
