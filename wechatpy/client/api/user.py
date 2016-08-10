# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import six

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatUser(BaseWeChatAPI):

    def get(self, user_id, lang='zh_CN'):
        """
        获取用户基本信息
        详情请参考
        http://mp.weixin.qq.com/wiki/14/bb5031008f1494a59c6f71fa0f319c66.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
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
        获取关注者列表
        详情请参考
        http://mp.weixin.qq.com/wiki/3/17e6919a39c1c53555185907acf70093.html

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
        http://mp.weixin.qq.com/wiki/10/bf8f4e3074e1cf91eb6518b6d08d223e.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param remark: 备注名
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

        详情请参考
        http://mp.weixin.qq.com/wiki/14/bb5031008f1494a59c6f71fa0f319c66.html#.E6.89.B9.E9.87.8F.E8.8E.B7.E5.8F.96.E7.94.A8.E6.88.B7.E5.9F.BA.E6.9C.AC.E4.BF.A1.E6.81.AF

        :param user_id: user_list
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
