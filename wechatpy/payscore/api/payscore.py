from .. base import BaseWeChatPayScoreAPI


class PayScore(BaseWeChatPayScoreAPI):

    def user_service_state(self, openid) -> bool:
        """
        查询用户授权状态API
        https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_8.shtml
        """
        data = dict(openid=openid)
        return self._get('v3/payscore/user-service-state', data=data)

    def create(self, out_order_no, service_introduction, risk_fund, notify_url, time_range={"start_time": "OnAccept"}, openid=None, **kwargs) -> bool:
        """
        创建支付分订单API
        https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_1.shtml
        """
        data = dict(
            out_order_no=out_order_no,
            service_introduction=service_introduction,
            risk_fund=risk_fund,
            notify_url=notify_url,
            time_range=time_range,
        )
        if openid:
            data.update(openid=openid)
        data.update(kwargs)
        return self._post('v3/payscore/serviceorder', data=data)

    def query(self, out_order_no=None, query_id=None):
        """
        查询支付分订单API
        https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_2.shtml
        """
        if out_order_no and not query_id:
            data = dict(out_order_no=out_order_no)
        elif not out_order_no and query_id:
            data = dict(query_id=query_id)
        else:
            raise ValueError('out_order_no 和 query_id 二选一')
        return self._get('v3/payscore/serviceorder', data=data)

    def complete(self, out_order_no, post_payments, total_amount, time_range=None, **kwargs):
        """
        完结支付分订单API
        https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_5.shtml
        """
        data = dict(
            post_payments=post_payments,
            total_amount=total_amount,
        )
        if time_range:
            data.update(time_range=time_range)
        data.update(kwargs)
        return self._post('v3/payscore/serviceorder/{out_order_no}/complete'.format(out_order_no=out_order_no), data=data)

    def cancel(self, out_order_no, reason):
        """
        取消支付分订单API
        https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_3.shtml
        """
        data = dict(
            reason=reason,
        )
        return self._post('v3/payscore/serviceorder/{out_order_no}/cancel'.format(out_order_no=out_order_no), data=data)

    def modify(self, out_order_no, post_payments, total_amount, reason, **kwargs):
        """
        修改订单金额API
        https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_4.shtml
        """
        data = dict(
            post_payments=post_payments,
            total_amount=total_amount,
            reason=reason,
        )
        data.update(kwargs)
        return self._post('v3/payscore/serviceorder/{out_order_no}/modify'.format(out_order_no=out_order_no), data=data)

    def pay(self, out_order_no, **kwargs):
        """
        商户发起催收扣款API
        https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_6.shtml
        """
        data = dict()
        data.update(kwargs)
        return self._post('v3/payscore/serviceorder/{out_order_no}/pay'.format(out_order_no=out_order_no), data=data)

    def sync(self, out_order_no, detail, _type='Order_Paid', **kwargs):
        """
        同步服务订单信息API
        https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_7.shtml
        """
        data = dict(
            detail=detail,
        )
        data.update({'type': _type})
        data.update(kwargs)
        return self._post('v3/payscore/serviceorder/{out_order_no}/sync'.format(out_order_no=out_order_no), data=data)
