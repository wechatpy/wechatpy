# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import time
import unittest


class ReplyTestCase(unittest.TestCase):

    def test_base_reply(self):
        from wechatpy.replies import TextReply

        timestamp = int(time.time())
        reply = TextReply(source='user1', target='user2')

        self.assertEqual('user1', reply.source)
        self.assertEqual('user2', reply.target)
        self.assertLessEqual(timestamp, reply.time)
