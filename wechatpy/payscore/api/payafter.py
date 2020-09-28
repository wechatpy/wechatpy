from .. base import BaseWeChatPayScoreAPI


class PayAfter(BaseWeChatPayScoreAPI):

    def permissions(self, authorization_code, **kwargs):
        """
        商户预授权API
        https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter5_1.shtml
        """
        data = dict(
            authorization_code=authorization_code,
        )
        data.update(kwargs)
        return self._post('v3/payscore/permissions', data=data)

    def authorization_record(self, authorization_code):
        """
        查询与用户授权记录（授权协议号）API
        https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter5_2.shtml
        """
        data = dict(
        )
        return self._get('v3/payscore/permissions/authorization-code/{authorization_code}'.format(authorization_code=authorization_code), data=data)

    def terminatei_authorization(self, authorization_code, reason):
        """
        解除用户授权关系（授权协议号）API
        https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter5_3.shtml
        """
        data = dict(
            reason=reason,
        )
        return self._post('v3/payscore/permissions/authorization-code/{authorization_code}/terminate'.format(authorization_code=authorization_code), data=data)

    def authorization_record_by_openid(self, openid):
        """
        查询与用户授权记录（openid）API
        https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter5_4.shtml
        """
        data = dict(
        )
        return self._get('v3/payscore/permissions/openid/{openid}'.format(openid=openid), data=data)

    def terminatei_authorization_by_openid(self, openid, reason):
        """
        解除用户授权关系（openid）API
        https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter5_5.shtml
        """
        data = dict(
            reason=reason,
        )
        return self._post('v3/payscore/permissions/openid/{openid}/terminate'.format(openid=openid), data=data)
