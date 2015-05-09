# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMessage(BaseWeChatAPI):

    def _send_message(self, agent_id, user_ids, party_ids='',
                      tag_ids='', msg=None):
        msg = msg or {}
        if isinstance(user_ids, (tuple, list)):
            user_ids = '|'.join(user_ids)
        if isinstance(party_ids, (tuple, list)):
            party_ids = '|'.join(party_ids)
        if isinstance(tag_ids, (tuple, list)):
            tag_ids = '|'.join(tag_ids)

        data = {
            'touser': user_ids,
            'toparty': party_ids,
            'totag': tag_ids,
            'agentid': agent_id
        }
        data.update(msg)
        return self._post(
            'message/send',
            data=data
        )

    def send_text(self, agent_id, user_ids, content,
                  party_ids='', tag_ids='', safe=0):
        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'text',
                'text': {'content': content},
                'safe': safe
            }
        )

    def send_image(self, agent_id, user_ids, media_id,
                   party_ids='', tag_ids='', safe=0):
        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'image',
                'image': {
                    'media_id': media_id
                },
                'safe': safe
            }
        )

    def send_voice(self, agent_id, user_ids, media_id,
                   party_ids='', tag_ids='', safe=0):
        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'voice',
                'voice': {
                    'media_id': media_id
                },
                'safe': safe
            }
        )

    def send_video(self, agent_id, user_ids, media_id, title=None,
                   description=None, party_ids='', tag_ids='', safe=0):
        video_data = optionaldict()
        video_data['media_id'] = media_id
        video_data['title'] = title
        video_data['description'] = description

        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'video',
                'video': dict(video_data),
                'safe': safe
            }
        )

    def send_file(self, agent_id, user_ids, media_id,
                  party_ids='', tag_ids='', safe=0):
        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'file',
                'file': {
                    'media_id': media_id
                },
                'safe': safe
            }
        )

    def send_articles(self, agent_id, user_ids, articles,
                      party_ids='', tag_ids=''):
        articles_data = []
        for article in articles:
            articles_data.append({
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'picurl': article['image']
            })
        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'news',
                'news': {
                    'articles': articles_data
                }
            }
        )

    def send_mp_articles(self, agent_id, user_ids, articles,
                         party_ids='', tag_ids='', safe=0):
        articles_data = []
        for article in articles:
            articles_data.append({
                'thumb_media_id': article['thumb_media_id'],
                'author': article['author'],
                'content': article['content'],
                'content_source_url': article['content_source_url'],
                'digest': article['digest'],
                'show_cover_pic': article['show_cover_pic']
            })
        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'mpnews',
                'mpnews': {
                    'articles': articles_data
                },
                'safe': safe
            }
        )
