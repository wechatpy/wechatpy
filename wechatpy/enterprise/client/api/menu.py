# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.client.api.base import BaseWeChatAPI
from wechatpy.exceptions import WeChatClientException


class WeChatMenu(BaseWeChatAPI):

    def create(self, agent_id, menu_data):
        return self._post(
            'menu/create',
            params={
                'agentid': agent_id
            },
            data=menu_data
        )

    def get(self, agent_id):
        try:
            return self._get(
                'menu/get',
                params={
                    'agentid': agent_id
                }
            )
        except WeChatClientException as e:
            if e.errcode == 46003:
                # menu not exist
                return None
            else:
                raise e

    def delete(self, agent_id):
        return self._get(
            'menu/delete',
            params={
                'agentid': agent_id
            }
        )

    def update(self, agent_id, menu_data):
        self.delete(agent_id)
        return self.create(agent_id, menu_data)
