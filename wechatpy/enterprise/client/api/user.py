# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.client.api.base import BaseWeChatAPI
from wechatpy.utils import NotNoneDict


class WeChatUser(BaseWeChatAPI):

    def create(self, user_id, name, department=None, position=None,
               mobile=None, gender=0, tel=None, email=None,
               weixin_id=None, extattr=None):
        """
        创建成员
        详情请参考 http://qydev.weixin.qq.com/wiki/index.php?title=管理成员
        """
        user_data = NotNoneDict()
        user_data['userid'] = user_id
        user_data['name'] = name
        user_data['gender'] = gender
        user_data['department'] = department
        user_data['position'] = position
        user_data['mobile'] = mobile
        user_data['tel'] = tel
        user_data['email'] = email
        user_data['weixinid'] = weixin_id
        user_data['extattr'] = extattr

        return self._post(
            'user/create',
            data=user_data
        )

    def update(self, user_id, name=None, department=None, position=None,
               mobile=None, gender=None, tel=None, email=None,
               weixin_id=None, enable=None, extattr=None):
        """
        更新成员
        详情请参考 http://qydev.weixin.qq.com/wiki/index.php?title=管理成员
        """
        user_data = NotNoneDict()
        user_data['userid'] = user_id
        user_data['name'] = name
        user_data['gender'] = gender
        user_data['department'] = department
        user_data['position'] = position
        user_data['mobile'] = mobile
        user_data['tel'] = tel
        user_data['email'] = email
        user_data['weixinid'] = weixin_id
        user_data['extattr'] = extattr
        user_data['enable'] = enable

        return self._post(
            'user/update',
            data=user_data
        )

    def delete(self, user_id):
        """
        删除成员
        详情请参考 http://qydev.weixin.qq.com/wiki/index.php?title=管理成员
        """
        return self._get(
            'user/delete',
            params={
                'userid': user_id
            }
        )

    def get(self, user_id):
        """
        获取成员
        详情请参考 http://qydev.weixin.qq.com/wiki/index.php?title=管理成员
        """
        return self._get(
            'user/get',
            params={
                'userid': user_id
            }
        )

    def verify(self, user_id):
        return self._get(
            'user/authsucc',
            params={
                'userid': user_id
            }
        )

    def get_info(self, agent_id, code):
        return self._get(
            'user/getuserinfo',
            params={
                'agentid': agent_id,
                'code': code
            }
        )
