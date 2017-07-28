# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatInvoice(BaseWeChatAPI):
    API_BASE_URL = 'https://api.weixin.qq.com/card/invoice/'

    def get_url(self):
        """
        获取自身开票平台专用的授权链接
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496561481_1TyO7

        :return:该开票平台专用的授权链接
        """
        return self._post(
            'seturl',
            data={},
            result_processor=lambda x: x['invoice_url'],
        )

    def create_card(self, base_info, payee, invoice_type, detail=None):
        """
        创建发票卡券模板
        注意这里的对象和会员卡有类似之处，但是含义有不同。创建发票卡券模板是创建发票卡券的基础。
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496561481_1TyO7

        :param base_info:发票卡券模板基础信息
        :type base_info: dict
        :param payee: 收款方（开票方）全称，显示在发票详情内。建议一个收款方对应一个发票卡券模板
        :param invoice_type: 发票类型描述
        :param detail: 备注详情
        :return: 发票卡券模板的编号，用于后续该商户发票生成后，作为必填参数在调用插卡接口时传入
        """
        return self._post(
            'platform/createcard',
            data={
                'base_info': base_info,
                'payee': payee,
                'type': invoice_type,
                'detail': detail,
            },
            result_processor=lambda x: x['card_id'],
        )

    def get_user_title_url(
            self, user_fill, title=None, phone=None, tax_no=None, addr=None, bank_type=None, bank_no=None,
            out_title_id=None):
        """
        获取添加发票链接
        获取链接，发送给用户。用户同意以后，发票抬头信息将会录入到用户微信中
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496554912_vfWU0

        :param user_fill: 企业设置抬头为0，用户自己填写抬头为1
        :type user_fill: bool
        :param title: 抬头，当 user_fill 为 False 时必填
        :param phone: 联系方式
        :param tax_no: 税号
        :param addr: 地址
        :param bank_type: 银行类型
        :param bank_no: 银行号码
        :param out_title_id: 开票码
        :return: 添加发票的链接
        """
        if user_fill and title is None:
            raise ValueError('title is required when user_fill is False')
        return self._post(
            'biz/getusertitleurl',
            data={
                'user_fill': int(user_fill),
                'title': title,
                'phone': phone,
                'tax_no': tax_no,
                'addr': addr,
                'bank_type': bank_type,
                'bank_no': bank_no,
                'out_title_id': out_title_id,
            },
            result_processor=lambda x: x['url'],
        )

    def get_select_title_url(self, attach=None):
        """
        获取商户专属开票链接
        商户调用接口，获取链接。用户扫码，可以选择抬头发给商户。可以将链接转成二维码，立在收银台。
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496554912_vfWU0

        :param attach: 附加字段，用户提交发票时会发送给商户
        :return: 商户专属开票链接
        """
        return self._post(
            'biz/getselecttitleurl',
            data={
                'attach': attach,
            },
            result_processor=lambda x: x['url'],
        )

    def scan_title(self, scan_text):
        """
        根据扫描码，获取用户发票抬头
        商户扫用户“我的—个人信息—我的发票抬头”里面的抬头二维码后，通过调用本接口，可以获取用户抬头信息
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496554912_vfWU0

        :param scan_text: 扫码后获取的文本
        :return: 用户的发票抬头数据
        :rtype: dict
        """
        return self._post(
            'scantitle',
            data={
                'scan_text': scan_text,
            },
        )
