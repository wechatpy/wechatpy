# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatChat(BaseWeChatAPI):

    def create(self, chat_id, name, owner, user_list):
        """
        创建会话

        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=企业会话接口说明

        :param chat_id: 会话id。字符串类型，最长32个字符。只允许字符0-9及字母a-zA-Z,
                        如果值内容为64bit无符号整型：要求值范围在[1, 2^63)之间，
                        [2^63, 2^64)为系统分配会话id区间
        :param name: 会话标题
        :param owner: 管理员userid，必须是该会话userlist的成员之一
        :param user_list: 会话成员列表，成员用userid来标识。会话成员必须在3人或以上，1000人以下
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'chat/create',
            data={
                'chatid': chat_id,
                'name': name,
                'owner': owner,
                'userlist': user_list,
            }
        )

    def get(self, chat_id):
        """
        获取会话

        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=企业会话接口说明

        :param chat_id: 会话 ID
        :return: 会话信息
        """
        res = self._get('chat/get', params={'chatid': chat_id})
        return res['chat_info']

    def update(self, chat_id, op_user, name=None, owner=None,
               add_user_list=None, del_user_list=None):
        """
        修改会话

        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=企业会话接口说明

        :param chat_id: 会话 ID
        :param op_user: 操作人 userid
        :param name: 会话标题
        :param owner: 管理员userid，必须是该会话userlist的成员之一
        :param add_user_list: 会话新增成员列表，成员用userid来标识
        :param del_user_list: 会话退出成员列表，成员用userid来标识
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(
            chatid=chat_id,
            op_user=op_user,
            name=name,
            owner=owner,
            add_user_list=add_user_list,
            del_user_list=del_user_list,
        )
        return self._post('chat/update', data=data)

    def quit(self, chat_id, op_user):
        """
        退出会话

        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=企业会话接口说明

        :param chat_id: 会话 ID
        :param op_user: 操作人 userid
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'chat/quit',
            data={
                'chatid': chat_id,
                'op_user': op_user,
            }
        )

    def clear_notify(self, op_user, type, id):
        """
        清除会话未读状态

        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=企业会话接口说明

        :param op_user: 会话所有者的userid
        :param type: 会话类型：single|group，分别表示：单聊|群聊
        :param id: 会话值，为userid|chatid，分别表示：成员id|会话id
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'chat/clearnotify',
            data={
                'op_user': op_user,
                'chat': {
                    'type': type,
                    'id': id,
                }
            }
        )

    def set_mute(self, user_mute_list):
        """
        设置成员新消息免打扰

        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=企业会话接口说明

        :param user_mute_list: 成员新消息免打扰参数，数组，最大支持10000个成员
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'chat/setmute',
            data={'user_mute_list': user_mute_list}
        )

    def send_text(self, sender, receiver_type, receiver_id, content):
        """
        发送文本消息

        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=企业会话接口说明

        :param sender: 发送人
        :param receiver_type: 接收人类型：single|group，分别表示：单聊|群聊
        :param receiver_id: 接收人的值，为userid|chatid，分别表示：成员id|会话id
        :param content: 消息内容
        :return: 返回的 JSON 数据包
        """
        data = {
            'receiver': {
                'type': receiver_type,
                'id': receiver_id,
            },
            'sender': sender,
            'msgtype': 'text',
            'text': {
                'content': content,
            }
        }
        return self._post('chat/send', data=data)

    def send_single_text(self, sender, receiver, content):
        """
        发送单聊文本消息

        :param sender: 发送人
        :param receiver: 接收人成员 ID
        :param content: 消息内容
        :return: 返回的 JSON 数据包
        """
        return self.send_text(sender, 'single', receiver, content)

    def send_group_text(self, sender, receiver, content):
        """
        发送群聊文本消息

        :param sender: 发送人
        :param receiver: 会话 ID
        :param content: 消息内容
        :return: 返回的 JSON 数据包
        """
        return self.send_text(sender, 'group', receiver, content)

    def send_image(self, sender, receiver_type, receiver_id, media_id):
        """
        发送图片消息

        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=企业会话接口说明

        :param sender: 发送人
        :param receiver_type: 接收人类型：single|group，分别表示：单聊|群聊
        :param receiver_id: 接收人的值，为userid|chatid，分别表示：成员id|会话id
        :param media_id: 图片媒体文件id，可以调用上传素材文件接口获取
        :return: 返回的 JSON 数据包
        """
        data = {
            'receiver': {
                'type': receiver_type,
                'id': receiver_id,
            },
            'sender': sender,
            'msgtype': 'image',
            'image': {
                'media_id': media_id,
            }
        }
        return self._post('chat/send', data=data)

    def send_single_image(self, sender, receiver, media_id):
        """
        发送单聊图片消息

        :param sender: 发送人
        :param receiver: 接收人成员 ID
        :param media_id: 图片媒体文件id，可以调用上传素材文件接口获取
        :return: 返回的 JSON 数据包
        """
        return self.send_image(sender, 'single', receiver, media_id)

    def send_group_image(self, sender, receiver, media_id):
        """
        发送群聊图片消息

        :param sender: 发送人
        :param receiver: 会话 ID
        :param media_id: 图片媒体文件id，可以调用上传素材文件接口获取
        :return: 返回的 JSON 数据包
        """
        return self.send_image(sender, 'group', receiver, media_id)

    def send_file(self, sender, receiver_type, receiver_id, media_id):
        """
        发送文件消息

        详情请参考
        http://qydev.weixin.qq.com/wiki/index.php?title=企业会话接口说明

        :param sender: 发送人
        :param receiver_type: 接收人类型：single|group，分别表示：单聊|群聊
        :param receiver_id: 接收人的值，为userid|chatid，分别表示：成员id|会话id
        :param media_id: 文件id，可以调用上传素材文件接口获取, 文件须大于4字节
        :return: 返回的 JSON 数据包
        """
        data = {
            'receiver': {
                'type': receiver_type,
                'id': receiver_id,
            },
            'sender': sender,
            'msgtype': 'file',
            'file': {
                'media_id': media_id,
            }
        }
        return self._post('chat/send', data=data)

    def send_single_file(self, sender, receiver, media_id):
        """
        发送单聊文件消息

        :param sender: 发送人
        :param receiver: 接收人成员 ID
        :param media_id: 文件id，可以调用上传素材文件接口获取, 文件须大于4字节
        :return: 返回的 JSON 数据包
        """
        return self.send_file(sender, 'single', receiver, media_id)

    def send_group_file(self, sender, receiver, media_id):
        """
        发送群聊文件消息

        :param sender: 发送人
        :param receiver: 会话 ID
        :param media_id: 文件id，可以调用上传素材文件接口获取, 文件须大于4字节
        :return: 返回的 JSON 数据包
        """
        return self.send_file(sender, 'group', receiver, media_id)
