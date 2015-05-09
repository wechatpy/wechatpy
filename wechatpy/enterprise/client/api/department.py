# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatDepartment(BaseWeChatAPI):

    def create(self, name, parent_id=1, order=None, id=None):
        """
        创建部门
        详情请参考 http://qydev.weixin.qq.com/wiki/index.php?title=管理部门

        :param name: 部门名称，长度限制为 1~64 个字符
        :param parent_id: 父亲部门 id ,根部门 id 为 1
        :return: 返回的 JSON 数据包
        """
        department_data = optionaldict()
        department_data['name'] = name
        department_data['parentid'] = parent_id
        department_data['order'] = order
        department_data['id'] = id
        return self._post(
            'department/create',
            data=dict(department_data)
        )

    def update(self, id, name=None, parent_id=None, order=None):
        """
        更新部门
        详情请参考 http://qydev.weixin.qq.com/wiki/index.php?title=管理部门

        :param id: 部门 id
        :param name: 部门名称
        :param parent_id: 父亲部门 id
        :param order: 在父部门中的次序，从 1 开始，数字越大排序越靠后
        :return: 返回的 JSON 数据包
        """
        department_data = optionaldict()
        department_data['id'] = id
        department_data['name'] = name
        department_data['parentid'] = parent_id
        department_data['order'] = order
        return self._post(
            'department/update',
            data=dict(department_data)
        )

    def delete(self, id):
        """
        删除部门
        详情请参考 http://qydev.weixin.qq.com/wiki/index.php?title=管理部门

        :param id: 部门 id
        :return: 返回的 JSON 数据包
        """
        return self._get(
            'department/delete',
            params={
                'id': id
            }
        )

    def get(self):
        """
        获取部门列表
        详情请参考 http://qydev.weixin.qq.com/wiki/index.php?title=管理部门

        :return: 部门列表
        """
        res = self._get('department/list')
        return res['department']

    def get_users(self, id, status=0, fetch_child=0):
        """
        获取部门成员列表
        详情请参考 http://qydev.weixin.qq.com/wiki/index.php?title=管理成员

        :param id: 部门 id
        :param status: 0 获取全部员工，1 获取已关注成员列表，
                       2 获取禁用成员列表，4 获取未关注成员列表。可叠加
        :param fetch_child: 1/0：是否递归获取子部门下面的成员
        :return: 部门成员列表
        """
        fetch_child = 1 if fetch_child else 0
        res = self._get(
            'user/simplelist',
            params={
                'department_id': id,
                'status': status,
                'fetch_child': fetch_child
            }
        )
        return res['userlist']
