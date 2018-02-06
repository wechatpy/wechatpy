# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import six

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatUser(BaseWeChatAPI):

    def get(self, user_id, lang='zh_CN'):
        """
        获取用户基本信息（包括UnionID机制）
        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140839

        :param user_id: 普通用户的标识，对当前公众号唯一
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            user = client.user.get('openid')

        """
        assert lang in ('zh_CN', 'zh_TW', 'en'), 'lang can only be one of \
            zh_CN, zh_TW, en language codes'
        return self._get(
            'user/info',
            params={
                'openid': user_id,
                'lang': lang
            }
        )

    def get_followers(self, first_user_id=None):
        """
        获取用户列表

        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140840

        :param first_user_id: 可选。第一个拉取的 OPENID，不填默认从头开始拉取
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            followers = client.user.get_followers()

        """
        params = {}
        if first_user_id:
            params['next_openid'] = first_user_id
        return self._get(
            'user/get',
            params=params
        )

    def update_remark(self, user_id, remark):
        """
        设置用户备注名

        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140838

        :param user_id: 用户标识
        :param remark: 新的备注名，长度必须小于30字符
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            client.user.update_remark('openid', 'Remark')

        """
        return self._post(
            'user/info/updateremark',
            data={
                'openid': user_id,
                'remark': remark
            }
        )

    def get_group_id(self, user_id):
        """
        获取用户所在分组 ID

        详情请参考
        http://mp.weixin.qq.com/wiki/0/56d992c605a97245eb7e617854b169fc.html

        :param user_id: 用户 ID
        :return: 用户所在分组 ID

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            group_id = client.user.get_group_id('openid')

        """
        res = self._post(
            'groups/getid',
            data={'openid': user_id},
            result_processor=lambda x: x['groupid']
        )
        return res

    def get_batch(self, user_list):
        """
        批量获取用户基本信息
        开发者可通过该接口来批量获取用户基本信息。最多支持一次拉取100条。

        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140839

        :param user_list: user_list，支持“使用示例”中两种输入格式
        :return: 用户信息的 list

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            users = client.user.get_batch(['openid1', 'openid2'])
            users = client.user.get_batch([
              {'openid': 'openid1', 'lang': 'zh-CN'},
              {'openid': 'openid2', 'lang': 'en'},
            ])

        """
        if all((isinstance(x, six.string_types) for x in user_list)):
            user_list = [{'openid': oid} for oid in user_list]
        res = self._post(
            'user/info/batchget',
            data={'user_list': user_list},
            result_processor=lambda x: x['user_info_list']
        )
        return res
