# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest
import time


class MessagesTestCase(unittest.TestCase):

    def test_message_init(self):
        from wechatpy.messages import TextMessage

        timestamp = int(time.time())
        msg = TextMessage({
            'MsgId': 123456,
            'MsgType': 'text',
            'FromUserName': 'user1',
            'ToUserName': 'user2',
            'CreateTime': timestamp,
            'Content': 'test',
        })

        self.assertEqual(123456, msg.id)
        self.assertEqual('user1', msg.source)
        self.assertEqual('user2', msg.target)
        self.assertEqual(timestamp, msg.time)
        self.assertEqual('test', msg.content)
