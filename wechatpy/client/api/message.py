# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from .base import BaseWeChatAPI


class WeChatMessage(BaseWeChatAPI):

    def send_text(self, user_id, content):
        """
        发送文本消息
        详情请参考
        http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param content: 消息正文
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'text',
                'text': {'content': content}
            }
        )

    def send_image(self, user_id, media_id):
        """
        发送图片消息
        详情请参考
        http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 图片的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'image',
                'image': {
                    'media_id': media_id
                }
            }
        )

    def send_voice(self, user_id, media_id):
        """
        发送语音消息
        详情请参考
        http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 发送的语音的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'voice',
                'voice': {
                    'media_id': media_id
                }
            }
        )

    def send_video(self, user_id, media_id, title=None, description=None):
        """
        发送视频消息
        详情请参考
        http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 发送的视频的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        :return: 返回的 JSON 数据包
        """
        video_data = {
            'media_id': media_id,
        }
        if title:
            video_data['title'] = title
        if description:
            video_data['description'] = description

        return self._post(
            'message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'video',
                'video': video_data
            }
        )

    def send_music(self, user_id, url, hq_url, thumb_media_id,
                   title=None, description=None):
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

        return self._post(
            'message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'music',
                'music': music_data
            }
        )

    def send_articles(self, user_id, articles):
        """
        发送图文消息
        详情请参考
        http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param articles: 一个包含至多10个图文的数组
        :return: 返回的 JSON 数据包
        """
        articles_data = []
        for article in articles:
            articles_data.append({
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'picurl': article['image']
            })
        return self._post(
            'message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'news',
                'news': {
                    'articles': articles_data
                }
            }
        )

    def delete_mass(self, msg_id):
        """
        删除群发消息
        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param msg_id: 要删除的群发消息 ID
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'message/mass/delete',
            data={
                'msg_id': msg_id
            }
        )

    def _send_mass_message(self, group_or_users, msg_type, msg):
        data = {
            'msgtype': msg_type
        }
        if isinstance(group_or_users, (tuple, list)):
            # send by user ids
            data['touser'] = group_or_users
        else:
            data['filter'] = {'group_id': group_or_users}

        data.update(msg)
        return self._post(
            'message/mass/sendall',
            data=data
        )

    def send_mass_text(self, group_or_users, content):
        """
        群发文本消息
        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param content: 消息正文

        :return: 返回的 JSON 数据包
        """
        return self._send_mass_message(
            group_or_users,
            'text',
            {
                'text': {
                    'content': content
                }
            }
        )

    def send_mass_image(self, group_or_users, media_id):
        """
        群发图片消息
        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param media_id: 图片的媒体 ID。 可以通过 :func:`upload_media` 上传。

        :return: 返回的 JSON 数据包
        """
        return self._send_mass_message(
            group_or_users,
            'image',
            {
                'image': {
                    'media_id': media_id
                }
            }
        )

    def send_mass_voice(self, group_or_users, media_id):
        """
        群发语音消息
        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param media_id: 语音的媒体 ID。可以通过 :func:`upload_media` 上传。

        :return: 返回的 JSON 数据包
        """
        return self._send_mass_message(
            group_or_users,
            'voice',
            {
                'voice': {
                    'media_id': media_id
                }
            }
        )

    def send_mass_video(self, group_or_users, media_id,
                        title=None, description=None):
        """
        群发视频消息
        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param media_id: 视频的媒体 ID。可以通过 :func:`upload_video` 上传。
        :param title: 视频标题
        :param description: 视频描述

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
            'video',
            {
                'video': video_data
            }
        )

    def send_mass_article(self, group_or_users, media_id):
        """
        群发图文消息
        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param media_id: 图文的媒体 ID。可以通过 :func:`upload_articles` 上传。

        :return: 返回的 JSON 数据包
        """
        return self._send_mass_message(
            group_or_users,
            'mpnews',
            {
                'mpnews': {
                    'media_id': media_id
                }
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
