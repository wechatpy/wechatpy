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

    def send_text_card(self, agent_id, user_ids, title, description, url, btntxt='详情',
                       party_ids='', tag_ids=''):
        """ 文本卡片消息
        https://work.weixin.qq.com/api/doc#10167/文本卡片消息

        请求示例：
        {
           "touser" : "UserID1|UserID2|UserID3",
           "toparty" : "PartyID1 | PartyID2",
           "totag" : "TagID1 | TagID2",
           "msgtype" : "textcard",
           "agentid" : 1,
           "textcard" : {
                "title" : "领奖通知",
                "description" : "<div class=\"gray\">2016年9月26日</div> <div class=\"normal\">恭喜你抽中iPhone 7一台，
                    领奖码：xxxx</div><div class=\"highlight\">请于2016年10月10日前联系行政同事领取</div>",
                "url" : "URL",
                "btntxt":"更多"
           }
        }

        特殊说明：
        卡片消息的展现形式非常灵活，支持使用br标签或者空格来进行换行处理，也支持使用div标签来使用不同的字体颜色，
        目前内置了3种文字颜色：灰色(gray)、高亮(highlight)、默认黑色(normal)，将其作为div标签的class属性即可，
        具体用法请参考上面的示例。

        :param agent_id: 必填，企业应用的id，整型。可在应用的设置页面查看。
        :param user_ids: 成员ID列表。
        :param title: 必填，成员ID列表（消息接收者，多个接收者用‘|’分隔，最多支持1000个）。
        :param description: 必填，描述，不超过512个字节，超过会自动截断
        :param url: 必填，点击后跳转的链接。
        :param btntxt: 按钮文字。 默认为“详情”， 不超过4个文字，超过自动截断。
        :param party_ids: 部门ID列表。
        :param tag_ids: 标签ID列表。
        """
        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'textcard',
                'textcard': {
                    'title': title,
                    'description': description,
                    'url': url,
                    'btntxt': btntxt,
                },
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
                'title': article['title'],
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
