# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.client.api.base import BaseWeChatAPI


class WeChatTag(BaseWeChatAPI):

    def create(self, name):
        return self._post(
            'tag/create',
            data={
                'tagname': name
            }
        )

    def update(self, tag_id, name):
        return self._post(
            'tag/update',
            data={
                'tagid': tag_id,
                'tagname': name
            }
        )

    def delete(self, tag_id):
        return self._get(
            'tag/delete',
            params={
                'tagid': tag_id
            }
        )

    def get_users(self, tag_id):
        return self._get(
            'tag/get',
            params={
                'tagid': tag_id
            }
        )

    def add_users(self, tag_id, user_ids):
        return self._post(
            'tag/addtagusers',
            data={
                'tagid': tag_id,
                'userlist': user_ids
            }
        )

    def delete_users(self, tag_id, user_ids):
        return self._post(
            'tag/deltagusers',
            data={
                'tagid': tag_id,
                'userlist': user_ids
            }
        )

    def list(self):
        res = self._get('tag/list')
        return res['taglist']
