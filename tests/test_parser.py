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
        self.assertEqual('', msg.key)

    def test_parse_subscribe_event_with_last_trade_no(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
        <EventKey><![CDATA[last_trade_no_4008072001201701105817415015]]></EventKey>
        </xml>"""

        msg = parse_message(xml)

        self.assertEqual('event', msg.type)
        self.assertEqual('subscribe', msg.event)
        self.assertEqual('last_trade_no_4008072001201701105817415015', msg.key)

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

    def test_parse_user_authorize_invoice_event(self):
        """ Test parsing xml for UserAuthorizeInvoiceEvent """
        from wechatpy.events import UserAuthorizeInvoiceEvent

        xml = """<xml>
        <ToUserName><![CDATA[gh_fc0a06a20993]]></ToUserName>
        <FromUserName><![CDATA[oZI8Fj040-be6rlDohc6gkoPOQTQ]]></FromUserName>
        <CreateTime>1475134700</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[user_authorize_invoice]]></Event>
        <SuccOrderId><![CDATA[1202933957956]]></SuccOrderId>
        <FailOrderId><![CDATA[]]></FailOrderId>
        <AppId><![CDATA[wx1234567887654321]]></AppId>
        <Source><![CDATA[]]></Source>
        </xml>"""

        msg = parse_message(xml)
        self.assertTrue(isinstance(msg, UserAuthorizeInvoiceEvent))
        self.assertEqual('1202933957956', msg.success_order_id)
        self.assertEqual(None, msg.fail_order_id)
        self.assertEqual('wx1234567887654321', msg.app_id)
        self.assertEqual(None, msg.auth_source)

    def test_parse_update_invoice_status_event(self):
        """ Test parsing xml for UpdateInvoiceStatusEvent """
        from wechatpy.events import UpdateInvoiceStatusEvent

        xml = """<xml>
        <ToUserName><![CDATA[gh_9e1765b5568e]]></ToUserName>
        <FromUserName><![CDATA[ojZ8Ytz4lESgdWZ34L_R1TvB2Kds]]></FromUserName>
        <CreateTime>1478068440</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[update_invoice_status]]></Event>
        <Status><![CDATA[INVOICE_REIMBURSE_INIT]]></Status>
        <CardId><![CDATA[pjZ8Yt7Um2jYxzneP8GomnxoVFWo]]></CardId>
        <Code><![CDATA[186921658591]]></Code>
        </xml>"""

        msg = parse_message(xml)
        self.assertTrue(isinstance(msg, UpdateInvoiceStatusEvent))
        self.assertEqual('INVOICE_REIMBURSE_INIT', msg.status)
        self.assertEqual('pjZ8Yt7Um2jYxzneP8GomnxoVFWo', msg.card_id)
        self.assertEqual('186921658591', msg.code)

    def test_parse_submit_invoice_title_event(self):
        """ Test parsing xml for SubmitInvoiceTitleEvent """
        from wechatpy.events import SubmitInvoiceTitleEvent

        xml = """<xml>
        <ToUserName><![CDATA[gh_fc0a06a20993]]></ToUserName>
        <FromUserName><![CDATA[oZI8Fj040-be6rlDohc6gkoPOQTQ]]></FromUserName>
        <CreateTime>1475134700</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[submit_invoice_title]]></Event>
        <title><![CDATA[样例公司抬头]]></title>
        <tax_no><![CDATA[1486715661]]></tax_no>
        <addr><![CDATA[abc]]></addr>
        <phone><![CDATA[13313331333]]></phone>
        <bank_type><![CDATA[bt]]></bank_type>
        <bank_no><![CDATA[bn]]></bank_no>
        <attach><![CDATA[at]]></attach>
        <title_type><![CDATA[InvoiceUserTitleBusinessType]]></title_type>
        </xml>"""

        msg = parse_message(xml)
        self.assertTrue(isinstance(msg, SubmitInvoiceTitleEvent))
        self.assertEqual('样例公司抬头', msg.title)
        self.assertEqual('1486715661', msg.tax_no)
        self.assertEqual('abc', msg.addr)
        self.assertEqual('13313331333', msg.phone)
        self.assertEqual('bt', msg.bank_type)
        self.assertEqual('bn', msg.bank_no)
        self.assertEqual('at', msg.attach)
        self.assertEqual('InvoiceUserTitleBusinessType', msg.title_type)

    def test_parse_device_text_event(self):
        from wechatpy.events import DeviceTextEvent

        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[device_text]]></MsgType>
        <MsgId>1234567890123456</MsgId>
        <OpenID><![CDATA[123]]></OpenID>
        <DeviceID><![CDATA[123]]></DeviceID>
        <DeviceType><![CDATA[123]]></DeviceType>
        <SessionID><![CDATA[123]]></SessionID>
        <Content><![CDATA[MTIz]]></Content>
        </xml>"""

        msg = parse_message(xml)

        self.assertTrue(isinstance(msg, DeviceTextEvent))
        self.assertEqual('123', msg.content)
        self.assertEqual('123', msg.device_type)
        self.assertEqual('123', msg.device_id)

    def test_parse_device_bind_event(self):
        from wechatpy.events import DeviceBindEvent

        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[device_event]]></MsgType>
        <MsgId>1234567890123456</MsgId>
        <Event><![CDATA[bind]]></Event>
        <OpenID><![CDATA[123]]></OpenID>
        <DeviceID><![CDATA[123]]></DeviceID>
        <DeviceType><![CDATA[123]]></DeviceType>
        <SessionID><![CDATA[123]]></SessionID>
        <Content><![CDATA[MTIz]]></Content>
        </xml>"""

        msg = parse_message(xml)

        self.assertTrue(isinstance(msg, DeviceBindEvent))
        self.assertEqual('123', msg.content)
        self.assertEqual('123', msg.device_type)
        self.assertEqual('123', msg.device_id)
