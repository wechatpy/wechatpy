# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import time
import unittest

from wechatpy.replies import TextReply


class ReplyTestCase(unittest.TestCase):

    def test_reply_init_ok(self):
        timestamp = int(time.time())
        reply = TextReply(source='user1', target='user2')

        self.assertEqual('user1', reply.source)
        self.assertEqual('user2', reply.target)
        self.assertTrue(timestamp <= reply.time)

    def test_reply_init_fail(self):
        self.assertRaises(AttributeError, TextReply, go_to_hell='hehe')

    def test_reply_render(self):
        timestamp = int(time.time())
        reply = TextReply(
            source='user1',
            target='user2',
            time=timestamp,
            content='test'
        )
        r = reply.render()

        self.assertTrue(r.startswith('<xml>\n'))
        self.assertTrue(r.endswith('\n</xml>'))
        self.assertTrue('<ToUserName><![CDATA[user2]]></ToUserName>' in r)
        self.assertTrue('<FromUserName><![CDATA[user1]]></FromUserName>' in r)
        self.assertTrue('<MsgType><![CDATA[text]]></MsgType>' in r)
        self.assertTrue('<Content><![CDATA[test]]></Content>' in r)
        create_time = '<CreateTime>{time}</CreateTime>'.format(time=timestamp)
        self.assertTrue(create_time in r)

    def test_image_reply_properties(self):
        from wechatpy.replies import ImageReply

        reply = ImageReply(image='7890')

        self.assertEqual('7890', reply.image)
        self.assertEqual('7890', reply.media_id)

        reply.media_id = '123456'
        self.assertEqual('123456', reply.image)
        self.assertEqual('123456', reply.media_id)

    def test_voice_reply_properties(self):
        from wechatpy.replies import VoiceReply

        reply = VoiceReply(voice='7890')

        self.assertEqual('7890', reply.voice)
        self.assertEqual('7890', reply.media_id)

        reply.media_id = '123456'
        self.assertEqual('123456', reply.voice)
        self.assertEqual('123456', reply.media_id)

    def test_video_reply_properties(self):
        from wechatpy.replies import VideoReply

        reply = VideoReply()
        reply.media_id = '123456'
        reply.title = 'test'

        self.assertEqual('123456', reply.media_id)
        self.assertEqual('test', reply.title)

    def test_music_reply_properties(self):
        from wechatpy.replies import MusicReply

        reply = MusicReply()
        reply.thumb_media_id = '123456'
        reply.title = 'test'
        reply.description = 'test'
        reply.music_url = 'http://www.qq.com'
        reply.hq_music_url = None

        self.assertEqual('123456', reply.thumb_media_id)
        self.assertEqual('test', reply.title)
        self.assertEqual('test', reply.description)
        self.assertEqual('http://www.qq.com', reply.music_url)
        self.assertTrue(reply.hq_music_url is None)
