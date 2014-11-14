# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from wechatpy.exceptions import WeChatClientException
from .base import BaseWeChatAPI


class WeChatMenu(BaseWeChatAPI):

    def get(self):
        """
        查询自定义菜单。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单查询接口

        :return: 返回的 JSON 数据包
        """
        try:
            return self._get('menu/get')
        except WeChatClientException as e:
            if e.errcode == 46003:
                # menu not exist
                return None
            else:
                raise e

    def create(self, menu_data):
        """
        创建自定义菜单 ::

            client = WeChatClient("id", "secret")
            client.menu.create({
                "button":[
                    {
                        "type":"click",
                        "name":"今日歌曲",
                        "key":"V1001_TODAY_MUSIC"
                    },
                    {
                        "type":"click",
                        "name":"歌手简介",
                        "key":"V1001_TODAY_SINGER"
                    },
                    {
                        "name":"菜单",
                        "sub_button":[
                            {
                                "type":"view",
                                "name":"搜索",
                                "url":"http://www.soso.com/"
                            },
                            {
                                "type":"view",
                                "name":"视频",
                                "url":"http://v.qq.com/"
                            },
                            {
                                "type":"click",
                                "name":"赞一下我们",
                                "key":"V1001_GOOD"
                            }
                        ]
                    }
                ]
            })

        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单创建接口

        :param menu_data: Python 字典

        :return: 返回的 JSON 数据包
        """
        return self._post(
            'menu/create',
            data=menu_data
        )

    def delete(self):
        """
        删除自定义菜单。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单删除接口

        :return: 返回的 JSON 数据包
        """
        return self._get('menu/delete')

    def update(self, menu_data):
        """
        更新自定义菜单
        等同于先调用 :func:`delete_menu` 删除自定义菜单后，
        再调用 :func:`create_menu` 创建自定义菜单。
        """
        self.delete()
        return self.create(menu_data)
