# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.client.api.base import BaseWeChatAPI


class WeChatBatch(BaseWeChatAPI):

    def invite_user(self):
        pass

    def sync_user(self):
        pass

    def replace_user(self):
        pass

    def replace_party(self):
        pass

    def get_result(self, job_id):
        """
        获取异步任务结果
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=异步任务接口

        :param job_id: 异步任务id，最大长度为64字符
        :return: 返回的 JSON 数据包
        """
        return self._get(
            'batch/getresult',
            params={
                'jobid': job_id
            }
        )
