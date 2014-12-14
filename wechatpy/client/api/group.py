# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from wechatpy.utils import to_text
from .base import BaseWeChatAPI


class WeChatGroup(BaseWeChatAPI):

    def create(self, name):
        """
        创建分组
        详情请参考
        http://mp.weixin.qq.com/wiki/13/be5272dc4930300ba561d927aead2569.html

        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包

        """
        name = to_text(name)
        return self._post(
            'groups/create',
            data={'group': {'name': name}}
        )

    def get(self, user_id=None):
        """
        查询所有分组或查询用户所在分组
        详情请参考
        http://mp.weixin.qq.com/wiki/13/be5272dc4930300ba561d927aead2569.html

        :param user_id: 用户 ID，提供时查询该用户所在分组，否则查询所有分组
        :return: 返回的 JSON 数据包
        """
        if user_id is None:
            return self._get('groups/get')
        else:
            return self._post(
                'groups/getid',
                data={'openid': user_id}
            )

    def update(self, group_id, name):
        """
        修改分组名
        详情请参考
        http://mp.weixin.qq.com/wiki/13/be5272dc4930300ba561d927aead2569.html

        :param group_id: 分组id，由微信分配
        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包
        """
        name = to_text(name)
        return self._post(
            'groups/update',
            data={
                'group': {
                    'id': int(group_id),
                    'name': name
                }
            }
        )

    def move_user(self, user_id, group_id):
        """
        移动用户分组
        详情请参考
        http://mp.weixin.qq.com/wiki/13/be5272dc4930300ba561d927aead2569.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param group_id: 分组 ID
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'groups/members/update',
            data={
                'openid': user_id,
                'to_groupid': group_id
            }
        )
