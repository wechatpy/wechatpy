# -*- coding: utf-8 -*-
import time
import random
from datetime import datetime, timedelta

from wechatpy.utils import timezone
from wechatpy.pay.v3.api.base import BaseWeChatPayAPI
from wechatpy.utils import random_string, to_text


class WeChatPartnerOrder(BaseWeChatPayAPI):
    """
    服务商模式下的订单接口

    https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter7_2_4.shtml
    """

    def create(
        self,
        sub_mchid,
        sub_appid,
        description,
        out_trade_no,
        notify_url,
        amount,
        payer: dict = None,
        detail: dict = None,
        settle_info: dict = None,
        attach=None,
        time_expire=None,
        goods_tag=None,
        scene_info: dict = None,
        **kwargs,
    ):
        """
        统一下单接口

        :param sub_mchid: 二级商户号
        :param sub_appid: 二级商户在开放平台申请的应用appid。
        :param description: 商品描述
        :param out_trade_no: 商户订单号，默认自动生成
        :param notify_url: 接收微信支付异步通知回调地址
        :param amount: 订单金额信息
        :param detail: 可选，商品详情
        :param attach: 可选，附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据
        :param time_expire: 可选，订单失效时间，默认为订单生成时间后两小时
        :param goods_tag: 可选，商品标记，代金券或立减优惠功能的参数
        :param settle_info: 可选，结算信息
        :param scene_info: 可选，上报支付的场景信息
        :param payer: 小程序必填，支付者信息
        :param kwargs: 其他未列举在上述参数中的统一下单接口调用参数,例如电子发票入口开放标识receipt
        :return: 返回的结果数据
        """

        if time_expire is None:
            now = datetime.fromtimestamp(time.time(), tz=timezone("Asia/Shanghai"))
            hours_later = now + timedelta(hours=2)
            time_expire = hours_later
        else:
            time_expire = time_expire.astimezone(timezone("Asia/Shanghai"))
        if not out_trade_no:
            out_trade_no = f"{self.mch_id}{now.strftime('%Y%m%d%H%M%S')}{random.randint(1000, 10000)}"
        data = {
            "sp_appid": self.appid,
            "sp_mchid": self.mch_id,
            "sub_appid": sub_appid,
            "sub_mchid": sub_mchid,
            "description": description,
            "out_trade_no": out_trade_no,
            "time_expire": time_expire.isoformat("T"),
            "attach": attach or "",
            "notify_url": notify_url,
            "goods_tag": goods_tag or "",
            "settle_info": settle_info,
            "amount": amount,
            "payer": payer,
            "scene_info": scene_info,
        }
        # 字典类型，不传参不能有这个字段
        if detail:
            data["detail"] = detail
        data.update(kwargs)
        return self._post("pay/partner/transactions/jsapi", json=data)

    def query(self, sub_mchid, transaction_id):
        """
        微信支付订单号

        :param sub_mchid: 二级商户的商户号，由微信支付生成并下发。
        :param transaction_id: 微信的订单号，优先使用
        :return: 返回的结果数据
        """
        data = {
            "sp_mchid": self.mch_id,
            "sub_mchid": sub_mchid,
        }
        return self._post(f"pay/partner/transactions/id/{transaction_id}", json=data)

    def query_by_out_trade_no(self, sub_mchid, out_trade_no):
        """
        微信支付订单号

        :param sub_mchid: 二级商户的商户号，由微信支付生成并下发。
        :param out_trade_no: 商户系统内部订单号，只能是数字、大小写字母_-*且在同一个商户号下唯一，详见【商户订单号】。
        :return: 返回的结果数据
        """
        data = {
            "sp_mchid": self.mch_id,
            "sub_mchid": sub_mchid,
        }
        return self._post(f"pay/partner/transactions/out-trade-no/{out_trade_no}", json=data)

    def close(self, sub_mchid, out_trade_no):
        """
        关闭订单

        :param sub_mchid: 二级商户的商户号，由微信支付生成并下发。
        :param out_trade_no: 商户系统内部订单号，只能是数字、大小写字母_-*且在同一个商户号下唯一，详见【商户订单号】。
        :return: 返回的结果数据
        """
        data = {
            "sp_mchid": self.mch_id,
            "sub_mchid": sub_mchid,
        }
        return self._post(f"pay/partner/transactions/out-trade-no/{out_trade_no}/close", json=data)

    def get_api_params(self, sub_appid, prepay_id, timestamp=None, nonce_str=None):
        """
        获取支付参数

        :param sub_appid: 商户申请的小程序对应的appid，由微信支付生成，可在小程序后台查看。若下单时候传了sub_appid,须为sub_appid的值
        :param prepay_id: 统一下单接口返回的 prepay_id 参数值
        :param timestamp: 可选，时间戳，默认为当前时间戳
        :param nonce_str: 可选，随机字符串，默认自动生成
        :return: 签名
        """
        timestamp = timestamp or to_text(int(time.time()))
        nonce_str = nonce_str or random_string(32)
        package = f"prepay_id={prepay_id}"
        data = {
            "appId": sub_appid,
            "prepayid": prepay_id,
            "package": package,
            "signType": "RSA",
            "timeStamp": timestamp,
            "nonceStr": nonce_str or random_string(32),
        }
        sign = self.calculate_pay_params_signature_rsa(sub_appid, package, timestamp, nonce_str)
        data["paySign"] = sign
        return data
