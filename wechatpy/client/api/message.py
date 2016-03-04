# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
import six

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMessage(BaseWeChatAPI):

    OPENID_RE = re.compile(r'^[\w\-]{28}$', re.I)

    def _send_custom_message(self, data, account=None):
        data = data or {}
        if account:
            data['customservice'] = {'kf_account': account}
        return self._post(
            'message/custom/send',
            data=data
        )

    def send_text(self, user_id, content, account=None):
        """
        发送文本消息

        详情请参考
        http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param content: 消息正文
        :param account: 可选，客服账号
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.message.send_text('openid', 'text')

        """
        data = {
            'touser': user_id,
            'msgtype': 'text',
            'text': {'content': content}
        }
        return self._send_custom_message(data, account=account)

    def send_image(self, user_id, media_id, account=None):
        """
        发送图片消息

        详情请参考
        http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 图片的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param account: 可选，客服账号
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.message.send_image('openid', 'media_id')

        """
        data = {
            'touser': user_id,
            'msgtype': 'image',
            'image': {
                'media_id': media_id
            }
        }
        return self._send_custom_message(data, account=account)

    def send_voice(self, user_id, media_id, account=None):
        """
        发送语音消息

        详情请参考
        http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 发送的语音的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param account: 可选，客服账号
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.message.send_voice('openid', 'media_id')

        """
        data = {
            'touser': user_id,
            'msgtype': 'voice',
            'voice': {
                'media_id': media_id
            }
        }
        return self._send_custom_message(data, account=account)

    def send_video(self, user_id, media_id, title=None,
                   description=None, account=None):
        """
        发送视频消息

        详情请参考
        http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 发送的视频的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        :param account: 可选，客服账号
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.message.send_video('openid', 'media_id', 'title', 'description')
        """
        video_data = {
            'media_id': media_id,
        }
        if title:
            video_data['title'] = title
        if description:
            video_data['description'] = description

        data = {
            'touser': user_id,
            'msgtype': 'video',
            'video': video_data
        }
        return self._send_custom_message(data, account=account)

    def send_music(self, user_id, url, hq_url, thumb_media_id,
                   title=None, description=None, account=None):
        """
        发送音乐消息

        详情请参考
        http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param url: 音乐链接
        :param hq_url: 高品质音乐链接，wifi环境优先使用该链接播放音乐
        :param thumb_media_id: 缩略图的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 音乐标题
        :param description: 音乐描述
        :param account: 可选，客服账号
        :return: 返回的 JSON 数据包
        """
        music_data = {
            'musicurl': url,
            'hqmusicurl': hq_url,
            'thumb_media_id': thumb_media_id
        }
        if title:
            music_data['title'] = title
        if description:
            music_data['description'] = description

        data = {
            'touser': user_id,
            'msgtype': 'music',
            'music': music_data
        }
        return self._send_custom_message(data, account=account)

    def send_articles(self, user_id, articles, account=None):
        """
        发送图文消息

        详情请参考
        http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param articles: 一个包含至多10个图文的数组, 或者微信图文消息素材 media_id
        :param account: 可选，客服账号
        :return: 返回的 JSON 数据包
        """
        if isinstance(articles, (tuple, list)):
            articles_data = []
            for article in articles:
                articles_data.append({
                    'title': article['title'],
                    'description': article['description'],
                    'url': article['url'],
                    'picurl': article.get('image', article.get('picurl')),
                })
            data = {
                'touser': user_id,
                'msgtype': 'news',
                'news': {
                    'articles': articles_data
                }
            }
        else:
            data = {
                'touser': user_id,
                'msgtype': 'mpnews',
                'mpnews': {
                    'media_id': articles,
                }
            }
        return self._send_custom_message(data, account=account)

    def send_card(self, user_id, card_id, card_ext, account=None):
        """
        发送卡券消息

        详情请参参考
        http://mp.weixin.qq.com/wiki/1/70a29afed17f56d537c833f89be979c9.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param card_id: 卡券 ID
        :param card_ext: 卡券扩展信息
        :param account: 可选，客服账号
        :return: 返回的 JSON 数据包
        """
        data = {
            'touser': user_id,
            'msgtype': 'wxcard',
            'wxcard': {
                'card_id': card_id,
                'card_ext': card_ext
            }
        }
        return self._send_custom_message(data, account=account)

    def delete_mass(self, msg_id):
        """
        删除群发消息

        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param msg_id: 要删除的群发消息 ID
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.message.delete_mass('message id')

        """
        return self._post(
            'message/mass/delete',
            data={
                'msg_id': msg_id
            }
        )

    def _send_mass_message(self, group_or_users, msg_type, msg,
                           is_to_all=False, preview=False):
        data = {
            'msgtype': msg_type
        }
        if not preview:
            if isinstance(group_or_users, (tuple, list)):
                # send by user ids
                data['touser'] = group_or_users
                endpoint = 'message/mass/send'
            else:
                # send by group id
                data['filter'] = {
                    'group_id': group_or_users,
                    'is_to_all': is_to_all,
                }
                endpoint = 'message/mass/sendall'
        else:
            if not isinstance(group_or_users, six.string_types):
                raise ValueError('group_or_users should be string types')
            # 预览接口
            if self.OPENID_RE.match(group_or_users):
                # 按照 openid 预览群发
                data['touser'] = group_or_users
            else:
                # 按照微信号预览群发
                data['towxname'] = group_or_users
            endpoint = 'message/mass/preview'

        data.update(msg)
        return self._post(
            endpoint,
            data=data
        )

    def send_mass_text(self, group_or_users, content,
                       is_to_all=False, preview=False):
        """
        群发文本消息

        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param content: 消息正文
        :param is_to_all: 用于设定是否向全部用户发送，值为true或false，选择true该消息群发给所有用户
                          选择false可根据group_id发送给指定群组的用户
        :param preview: 是否发送预览，此时 group_or_users 参数应为一个openid字符串

        :return: 返回的 JSON 数据包
        """
        return self._send_mass_message(
            group_or_users,
            'text',
            {
                'text': {
                    'content': content
                }
            },
            is_to_all,
            preview
        )

    def send_mass_image(self, group_or_users, media_id,
                        is_to_all=False, preview=False):
        """
        群发图片消息

        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param media_id: 图片的媒体 ID。 可以通过 :func:`upload_media` 上传。
        :param is_to_all: 用于设定是否向全部用户发送，值为true或false，选择true该消息群发给所有用户
                          选择false可根据group_id发送给指定群组的用户
        :param preview: 是否发送预览，此时 group_or_users 参数应为一个openid字符串

        :return: 返回的 JSON 数据包
        """
        return self._send_mass_message(
            group_or_users,
            'image',
            {
                'image': {
                    'media_id': media_id
                }
            },
            is_to_all,
            preview
        )

    def send_mass_voice(self, group_or_users, media_id,
                        is_to_all=False, preview=False):
        """
        群发语音消息

        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param media_id: 语音的媒体 ID。可以通过 :func:`upload_media` 上传。
        :param is_to_all: 用于设定是否向全部用户发送，值为true或false，选择true该消息群发给所有用户
                          选择false可根据group_id发送给指定群组的用户
        :param preview: 是否发送预览，此时 group_or_users 参数应为一个openid字符串

        :return: 返回的 JSON 数据包
        """
        return self._send_mass_message(
            group_or_users,
            'voice',
            {
                'voice': {
                    'media_id': media_id
                }
            },
            is_to_all,
            preview
        )

    def send_mass_video(self, group_or_users, media_id, title=None,
                        description=None, is_to_all=False, preview=False):
        """
        群发视频消息

        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param media_id: 视频的媒体 ID。可以通过 :func:`upload_video` 上传。
        :param title: 视频标题
        :param description: 视频描述
        :param is_to_all: 用于设定是否向全部用户发送，值为true或false，选择true该消息群发给所有用户
                          选择false可根据group_id发送给指定群组的用户
        :param preview: 是否发送预览，此时 group_or_users 参数应为一个openid字符串

        :return: 返回的 JSON 数据包
        """
        video_data = {
            'media_id': media_id
        }
        if title:
            video_data['title'] = title
        if description:
            video_data['description'] = description
        return self._send_mass_message(
            group_or_users,
            'mpvideo',
            {
                'mpvideo': video_data
            },
            is_to_all,
            preview
        )

    def send_mass_article(self, group_or_users, media_id,
                          is_to_all=False, preview=False):
        """
        群发图文消息

        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param media_id: 图文的媒体 ID。可以通过 :func:`upload_articles` 上传。
        :param is_to_all: 用于设定是否向全部用户发送，值为true或false，选择true该消息群发给所有用户
                          选择false可根据group_id发送给指定群组的用户
        :param preview: 是否发送预览，此时 group_or_users 参数应为一个openid字符串

        :return: 返回的 JSON 数据包
        """
        return self._send_mass_message(
            group_or_users,
            'mpnews',
            {
                'mpnews': {
                    'media_id': media_id
                }
            },
            is_to_all,
            preview
        )

    def get_mass(self, msg_id):
        """
        查询群发消息发送状态

        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param msg_id: 群发消息后返回的消息id
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            res = client.message.get_mass('mass message id')

        """
        return self._post(
            'message/mass/get',
            data={
                'msg_id': msg_id
            }
        )

    def send_template(self, user_id, template_id, url, top_color, data):
        """
        发送模板消息

        详情请参考
        http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param template_id: 模板 ID。在公众平台线上模板库中选用模板获得
        :param url: 链接地址
        :param top_color: 消息顶部颜色
        :param data: 模板消息数据

        :return: 返回的 JSON 数据包
        """
        return self._post(
            'message/template/send',
            data={
                'touser': user_id,
                'template_id': template_id,
                'url': url,
                'topcolor': top_color,
                'data': data
            }
        )

    def get_autoreply_info(self):
        """
        获取自动回复规则

        详情请参考
        http://mp.weixin.qq.com/wiki/7/7b5789bb1262fb866d01b4b40b0efecb.html

        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            info = client.message.get_autoreply_info()

        """
        return self._get('get_current_autoreply_info')

    def send_mass_card(self, group_or_users, card_id,
                       is_to_all=False, preview=False):
        """
        群发卡券消息

        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param card_id: 卡券 ID
        :param is_to_all: 用于设定是否向全部用户发送，值为true或false，选择true该消息群发给所有用户
                          选择false可根据group_id发送给指定群组的用户
        :param preview: 是否发送预览，此时 group_or_users 参数应为一个openid字符串

        :return: 返回的 JSON 数据包
        """
        return self._send_mass_message(
            group_or_users,
            'wxcard',
            {
                'wxcard': {
                    'card_id': card_id
                }
            },
            is_to_all,
            preview
        )
