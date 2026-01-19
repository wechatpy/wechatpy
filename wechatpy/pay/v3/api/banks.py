# -*- coding: utf-8 -*-


from wechatpy.pay.v3.api.base import BaseWeChatPayAPI


class WeChatBanks(BaseWeChatPayAPI):
    """
    银行组件

    https://pay.weixin.qq.com/wiki/doc/apiv3_partner/Offline/apis/chapter11_2_1.shtml
    """

    def search_banks_by_bank_account(self, account_number):
        """
        获取对私银行卡号开户银行

        :param account_number: 银行账号
        :return: 返回的结果数据
        """
        return self._get(
            "capital/capitallhh/banks/search-banks-by-bank-account", params={"account_number": account_number}
        )

    def query_personal_banking(self, limit, offset=0):
        """
        查询支持个人业务的银行

        :param limit: 本次请求最大查询条数
        :param offset: 本次查询偏移量
        :return: 返回的结果数据
        """
        return self._get("capital/capitallhh/banks/personal-banking", params={"offset": offset, "limit": limit})

    def query_corporate_banking(self, limit, offset=0):
        """
        查询支持对公业务的银行列表

        :param limit: 本次请求最大查询条数
        :param offset: 本次查询偏移量
        :return: 返回的结果数据
        """
        return self._get("capital/capitallhh/banks/corporate-banking", params={"offset": offset, "limit": limit})

    def query_provinces(self):
        """
        查询省份

        :return: 返回的结果数据
        """
        return self._get("capital/capitallhh/areas/provinces")

    def query_cities(self, province_code):
        """
        查询城市列表

        :param province_code: 省份编码
        :return: 返回的结果数据
        """
        return self._get(f"capital/capitallhh/areas/provinces/{province_code}/cities")

    def query_branches(self, bank_alias_code, city_code, limit, offset=0):
        """
        查询支行列表

        :param bank_alias_code: 银行别名编码
        :param city_code: 城市编码
        :param limit: 本次请求最大查询条数
        :param offset: 本次查询偏移量
        :return: 返回的结果数据
        """
        query = {"city_code": city_code, "offset": offset, "limit": limit}
        return self._get(f"capital/capitallhh/banks/{bank_alias_code}/branches", params=query)
