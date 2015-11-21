# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatTemplate(BaseWeChatAPI):

    def set_industry(self, industry_id1, industry_id2):
        """
        设置所属行业
        详情请参考
        http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html

        :param industry_id1: 公众号模板消息所属行业编号
        :param industry_id2: 公众号模板消息所属行业编号
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'template/api_set_industry',
            data={
                'industry_id1': industry_id1,
                'industry_id2': industry_id2
            }
        )

    def get(self, template_id_short):
        """
        获得模板ID
        详情请参考
        http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html

        :param template_id_short: 模板库中模板的编号，有“TM**”和“OPENTMTM**”等形式
        :return: 模板 ID
        """
        res = self._post(
            'template/api_add_template',
            data={
                'template_id_short': template_id_short
            },
            result_processor=lambda x: x['template_id']
        )
        return res

    add = get
