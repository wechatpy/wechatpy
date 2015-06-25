# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import random
from datetime import datetime

from wechatpy.pay.base import BaseWeChatPayAPI


class WeChatRedpack(BaseWeChatPayAPI):

    def send(self, user_id, total_amount, nick_name, act_name,
             wishing, remark, client_ip,
             send_name=None, total_num=1, min_value=None,
             max_value=None, mch_billno=None, logo_imgurl=None):
        """
        发送现金红包

        :param user_id: 接受收红包的用户在公众号下的 openid
        :param total_amount: 红包金额，单位分
        :param nick_name: 提供方名称
        :param act_name: 活动名称
        :param wishing: 红包祝福语
        :param remark: 备注
        :param client_ip: 调用接口的机器 IP 地址
        :param send_name: 可选，商户名称，默认和提供方名称相同
        :param total_num: 可选，红包发放总人数，默认为 1
        :param min_value: 可选，最小红包金额，单位分
        :param max_value: 可选，最大红包金额，单位分
        :param mch_billno: 可选，商户订单号，默认会自动生成
        :param logo_imgurl: 可选，商户 Logo 的 URL
        :return: 返回的结果数据字典
        """
        if not mch_billno:
            now = datetime.now()
            mch_billno = '{0}{1}{2}'.format(
                self._client.mch_id,
                now.strftime('%Y%m%d%H%M%S'),
                random.randint(1000, 10000)
            )
        data = {
            're_openid': user_id,
            'total_amount': total_amount,
            'nick_name': nick_name,
            'send_name': send_name or nick_name,
            'act_name': act_name,
            'wishing': wishing,
            'remark': remark,
            'client_ip': client_ip,
            'total_num': total_num,
            'min_value': min_value or total_amount,
            'max_value': max_value or total_amount,
            'mch_billno': mch_billno,
            'logo_imgurl': logo_imgurl,
        }
        return self._post('mmpaymkttransfers/sendredpack', data=data)

    def query(self, mch_billno, bill_type='MCHT'):
        """
        查询红包发放记录

        :param mch_billno: 商户订单号
        :param bill_type: 可选，订单类型，目前固定为 MCHT
        :return: 返回的红包发放记录信息
        """
        data = {
            'mch_billno': mch_billno,
            'bill_type': bill_type,
            'appid': self._client.appid,  # fuck Tencent
        }
        return self._post('mmpaymkttransfers/gethbinfo', data=data)
