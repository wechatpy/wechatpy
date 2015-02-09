# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import hashlib

from .base import BaseWeChatAPI


class WeChatCustomService(BaseWeChatAPI):

    def add_account(self, account, nickname, password):
        """
        添加客服账号
        详情请参考
        http://mp.weixin.qq.com/wiki/1/70a29afed17f56d537c833f89be979c9.html

        :param account: 完整客服账号，格式为：账号前缀@公众号微信号
        :param nickname: 客服昵称，最长6个汉字或12个英文字符
        :param password: 客服账号登录密码
        :return: 返回的 JSON 数据包
        """
        password = hashlib.md5(password).hexdigest()
        return self._post(
            'customservice/kfaccount/add',
            data={
                'kf_account': account,
                'nickname': nickname,
                'password': password
            }
        )

    def update_account(self, account, nickname, password):
        """
        更新客服账号
        详情请参考
        http://mp.weixin.qq.com/wiki/1/70a29afed17f56d537c833f89be979c9.html

        :param account: 完整客服账号，格式为：账号前缀@公众号微信号
        :param nickname: 客服昵称，最长6个汉字或12个英文字符
        :param password: 客服账号登录密码
        :return: 返回的 JSON 数据包
        """
        password = hashlib.md5(password).hexdigest()
        return self._post(
            'customservice/kfaccount/update',
            data={
                'kf_account': account,
                'nickname': nickname,
                'password': password
            }
        )

    def delete_account(self, account, nickname, password):
        """
        删除客服账号
        详情请参考
        http://mp.weixin.qq.com/wiki/1/70a29afed17f56d537c833f89be979c9.html

        :param account: 完整客服账号，格式为：账号前缀@公众号微信号
        :param nickname: 客服昵称，最长6个汉字或12个英文字符
        :param password: 客服账号登录密码
        :return: 返回的 JSON 数据包
        """
        password = hashlib.md5(password).hexdigest()
        return self._post(
            'customservice/kfaccount/del',
            data={
                'kf_account': account,
                'nickname': nickname,
                'password': password
            }
        )

    def get_accounts(self):
        """
        获取客服账号列表
        详情请参考
        http://mp.weixin.qq.com/wiki/1/70a29afed17f56d537c833f89be979c9.html

        :return: 客服账号列表
        """
        res = self._get('customservice/getkflist')
        return res['kf_list']

    def upload_headimg(self, account, media_file):
        """
        上传客服账号头像
        详情请参考
        http://mp.weixin.qq.com/wiki/1/70a29afed17f56d537c833f89be979c9.html

        :param account: 完整客服账号
        :param media_file: 要上传的头像文件，一个 File-Object
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'customservice/kfaccount/uploadheadimg',
            params={
                'kf_account': account
            },
            files={
                'media': media_file
            }
        )

    def get_online_accounts(self):
        """
        获取在线客服接待信息
        详情请参考
        http://mp.weixin.qq.com/wiki/9/6fff6f191ef92c126b043ada035cc935.html

        :return: 客服接待信息列表
        """
        res = self._get('customservice/getonlinekflist')
        return res['kf_online_list']
