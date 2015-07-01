# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import random
from datetime import datetime

from wechatpy.pay.utils import get_external_ip
from wechatpy.pay.base import BaseWeChatPayAPI


class WeChatRedpack(BaseWeChatPayAPI):

    def send(self, user_id, total_amount, send_name, act_name,
             wishing, remark, total_num=1, client_ip=None,
             nick_name=None, min_value=None,
             max_value=None, out_trade_no=None, logo_imgurl=None):
        """
        发送现金红包

        :param user_id: 接收红包的用户在公众号下的 openid
        :param total_amount: 红包金额，单位分
        :param send_name: 商户名称
        :param nick_name: 可选，提供方名称，默认和商户名称相同
        :param act_name: 活动名称
        :param wishing: 红包祝福语
        :param remark: 备注
        :param client_ip: 可选，调用接口的机器 IP 地址
        :param total_num: 可选，红包发放总人数，默认为 1
        :param min_value: 可选，最小红包金额，单位分
        :param max_value: 可选，最大红包金额，单位分
        :param out_trade_no: 可选，商户订单号，默认会自动生成
        :param logo_imgurl: 可选，商户 Logo 的 URL
        :return: 返回的结果数据字典
        """
        if not out_trade_no:
            now = datetime.now()
            out_trade_no = '{0}{1}{2}'.format(
                self.mch_id,
                now.strftime('%Y%m%d%H%M%S'),
                random.randint(1000, 10000)
            )
        data = {
            'wxappid': self.appid,
            're_openid': user_id,
            'total_amount': total_amount,
            'nick_name': nick_name or send_name,
            'send_name': send_name,
            'act_name': act_name,
            'wishing': wishing,
            'remark': remark,
            'client_ip': client_ip or get_external_ip(),
            'total_num': total_num,
            'min_value': min_value or total_amount,
            'max_value': max_value or total_amount,
            'mch_billno': out_trade_no,
            'logo_imgurl': logo_imgurl,
        }
        return self._post('mmpaymkttransfers/sendredpack', data=data)

    def send_group(self, user_id, total_amount, send_name, act_name, wishing,
                   remark, total_num, client_ip=None, amt_type="ALL_RAND",
                   amt_list=None, out_trade_no=None,
                   logo_imgurl=None, watermark_imgurl=None,
                   banner_imgurl=None):
        """
        发送裂变红包

        :param user_id: 接收红包的用户在公众号下的 openid
        :param total_amount: 红包金额，单位分
        :param send_name: 商户名称
        :param act_name: 活动名称
        :param wishing: 红包祝福语
        :param remark: 备注
        :param total_num: 红包发放总人数
        :param client_ip: 可选，调用接口的机器 IP 地址
        :param amt_type: 可选，红包金额设置方式
                         ALL_RAND—全部随机,商户指定总金额和红包发放总人数，由微信支付随机计算出各红包金额
                         ALL_SPECIFIED—全部自定义
                         SEED_SPECIFIED—种子红包自定义，其他随机
        :param amt_list: 可选，各红包具体金额，自定义金额时必须设置，单位分
        :param out_trade_no: 可选，商户订单号，默认会自动生成
        :param logo_imgurl: 可选，商户 Logo 的 URL
        :param watermark_imgurl: 可选，背景水印图片 URL
        :param banner_imgurl: 红包详情页面的 banner 图片 URL
        :return: 返回的结果数据字典
        """
        if not out_trade_no:
            now = datetime.now()
            out_trade_no = '{0}{1}{2}'.format(
                self._client.mch_id,
                now.strftime('%Y%m%d%H%M%S'),
                random.randint(1000, 10000)
            )
        data = {
            'wxappid': self.appid,
            're_openid': user_id,
            'total_amount': total_amount,
            'send_name': send_name,
            'act_name': act_name,
            'wishing': wishing,
            'remark': remark,
            'total_num': total_num,
            'client_ip': client_ip or get_external_ip(),
            'amt_type': amt_type,
            'amt_list': amt_list,
            'mch_billno': out_trade_no,
            'logo_imgurl': logo_imgurl,
            'watermark_imgurl': watermark_imgurl,
            'banner_imgurl': banner_imgurl,
        }
        return self._post('mmpaymkttransfers/sendgroupredpack', data=data)

    def query(self, out_trade_no, bill_type='MCHT'):
        """
        查询红包发放记录

        :param out_trade_no: 商户订单号
        :param bill_type: 可选，订单类型，目前固定为 MCHT
        :return: 返回的红包发放记录信息
        """
        data = {
            'mch_billno': out_trade_no,
            'bill_type': bill_type,
            'appid': self.appid,
        }
        return self._post('mmpaymkttransfers/gethbinfo', data=data)
