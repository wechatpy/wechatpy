# -*- coding: utf-8 -*-


from wechatpy.pay.v3.api.base import BaseWeChatPayAPI


class WeChatEcommerce(BaseWeChatPayAPI):
    """
    电商收付通

    https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter7_1_1.shtml
    """

    def applyments(
        self,
        out_request_no,
        organization_type,
        contact_info,
        sales_scene_info,
        merchant_shortname,
        finance_institution=False,
        business_license_info=None,
        finance_institution_info=None,
        id_holder_type=None,
        id_doc_type=None,
        authorize_letter_copy=None,
        id_card_info=None,
        owner=True,
        ubo_info_list=None,
        account_info=None,
        settlement_info=None,
        qualifications=None,
        business_addition_pics=None,
        business_addition_desc=None,
    ):
        """
        二级商户进件申请
        https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter7_1_8.shtml

        :param out_request_no: 业务申请编号
        :param organization_type: 主体类型
        :param finance_institution: 是否金融机构 条件选填
        :param business_license_info: 营业执照信息 条件选填
        :param finance_institution_info: 金融机构许可证信息 条件选填
        :param id_holder_type: 证件持有人类型
        :param id_doc_type: 经营者/法人证件类型
        :param authorize_letter_copy: 法定代表人授权函 条件选填
        :param id_card_info: 经营者/法人身份证信息
        :param owner: 经营者/法人是否为受益人
        :param ubo_info_list: 最终受益人列表
        :param need_account_info: 是否填写结算账户信息
        :param account_info: 结算账户信息
        :param contact_info: 超级管理员信息
        :param sales_scene_info: 店铺信息
        :param settlement_info: 结算规则
        :param merchant_shortname: 商户简称
        :param qualifications: 特殊资质
        :param business_addition_pics: 补充材料
        :param business_addition_desc: 补充说明

        :return: 返回的结果数据
        """
        data = {
            "out_request_no": out_request_no,
            "organization_type": organization_type,
            "finance_institution": finance_institution,
            "business_license_info": business_license_info,
            "finance_institution_info": finance_institution_info,
            "id_holder_type": id_holder_type,
            "id_doc_type": id_doc_type,
            "authorize_letter_copy": authorize_letter_copy,
            "id_card_info": id_card_info,
            "owner": owner,
            "account_info": account_info,
            "contact_info": contact_info,
            "sales_scene_info": sales_scene_info,
            "settlement_info": settlement_info,
            "merchant_shortname": merchant_shortname,
            "qualifications": qualifications,
            "business_addition_pics": business_addition_pics,
            "business_addition_desc": business_addition_desc,
        }
        if ubo_info_list:
            data['ubo_info_list'] = ubo_info_list
        return self._post("ecommerce/applyments/", json=data)

    def applyments_query_by_applyment_id(self, applyment_id):
        """
        进件查询

        :param applyment_id: 申请单号
        :return: 返回的结果数据
        """
        return self._get(f"ecommerce/applyments/{applyment_id}")

    def applyments_query_by_out_request_no(self, out_request_no):
        """
        进件查询

        :param out_request_no: 服务商自定义的商户唯一编号
        :return: 返回的结果数据
        """
        return self._get(f"ecommerce/applyments/out-request-no/{out_request_no}")

    def modify_settlement(
        self,
        sub_mchid,
        account_type,
        account_bank,
        bank_address_code,
        account_number,
        bank_name=None,
        bank_branch_id=None,
    ):
        """
        修改结算账户

        :param sub_mchid: 特约商户/二级商户号
        :param account_type: 账户类型
        :param account_bank: 开户银行
        :param bank_address_code: 开户银行省市编码
        :param bank_name: 开户银行全称（含支行）
        :param bank_branch_id: 开户银行联行号
        :param account_number: 银行账号
        :return: 返回的结果数据
        """
        data = {
            "account_type": account_type,
            "account_bank": account_bank,
            "bank_address_code": bank_address_code,
            "bank_name": bank_name,
            "bank_branch_id": bank_branch_id,
            "account_number": account_number,
        }
        return self._post(f"apply4sub/sub_merchants/{sub_mchid}/modify-settlement", json=data)

    def settlement_query(self, sub_mchid):
        """
        查询结算账户

        :param sub_mchid: 特约商户/二级商户号
        :return: 返回的结果数据
        """
        return self._get(f"apply4sub/sub_merchants/{sub_mchid}/settlement")

    def refund_apply(
        self,
        sub_mchid,
        sub_appid,
        out_refund_no,
        amount,
        transaction_id=None,
        out_trade_no=None,
        reason=None,
        refund_account="REFUND_SOURCE_UNSETTLED_FUNDS",
        funds_account=None,
        notify_url=None,
    ):
        """
        申请退款

        :param sub_mchid: 微信支付分配二级商户的商户号。
        :param sub_appid: 退款总金额，单位为分
        :param out_refund_no: 商户系统内部的退款单号，商户系统内部唯一，同一退款单号多次请求只退一笔
        :param transaction_id: 可选，微信订单号
        :param out_trade_no: 可选，商户系统内部的订单号，与 transaction_id 二选一
        :param reason: 可选，退款原因
        :param amount: 订单金额信息
        :param refund_account: 可选，退款资金来源，仅针对老资金流商户使用，默认使用未结算资金退款
        :param notify_url: 可选，异步接收微信支付退款结果通知的回调地址
        :param funds_account: 资金账户
        :return: 返回的结果数据
        """
        data = {
            "sp_appid": self.appid,
            "sub_mchid": sub_mchid,
            "sub_appid": sub_appid,
            "transaction_id": transaction_id,
            "out_trade_no": out_trade_no,
            "out_refund_no": out_refund_no,
            "reason": reason,
            "amount": amount,
            "notify_url": notify_url,
            "refund_account": refund_account,
            "funds_account": funds_account,
        }
        return self._post("ecommerce/refunds/apply", json=data)

    def refund_query(
        self,
        sub_mchid,
        refund_id=None,
    ):
        """
        查询退款

        :param sub_mchid: 商户退款单号
        :param refund_id: 微信退款单号
        :return: 返回的结果数据
        """
        query = {
            "sub_mchid": sub_mchid,
        }
        return self._get(f"ecommerce/refunds/id/{refund_id}", params=query)

    def refund_query_by_out_refund_no(
        self,
        sub_mchid,
        out_refund_no,
    ):
        """
        查询退款
        :param sub_mchid: 商户退款单号
        :param out_refund_no: 微信退款单号
        :return: 返回的结果数据
        """
        query = {
            "sub_mchid": sub_mchid,
        }
        return self._get(f"ecommerce/refunds/out-refund-no/{out_refund_no}", params=query)

    def fund_balance_query(
        self,
        sub_mchid,
        account_type="BASIC",
    ):
        """
        查询二级商户账户实时余额

        :param sub_mchid: 商户退款单号
        :param account_type: 账户类型
        :return: 返回的结果数据
        """
        query = {
            "account_type": account_type,
        }
        return self._get(f"ecommerce/fund/balance/{sub_mchid}", params=query)

    def merchant_balance_query(
        self,
        account_type="BASIC",
    ):
        """
        查询电商平台账户实时余额

        :param account_type: 账户类型
        :return: 返回的结果数据
        """
        return self._get(f"merchant/fund/balance/{account_type}")

    def fund_withdraw(
        self,
        sub_mchid,
        out_request_no,
        amount,
        remark=None,
        bank_memo=None,
        account_type="BASIC",
    ):
        """
        二级商户预约提现

        :param sub_mchid: 电商平台二级商户号，由微信支付生成并下发
        :param out_request_no: 商户预约提现单号，由商户自定义生成
        :param amount: 提现金额
        :param remark: 提现备注
        :param bank_memo: 银行附言
        :param account_type: 账户类型
        :return: 返回的结果数据
        """

        data = {
            "sub_mchid": sub_mchid,
            "account_type": account_type,
            "out_request_no": out_request_no,
            "amount": amount,
            "bank_memo": bank_memo,
            "remark": remark,
        }
        return self._post("ecommerce/fund/withdraw", json=data)

    def fund_withdraw_query(
        self,
        sub_mchid,
        withdraw_id,
    ):
        """
        微信支付预约提现单号查询

        :param sub_mchid: 商户退款单号
        :param withdraw_id: 微信支付预约提现单号
        :return: 返回的结果数据
        """
        query = {
            "sub_mchid": sub_mchid,
        }
        return self._get(f"ecommerce/fund/withdraw/{withdraw_id}", params=query)

    def fund_withdraw_query_by_out_refund_no(
        self,
        sub_mchid,
        out_request_no,
    ):
        """
        查询退款
        :param sub_mchid: 商户退款单号
        :param out_request_no: 商户预约提现单号
        :return: 返回的结果数据
        """
        query = {
            "sub_mchid": sub_mchid,
        }
        return self._get(f"ecommerce/fund/withdraw/out-request-no/{out_request_no}", params=query)

    def profit_sharing(self, appid, sub_mchid, transaction_id, out_order_no, receivers, finish):
        """
        请求分账

        :param appid: 公众账号ID
        :param sub_mchid: 电商平台二级商户号，由微信支付生成并下发
        :param out_order_no: 商户分账单号
        :param transaction_id: 微信订单号
        :param finish: 是否分账完成
        :param receivers: 分账接收方列表
        :return: 返回的结果数据
        """

        data = {
            "appid": appid,
            "sub_mchid": sub_mchid,
            "transaction_id": transaction_id,
            "out_order_no": out_order_no,
            "receivers": receivers,
            "finish": finish,
        }
        return self._post("ecommerce/profitsharing/orders", json=data)

    def profit_sharing_query(self, sub_mchid, transaction_id, out_order_no):
        """
        分账查询

        :param sub_mchid: 电商平台二级商户号，由微信支付生成并下发
        :param out_order_no: 商户分账单号
        :param transaction_id: 微信订单号
        :return: 返回的结果数据
        """

        query = {
            "sub_mchid": sub_mchid,
            "transaction_id": transaction_id,
            "out_order_no": out_order_no,
        }
        return self._get("ecommerce/profitsharing/orders", params=query)

    def profit_sharing_return_orders(
        self, sub_mchid, out_return_no, return_mchid, amount, description, order_id=None, out_order_no=None
    ):
        """
        请求分账回退

        :param sub_mchid: 电商平台二级商户号，由微信支付生成并下发
        :param out_order_no: 商户分账单号
        :param out_return_no: 微信订单号
        :param order_id: 微信分账单号
        :param return_mchid: 回退商户号
        :param amount: 回退金额
        :param description: 回退描述
        :return: 返回的结果数据
        """

        data = {
            "sub_mchid": sub_mchid,
            "return_mchid": return_mchid,
            "order_id": order_id,
            "out_return_no": out_return_no,
            "out_order_no": out_order_no,
            "amount": amount,
            "description": description,
        }
        return self._post("ecommerce/profitsharing/returnorders", json=data)

    def profit_sharing_return_orders_query(
        self,
        sub_mchid,
        out_return_no,
        order_id=None,
        out_order_no=None,
    ):
        """
        查询分账回退

        :param sub_mchid: 电商平台二级商户号，由微信支付生成并下发
        :param order_id: 微信分账单号
        :param out_order_no: 商户分账单号
        :param out_return_no: 商户回退单号
        :return: 返回的结果数据
        """

        query = {
            "sub_mchid": sub_mchid,
            "order_id": order_id,
            "out_order_no": out_order_no,
            "out_return_no": out_return_no,
        }
        return self._get("ecommerce/profitsharing/returnorders", params=query)

    def profit_sharing_finish_orders(
        self,
        sub_mchid,
        transaction_id,
        out_order_no,
        description,
    ):
        """
        完结分账

        :param sub_mchid: 电商平台二级商户号，由微信支付生成并下发
        :param transaction_id: 微信订单号
        :param out_order_no: 商户分账单号
        :param description: 分账描述
        :return: 返回的结果数据
        """

        data = {
            "sub_mchid": sub_mchid,
            "transaction_id": transaction_id,
            "out_order_no": out_order_no,
            "description": description,
        }
        return self._post("ecommerce/profitsharing/finish-order", json=data)

    def profit_sharing_orders_amounts_query(self, transaction_id):
        """
        查询订单剩余待分金额

        :param transaction_id: 微信订单号
        :return: 返回的结果数据
        """

        return self._get(f"ecommerce/profitsharing/orders/{transaction_id}/amounts")
