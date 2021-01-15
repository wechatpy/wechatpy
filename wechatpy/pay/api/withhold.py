# -*- coding: utf-8 -*-

import time
import random
from datetime import datetime

from optionaldict import optionaldict

from wechatpy.utils import timezone
from wechatpy.pay.utils import get_external_ip, calculate_signature
from wechatpy.pay.base import BaseWeChatPayAPI


class WeChatWithhold(BaseWeChatPayAPI):
    def apply_signing(
        self,
        plan_id,
        contract_code,
        contract_display_account,
        notify_url,
        version="1.0",
        clientip=None,
        deviceid=None,
        mobile=None,
        email=None,
        qq=None,
        request_serial=None,
        openid=None,
        creid=None,
        outerid=None,
    ):
        """
        申请签约 api

        https://pay.weixin.qq.com/wiki/doc/api/pap.php?chapter=18_1&index=1

        :param plan_id: 模板id 协议模板id，设置路径见开发步骤。
        :param contract_code: 签约协议号 商户侧的签约协议号，由商户生成
        :param contract_display_account: 用户账户展示名称 签约用户的名称，用于页面展示，页面样例可见案例与规范
        :param notify_url: 回调通知url 用于接收签约成功消息的回调通知地址，以http或https开头。
        :param version: 版本号 固定值1.0
        :param request_serial: 可选 请求序列号 商户请求签约时的序列号，商户侧须唯一。序列号主要用于排序，不作为查询条件
        :param clientip: 可选 客户端 IP 点分IP格式(客户端IP)
        :param deviceid: 可选 设备ID android填imei的一次md5; ios填idfa的一次md5
        :param mobile: 可选 手机号 用户手机号
        :param email: 可选 邮箱地址 用户邮箱地址
        :param qq: 可选 QQ号 用户QQ号
        :param openid: 可选 微信open ID 用户微信open ID
        :param creid: 可选 身份证号 用户身份证号
        :param outerid: 可选 商户侧用户标识 用户在商户侧的标识
        :return: 返回的结果数据字典
        """
        timestamp = int(time.time())
        if request_serial is None:
            request_serial = int(time.time() * 1000)
        data = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "sub_mch_id": self.sub_mch_id,
            "plan_id": plan_id,
            "contract_code": contract_code,
            "request_serial": request_serial,
            "contract_display_account": contract_display_account,
            "notify_url": notify_url,
            "version": version,
            "timestamp": timestamp,
            "clientip": clientip,
            "deviceid": deviceid,
            "mobile": mobile,
            "email": email,
            "qq": qq,
            "openid": openid,
            "creid": creid,
            "outerid": outerid,
        }
        data = optionaldict(data)
        sign = calculate_signature(data, self._client.api_key)
        data["sign"] = sign
        return {
            "base_url": f"{self._client.API_BASE_URL}papay/entrustweb",
            "data": data,
        }

    def query_signing(
        self,
        contract_id=None,
        plan_id=None,
        contract_code=None,
        openid=None,
        version="1.0",
    ):
        """
        查询签约关系 api

        :param contract_id: 可选 委托代扣协议id 委托代扣签约成功后由微信返回的委托代扣协议id，选择contract_id查询，则此参数必填
        :param plan_id: 可选 模板id 商户在微信商户平台配置的代扣模板id，选择plan_id+contract_code查询，则此参数必填
        :param contract_code: 可选 签约协议号 商户请求签约时传入的签约协议号，商户侧须唯一。选择plan_id+contract_code查询，则此参数必填
        :param openid: 可选 openid 用户标识，必须保证与传入appid对应
        :param version: 版本号 固定值1.0
        :return: 返回的结果信息
        """
        if not contract_id and not (plan_id and contract_code) and not (plan_id and openid):
            raise ValueError("contract_id and (plan_id, contract_code) and (plan_id, openid) must be a choice.")
        data = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "contract_id": contract_id,
            "plan_id": plan_id,
            "contract_code": contract_code,
            "openid": openid,
            "version": version,
            "nonce_str": None,
        }
        return self._post("papay/querycontract", data=data)

    def apply_deduct(
        self,
        body,
        total_fee,
        contract_id,
        notify_url,
        out_trade_no=None,
        detail=None,
        attach=None,
        fee_type="CNY",
        goods_tag=None,
        clientip=None,
        deviceid=None,
        mobile=None,
        email=None,
        qq=None,
        openid=None,
        creid=None,
        outerid=None,
    ):
        """
        申请扣款 api

        :param body: 商品描述 商品或支付单简要描述
        :param out_trade_no: 可选 商户订单号 商户系统内部的订单号,32个字符内、可包含字母, 其他说明见商户订单号
        :param total_fee: 总金额 订单总金额，单位为分，只能为整数，详见支付金额
        :param contract_id: 委托代扣协议id 签约成功后，微信返回的委托代扣协议id
        :param notify_url: 回调通知url 接受扣款结果异步回调通知的url
        :param detail: 可选 商品详情 商品名称明细列表
        :param attach: 可选 附加数据 附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据
        :param fee_type: 可选 货币类型 符合ISO 4217标准的三位字母代码，默认人民币：CNY
        :param goods_tag: 可选 商品标记 商品标记，代金券或立减优惠功能的参数，说明详见代金券或立减优惠
        :param clientip: 可选 客户端 IP 点分IP格式(客户端IP)
        :param deviceid: 可选 设备ID android填imei的一次md5; ios填idfa的一次md5
        :param mobile: 可选 手机号 用户手机号
        :param email: 可选 邮箱地址 用户邮箱地址
        :param qq: 可选 QQ号 用户QQ号
        :param openid: 可选 微信open ID 用户微信open ID
        :param creid: 可选 身份证号 用户身份证号
        :param outerid: 可选 商户侧用户标识 用户在商户侧的标识
        :return: 返回的结果信息
        """
        trade_type = "PAP"  # 交易类型 交易类型PAP-微信委托代扣支付
        timestamp = int(time.time())  # 10位时间戳
        spbill_create_ip = get_external_ip()  # 终端IP 调用微信支付API的机器IP
        if not out_trade_no:
            now = datetime.fromtimestamp(time.time(), tz=timezone("Asia/Shanghai"))
            out_trade_no = f"{self.mch_id}{now.strftime('%Y%m%d%H%M%S')}{random.randint(1000, 10000)}"

        data = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "body": body,
            "out_trade_no": out_trade_no,
            "total_fee": total_fee,
            "trade_type": trade_type,
            "contract_id": contract_id,
            "notify_url": notify_url,
            "detail": detail,
            "attach": attach,
            "fee_type": fee_type,
            "goods_tag": goods_tag,
            "clientip": clientip,
            "deviceid": deviceid,
            "mobile": mobile,
            "email": email,
            "qq": qq,
            "openid": openid,
            "creid": creid,
            "outerid": outerid,
            "timestamp": timestamp,
            "spbill_create_ip": spbill_create_ip,
        }
        return self._post("pay/pappayapply", data=data)

    def query_order(self, transaction_id=None, out_trade_no=None):
        """
        查询订单 api

        :param transaction_id: 二选一 微信订单号 微信的订单号，优先使用
        :param out_trade_no: 二选一 商户订单号 商户系统内部的订单号，当没提供transaction_id时需要传这个。
        :return: 返回的结果信息
        """
        if not transaction_id and not out_trade_no:
            raise ValueError("transaction_id and out_trade_no must be a choice.")
        data = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "transaction_id": transaction_id,
            "out_trade_no": out_trade_no,
        }
        return self._post("pay/paporderquery", data=data)

    def apply_cancel_signing(
        self,
        contract_id=None,
        plan_id=None,
        contract_code=None,
        contract_termination_remark=None,
        version="1.0",
    ):
        """
        申请解约

        https://pay.weixin.qq.com/wiki/doc/api/pap.php?chapter=18_4&index=6

        :param contract_id: 合同ID
        :param plan_id: 模板ID
        :param contract_code: 合同号
        :param contract_termination_remark: 解约原因
        :param version: 版本号
        :return:
        """
        if not (contract_id or (plan_id and contract_code)):
            raise ValueError("contract_id and (plan_id, contract_code) must be a choice.")
        data = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "plan_id": plan_id,
            "contract_code": contract_code,
            "contract_id": contract_id,
            "contract_termination_remark": contract_termination_remark,
            "version": version,
            "nonce_str": None,
        }
        return self._post("papay/deletecontract", data=data)
