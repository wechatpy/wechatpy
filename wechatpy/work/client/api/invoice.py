#!/usr/bin/env python3
# -*- coding: utf8 -*-

# Date: 2020/05/06
# Author: huimingz
# Contact: huimingz12@outlook.com

"""
企业微信服务端电子发票API

企业微信文档：https://work.weixin.qq.com/api/doc/90000/90135/90283
"""

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatInvoice(BaseWeChatAPI):
    """企业微信电子发票API"""

    def get_info(self, card_id: str, encrypt_code: str) -> dict:
        """查询电子发票

        参考：https://work.weixin.qq.com/api/doc/90000/90135/90284

        接口说明：报销方在获得用户选择的电子发票标识参数后，可以通过该接口查询电子发票的
        结构化信息，并获取发票PDF文件。

        **权限说明**：仅认证的企业微信账号有接口权限

        返回结果参数说明请查看官方文档。

        :param card_id: 发票id
        :param encrypt_code: 加密code
        :return: 发票信息
        """
        url = "card/invoice/reimburse/getinvoiceinfo"
        data = {"card_id": card_id, "encrypt_code": encrypt_code}
        return self._post(url, data=data)
