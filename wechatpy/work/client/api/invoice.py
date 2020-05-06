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

# 发票初始状态，未锁定
INVOICE_REIMBURSE_INIT = "INVOICE_REIMBURSE_INIT"
# 发票已锁定，无法重复提交报销
INVOICE_REIMBURSE_LOCK = "INVOICE_REIMBURSE_LOCK"
# 发票已核销，从用户卡包中移除
INVOICE_REIMBURSE_CLOSURE = "INVOICE_REIMBURSE_CLOSURE"

invoice_reimburse_status_set = {INVOICE_REIMBURSE_INIT, INVOICE_REIMBURSE_LOCK, INVOICE_REIMBURSE_CLOSURE}


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

    def update_status(self, card_id: str, encrypt_code: str, reimburse_status: str) -> dict:
        """更新发票状态

        参考：https://work.weixin.qq.com/api/doc/90000/90135/90285

        接口说明：报销企业和报销服务商可以通过该接口对某一张发票进行锁定、解锁和报销操作。

        **权限说明**：仅认证的企业微信账号有接口权限

        **发报销状态如下：**

        * **锁定**：电子发票进入了企业的报销流程时应该执行锁定操作，执行锁定操作后的电子
          发票仍然会存在于用户卡包内，但无法重复提交报销。
        * **解锁**：当电子发票由于各种原因，无法完成报销流程时，应执行解锁操作。执行锁定
          操作后的电子发票将恢复可以被提交的状态。
        * **报销**：当电子发票报销完成后，应该使用本接口执行报销操作。执行报销操作后的
          电子发票将从用户的卡包中移除，用户可以在卡包的消息中查看到电子发票的核销信息。
          注意，报销为不可逆操作，请开发者慎重调用。

        参数 ``reimburse_status`` 选项如下：

        * ``INVOICE_REIMBURSE_INIT`` 表示发票初始状态，未锁定；
        * ``INVOICE_REIMBURSE_LOCK`` 表示发票已锁定，无法重复提交报销;
        * ``INVOICE_REIMBURSE_CLOSURE`` 表示发票已核销，从用户卡包中移除。

        :param card_id: 发票id
        :param encrypt_code: 加密code
        :param reimburse_status: 发报销状态
        :return: 更新结果
        """
        self._validate_invoice_reimburse(reimburse_status)
        url = "card/invoice/reimburse/updateinvoicestatus"
        data = {"card_id": card_id, "encrypt_code": encrypt_code, "reimburse_status": reimburse_status}
        return self._post(url, data=data)

    def update_status_batch(self, openid: str, reimburse_status: str, invoice_list: List[Dict[str, str]]) -> dict:
        """批量更新发票状态

        参考：https://work.weixin.qq.com/api/doc/90000/90135/90286

        **接口说明**：发票平台可以通过该接口对某个成员的一批发票进行锁定、解锁和报销操作。
        注意，报销状态为不可逆状态，请开发者慎重调用。

        **权限说明**：仅认证的企业微信账号有接口权限

        **注意**：

        * 报销方须保证在报销、锁定、解锁后及时将状态同步至微信侧，保证用户发票可以正常使用
        * 批量更新发票状态接口为事务性操作，如果其中一张发票更新失败，列表中的其它发票状态
          更新也会无法执行，恢复到接口调用前的状态

        ------------------------

        参数 ``reimburse_status`` 选项如下：

        * ``INVOICE_REIMBURSE_INIT`` 表示发票初始状态，未锁定；
        * ``INVOICE_REIMBURSE_LOCK`` 表示发票已锁定，无法重复提交报销;
        * ``INVOICE_REIMBURSE_CLOSURE`` 表示发票已核销，从用户卡包中移除。

        :param openid: 用户openid，可用“userid与openid互换接口”获取
        :param reimburse_status: 发票报销状态
        :param invoice_list: 发票列表，必须全部属于同一个openid，示例：
            [{'card_id': 'id', 'encrypt_code': 'code'}...]
        :return: 更新结果
        """
        self._validate_invoice_reimburse(reimburse_status)
        if not invoice_list:
            raise ValueError("the invoice list cannot be empty")

        url = "card/invoice/reimburse/updatestatusbatch"
        data = {"openid": openid, "reimburse_status": reimburse_status, "invoice_list": invoice_list}
        return self._post(url, data=data)

    @staticmethod
    def _validate_invoice_reimburse(status: str) -> None:
        if not status:
            raise ValueError("the invoice reimburse_status cannot be empty")
        if status not in invoice_reimburse_status_set:
            raise ValueError(f"the invoice defer_status must be in the set of {invoice_reimburse_status_set!r}")
