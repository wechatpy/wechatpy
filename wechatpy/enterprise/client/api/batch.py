# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI
from wechatpy.utils import to_text


class WeChatBatch(BaseWeChatAPI):

    def invite_user(self, url, token, encoding_aes_key, user_ids=None,
                    party_ids=None, tag_ids=None, invite_tips=None):
        """
        邀请成员关注
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=异步任务接口

        :param url: 企业应用接收企业号推送请求的访问协议和地址，支持http或https协议
        :param token: 用于生成签名
        :param encoding_aes_key: 用于消息体的加密，是AES密钥的Base64编码
        :param user_ids: 可选，成员ID列表，多个接收者用‘|’分隔，最多支持1000个。
        :param party_ids: 可选，部门ID列表，多个接收者用‘|’分隔，最多支持100个。
        :param tag_ids: 可选，标签ID列表，多个接收者用‘|’分隔。
        :param invite_tips: 可选，推送到微信上的提示语
        :return: 返回的 JSON 数据包
        """
        data = optionaldict()
        data['callback'] = {
            'url': url,
            'token': token,
            'encodingaeskey': encoding_aes_key
        }
        if isinstance(user_ids, (tuple, list)):
            user_ids = '|'.join(map(to_text, user_ids))
        if isinstance(party_ids, (tuple, list)):
            party_ids = '|'.join(map(to_text, party_ids))
        if isinstance(tag_ids, (tuple, list)):
            tag_ids = '|'.join(map(to_text, tag_ids))
        data['touser'] = user_ids
        data['toparty'] = party_ids
        data['totag'] = tag_ids
        data['invite_tips'] = invite_tips
        return self._post(
            'batch/inviteuser',
            data=data
        )

    def sync_user(self, url, token, encoding_aes_key, media_id):
        """
        增量更新成员
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=异步任务接口

        :param url: 企业应用接收企业号推送请求的访问协议和地址，支持http或https协议
        :param token: 用于生成签名
        :param encoding_aes_key: 用于消息体的加密，是AES密钥的Base64编码
        :param media_id: 上传的csv文件的media_id
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'batch/syncuser',
            data={
                'media_id': media_id,
                'callback': {
                    'url': url,
                    'token': token,
                    'encodingaeskey': encoding_aes_key
                }
            }
        )

    def replace_user(self, url, token, encoding_aes_key, media_id):
        """
        全量覆盖成员
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=异步任务接口

        :param url: 企业应用接收企业号推送请求的访问协议和地址，支持http或https协议
        :param token: 用于生成签名
        :param encoding_aes_key: 用于消息体的加密，是AES密钥的Base64编码
        :param media_id: 上传的csv文件的media_id
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'batch/replaceuser',
            data={
                'media_id': media_id,
                'callback': {
                    'url': url,
                    'token': token,
                    'encodingaeskey': encoding_aes_key
                }
            }
        )

    def replace_party(self, url, token, encoding_aes_key, media_id):
        """
        全量覆盖部门
        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=异步任务接口

        :param url: 企业应用接收企业号推送请求的访问协议和地址，支持http或https协议
        :param token: 用于生成签名
        :param encoding_aes_key: 用于消息体的加密，是AES密钥的Base64编码
        :param media_id: 上传的csv文件的media_id
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'batch/replaceparty',
            data={
                'media_id': media_id,
                'callback': {
                    'url': url,
                    'token': token,
                    'encodingaeskey': encoding_aes_key
                }
            }
        )

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
