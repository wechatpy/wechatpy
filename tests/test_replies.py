# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import time
import unittest
import six

from wechatpy.replies import TextReply, create_reply


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
        create_time = '<CreateTime>{}</CreateTime>'.format(timestamp)
        self.assertTrue(create_time in r)


class CreateReplyTestCase(unittest.TestCase):

    def test_create_reply_with_text_not_render(self):
        text = 'test'
        reply = create_reply(text, render=False)
        self.assertEqual('text', reply.type)
        self.assertEquals(text, reply.content)

    def test_create_reply_with_text_render(self):
        text = 'test'
        reply = create_reply(text)
        self.assertTrue(isinstance(reply, six.text_type))

    def test_create_reply_should_return_none(self):
        reply = create_reply(None)
        self.assertIsNone(reply)

    def test_create_reply_with_message(self):
        from wechatpy.messages import TextMessage

        msg = TextMessage({
            'FromUserName': 'user1',
            'ToUserName': 'user2',
        })
        reply = create_reply('test', msg, render=False)

        self.assertEqual('user1', reply.target)
        self.assertEqual('user2', reply.source)

    def test_create_reply_with_reply(self):
        _reply = TextReply(content='test')
        reply = create_reply(_reply, render=False)

        self.assertEqual(_reply, reply)

    def test_create_reply_with_articles(self):
        articles = [
            {
                'title': 'test 1',
                'description': 'test 1',
                'image': 'http://www.qq.com/1.png',
                'url': 'http://www.qq.com/1'
            },
            {
                'title': 'test 2',
                'description': 'test 2',
                'image': 'http://www.qq.com/2.png',
                'url': 'http://www.qq.com/2'
            },
            {
                'title': 'test 3',
                'description': 'test 3',
                'image': 'http://www.qq.com/3.png',
                'url': 'http://www.qq.com/3'
            },
        ]
        reply = create_reply(articles, render=False)
        self.assertEqual('news', reply.type)

    def test_create_reply_with_more_than_ten_articles(self):
        articles = [
            {
                'title': 'test 1',
                'description': 'test 1',
                'image': 'http://www.qq.com/1.png',
                'url': 'http://www.qq.com/1'
            },
            {
                'title': 'test 2',
                'description': 'test 2',
                'image': 'http://www.qq.com/2.png',
                'url': 'http://www.qq.com/2'
            },
            {
                'title': 'test 3',
                'description': 'test 3',
                'image': 'http://www.qq.com/3.png',
                'url': 'http://www.qq.com/3'
            },
            {
                'title': 'test 4',
                'description': 'test 4',
                'image': 'http://www.qq.com/4.png',
                'url': 'http://www.qq.com/4'
            },
            {
                'title': 'test 5',
                'description': 'test 5',
                'image': 'http://www.qq.com/5.png',
                'url': 'http://www.qq.com/5'
            },
            {
                'title': 'test 6',
                'description': 'test 6',
                'image': 'http://www.qq.com/6.png',
                'url': 'http://www.qq.com/6'
            },
            {
                'title': 'test 7',
                'description': 'test 7',
                'image': 'http://www.qq.com/7.png',
                'url': 'http://www.qq.com/7'
            },
            {
                'title': 'test 8',
                'description': 'test 8',
                'image': 'http://www.qq.com/8.png',
                'url': 'http://www.qq.com/8'
            },
            {
                'title': 'test 9',
                'description': 'test 9',
                'image': 'http://www.qq.com/9.png',
                'url': 'http://www.qq.com/9'
            },
            {
                'title': 'test 10',
                'description': 'test 10',
                'image': 'http://www.qq.com/10.png',
                'url': 'http://www.qq.com/10'
            },
            {
                'title': 'test 11',
                'description': 'test 11',
                'image': 'http://www.qq.com/11.png',
                'url': 'http://www.qq.com/11'
            },
        ]
        self.assertRaises(AttributeError, create_reply, articles)
