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
        create_time = '<CreateTime>{}</CreateTime>'.format(timestamp)
        self.assertTrue(create_time in r)
