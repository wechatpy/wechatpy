# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest

from wechatpy import parse_message


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

    def test_parse_subscribe_event(self):
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

    def test_parse_subscribe_scan_event(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
        <EventKey><![CDATA[qrscene_123123]]></EventKey>
        <Ticket><![CDATA[TICKET]]></Ticket>
        </xml>"""

        msg = parse_message(xml)

        self.assertEqual('event', msg.type)
        self.assertEqual('subscribe_scan', msg.event)
        self.assertEqual('123123', msg.scene_id)
        self.assertEqual('TICKET', msg.ticket)

    def test_parse_scan_event(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[SCAN]]></Event>
        <EventKey><![CDATA[123123]]></EventKey>
        <Ticket><![CDATA[TICKET]]></Ticket>
        </xml>"""

        msg = parse_message(xml)

        self.assertEqual('event', msg.type)
        self.assertEqual('scan', msg.event)
        self.assertEqual('123123', msg.scene_id)
        self.assertEqual('TICKET', msg.ticket)

    def test_parse_location_event(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[LOCATION]]></Event>
        <Latitude>23.137466</Latitude>
        <Longitude>113.352425</Longitude>
        <Precision>119.385040</Precision>
        </xml>"""

        msg = parse_message(xml)

        self.assertEqual('event', msg.type)
        self.assertEqual('location', msg.event)
        self.assertEqual(23.137466, msg.latitude)
        self.assertEqual(113.352425, msg.longitude)
        self.assertEqual(119.385040, msg.precision)

    def test_parse_click_event(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[CLICK]]></Event>
        <EventKey><![CDATA[EVENTKEY]]></EventKey>
        </xml>"""

        msg = parse_message(xml)

        self.assertEqual('event', msg.type)
        self.assertEqual('click', msg.event)
        self.assertEqual('EVENTKEY', msg.key)

    def test_parse_view_event(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[VIEW]]></Event>
        <EventKey><![CDATA[www.qq.com]]></EventKey>
        </xml>"""

        msg = parse_message(xml)

        self.assertEqual('event', msg.type)
        self.assertEqual('view', msg.event)
        self.assertEqual('www.qq.com', msg.url)

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

    def test_parse_subscribe_scan_product_event(self):
        from wechatpy.events import SubscribeScanProductEvent

        xml = """<xml>
        <ToUserName><![CDATA[gh_fbe8a958756e]]></ToUserName>
        <FromUserName><![CDATA[otAzGjrS4AYCmeJM1GhEOcHXXTAo]]></FromUserName>
        <CreateTime>1433259128</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
        <EventKey><![CDATA[scanbarcode|keystandard|keystr]]></EventKey>
        </xml>"""

        msg = parse_message(xml)
        self.assertTrue(isinstance(msg, SubscribeScanProductEvent))
        self.assertEqual('scanbarcode', msg.scene)
        self.assertEqual('keystandard', msg.standard)
        self.assertEqual('keystr', msg.key)

        xml = """<xml>
        <ToUserName><![CDATA[gh_fbe8a958756e]]></ToUserName>
        <FromUserName><![CDATA[otAzGjrS4AYCmeJM1GhEOcHXXTAo]]></FromUserName>
        <CreateTime>1433259128</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
        <EventKey><![CDATA[scanimage|keystandard|keystr]]></EventKey>
        </xml>"""

        msg = parse_message(xml)
        self.assertTrue(isinstance(msg, SubscribeScanProductEvent))
        self.assertEqual('scanimage', msg.scene)
        self.assertEqual('keystandard', msg.standard)
        self.assertEqual('keystr', msg.key)
