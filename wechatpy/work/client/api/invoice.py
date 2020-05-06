#!/usr/bin/env python3
# -*- coding: utf8 -*-

# Date: 2020/05/06
# Author: huimingz
# Contact: huimingz12@outlook.com

"""
企业微信服务端电子发票API

企业微信文档：https://work.weixin.qq.com/api/doc/90000/90135/90283
"""

from typing import Dict, List

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

    def get_info_batch(self, item_list: List[Dict[str, str]]) -> dict:
        """批量查询电子发票

        参考：https://work.weixin.qq.com/api/doc/90000/90135/90287

        报销方在获得用户选择的电子发票标识参数后，可以通过该接口批量查询电子发票的结构化信息。

        **权限说明**：
        仅认证的企业微信账号并且企业激活人数超过200的企业才有接口权限，如果认证的企业
        激活人数不超过200人请联系企业微信客服咨询。

        返回结果参数说明请查看官方文档。

        :param item_list: 发票列表，示例：
            [{'card_id': 'id', 'encrypt_code': 'code'}...]
        :return: 电子发票信息
        """
        if not item_list:
            raise ValueError("the item_list cannot be empty")

        url = "card/invoice/reimburse/getinvoiceinfobatch"
        data = {"item_list": item_list}
        return self._post(url, data=data)
