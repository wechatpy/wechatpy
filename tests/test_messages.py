# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest
import time

from wechatpy import parse_message


class MessagesTestCase(unittest.TestCase):

    def test_base_message(self):
        from wechatpy.messages import TextMessage

        timestamp = int(time.time())
        msg = TextMessage({
            'MsgId': 123456,
            'MsgType': 'text',
            'FromUserName': 'user1',
            'ToUserName': 'user2',
            'CreateTime': timestamp,
        })

        self.assertEqual(123456, msg.id)
        self.assertEqual('user1', msg.source)
        self.assertEqual('user2', msg.target)
        self.assertEqual(timestamp, msg.time)

    def test_text_message(self):
        from wechatpy.messages import TextMessage

        msg = TextMessage({
            'Content': 'test',
        })

        self.assertEqual('test', msg.content)

    def test_image_message(self):
        from wechatpy.messages import ImageMessage

        msg = ImageMessage({
            'PicUrl': 'http://www.qq.com/1.png',
        })

        self.assertEqual('http://www.qq.com/1.png', msg.image)

    def test_voice_message(self):
        from wechatpy.messages import VoiceMessage

        msg = VoiceMessage({
            'MediaId': '123456',
            'Format': 'aac',
            'Recognition': 'test',
        })

        self.assertEqual('123456', msg.media_id)
        self.assertEqual('aac', msg.format)
        self.assertEqual('test', msg.recognition)

    def test_video_message(self):
        from wechatpy.messages import VideoMessage

        msg = VideoMessage({
            'MediaId': '123456',
            'ThumbMediaId': '123456',
        })

        self.assertEqual('123456', msg.media_id)
        self.assertEqual('123456', msg.thumb_media_id)

    def test_location_message(self):
        from wechatpy.messages import LocationMessage

        msg = LocationMessage({
            'Location_X': '123',
            'Location_Y': '456',
            'Scale': '1',
            'Label': 'test',
        })

        self.assertEqual('123', msg.location_x)
        self.assertEqual('456', msg.location_y)
        self.assertEquals('1', msg.scale)
        self.assertEqual('test', msg.label)

    def test_link_message(self):
        from wechatpy.messages import LinkMessage

        msg = LinkMessage({
            'Title': 'test',
            'Description': 'test',
            'Url': 'http://www.qq.com',
        })

        self.assertEqual('test', msg.title)
        self.assertEqual('test', msg.description)
        self.assertEqual('http://www.qq.com', msg.url)


class ParseMessageTestCase(unittest.TestCase):

    def test_parse_text_message(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
         <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[this is a test]]></Content>
        <MsgId>1234567890123456</MsgId>
        </xml>"""

        msg = parse_message(xml)
        self.assertEqual('text', msg.type)

    def test_parse_image_message(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <PicUrl><![CDATA[this is a url]]></PicUrl>
        <MediaId><![CDATA[media_id]]></MediaId>
        <MsgId>1234567890123456</MsgId>
        </xml>"""

        msg = parse_message(xml)
        self.assertEqual('image', msg.type)

    def test_parse_voice_message(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1357290913</CreateTime>
        <MsgType><![CDATA[voice]]></MsgType>
        <MediaId><![CDATA[media_id]]></MediaId>
        <Format><![CDATA[Format]]></Format>
        <MsgId>1234567890123456</MsgId>
        </xml>"""

        msg = parse_message(xml)
        self.assertEqual('voice', msg.type)

    def test_parse_video_message(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1357290913</CreateTime>
        <MsgType><![CDATA[video]]></MsgType>
        <MediaId><![CDATA[media_id]]></MediaId>
        <ThumbMediaId><![CDATA[thumb_media_id]]></ThumbMediaId>
        <MsgId>1234567890123456</MsgId>
        </xml>"""

        msg = parse_message(xml)
        self.assertEqual('video', msg.type)

    def test_parse_location_message(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1351776360</CreateTime>
        <MsgType><![CDATA[location]]></MsgType>
        <Location_X>23.134521</Location_X>
        <Location_Y>113.358803</Location_Y>
        <Scale>20</Scale>
        <Label><![CDATA[位置信息]]></Label>
        <MsgId>1234567890123456</MsgId>
        </xml>"""

        msg = parse_message(xml)
        self.assertEqual('location', msg.type)

    def test_parse_link_message(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1351776360</CreateTime>
        <MsgType><![CDATA[link]]></MsgType>
        <Title><![CDATA[公众平台官网链接]]></Title>
        <Description><![CDATA[公众平台官网链接]]></Description>
        <Url><![CDATA[url]]></Url>
        <MsgId>1234567890123456</MsgId>
        </xml>"""

        msg = parse_message(xml)
        self.assertEqual('link', msg.type)

    def test_parse_event_message(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
        </xml>"""

        msg = parse_message(xml)

        self.assertEqual('event', msg.type)
        self.assertEqual('subscribe', msg.event)

    def test_parse_unknown_message(self):
        from wechatpy.messages import UnknownMessage

        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[notsure]]></MsgType>
        <MsgId>1234567890123456</MsgId>
        </xml>"""

        msg = parse_message(xml)

        self.assertTrue(isinstance(msg, UnknownMessage))
