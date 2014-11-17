# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest
from wechatpy import parse_message


class EventsTestCase(unittest.TestCase):

    def test_scan_code_push_event(self):
        from wechatpy.events import ScanCodePushEvent

        xml = """<xml>
        <ToUserName><![CDATA[gh_e136c6e50636]]></ToUserName>
        <FromUserName><![CDATA[oMgHVjngRipVsoxg6TuX3vz6glDg]]></FromUserName>
        <CreateTime>1408090502</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[scancode_push]]></Event>
        <EventKey><![CDATA[6]]></EventKey>
        <ScanCodeInfo><ScanType><![CDATA[qrcode]]></ScanType>
        <ScanResult><![CDATA[1]]></ScanResult>
        </ScanCodeInfo>
        </xml>"""

        event = parse_message(xml)

        self.assertTrue(isinstance(event, ScanCodePushEvent))
        self.assertEqual('qrcode', event.scan_type)
        self.assertEqual('1', event.scan_result)

    def test_scan_code_waitmsg_event(self):
        from wechatpy.events import ScanCodeWaitMsgEvent

        xml = """<xml>
        <ToUserName><![CDATA[gh_e136c6e50636]]></ToUserName>
        <FromUserName><![CDATA[oMgHVjngRipVsoxg6TuX3vz6glDg]]></FromUserName>
        <CreateTime>1408090606</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[scancode_waitmsg]]></Event>
        <EventKey><![CDATA[6]]></EventKey>
        <ScanCodeInfo><ScanType><![CDATA[qrcode]]></ScanType>
        <ScanResult><![CDATA[2]]></ScanResult>
        </ScanCodeInfo>
        </xml>"""

        event = parse_message(xml)

        self.assertTrue(isinstance(event, ScanCodeWaitMsgEvent))
        self.assertEqual('qrcode', event.scan_type)
        self.assertEqual('2', event.scan_result)

    def test_pic_sysphoto_event(self):
        from wechatpy.events import PicSysPhotoEvent

        xml = """<xml>
        <ToUserName><![CDATA[gh_e136c6e50636]]></ToUserName>
        <FromUserName><![CDATA[oMgHVjngRipVsoxg6TuX3vz6glDg]]></FromUserName>
        <CreateTime>1408090651</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[pic_sysphoto]]></Event>
        <EventKey><![CDATA[6]]></EventKey>
        <SendPicsInfo><Count>1</Count>
        <PicList>
            <item>
            <PicMd5Sum><![CDATA[1b5f7c23b5bf75682a53e7b6d163e185]]></PicMd5Sum>
            </item>
        </PicList>
        </SendPicsInfo>
        </xml>"""

        event = parse_message(xml)

        self.assertTrue(isinstance(event, PicSysPhotoEvent))
        self.assertEqual(1, event.count)
        self.assertEqual(
            '1b5f7c23b5bf75682a53e7b6d163e185',
            event.pictures[0]['PicMd5Sum']
        )

    def test_pic_photo_or_album_event(self):
        from wechatpy.events import PicPhotoOrAlbumEvent

        xml = """<xml>
        <ToUserName><![CDATA[gh_e136c6e50636]]></ToUserName>
        <FromUserName><![CDATA[oMgHVjngRipVsoxg6TuX3vz6glDg]]></FromUserName>
        <CreateTime>1408090816</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[pic_photo_or_album]]></Event>
        <EventKey><![CDATA[6]]></EventKey>
        <SendPicsInfo><Count>1</Count>
        <PicList>
        <item>
        <PicMd5Sum><![CDATA[5a75aaca956d97be686719218f275c6b]]></PicMd5Sum>
        </item>
        </PicList>
        </SendPicsInfo>
        </xml>"""

        event = parse_message(xml)

        self.assertTrue(isinstance(event, PicPhotoOrAlbumEvent))
        self.assertEqual(1, event.count)
        self.assertEqual(
            '5a75aaca956d97be686719218f275c6b',
            event.pictures[0]['PicMd5Sum']
        )

    def test_pic_wechat_event(self):
        from wechatpy.events import PicWeChatEvent

        xml = """<xml>
        <ToUserName><![CDATA[gh_e136c6e50636]]></ToUserName>
        <FromUserName><![CDATA[oMgHVjngRipVsoxg6TuX3vz6glDg]]></FromUserName>
        <CreateTime>1408090816</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[pic_weixin]]></Event>
        <EventKey><![CDATA[6]]></EventKey>
        <SendPicsInfo><Count>1</Count>
        <PicList>
        <item>
        <PicMd5Sum><![CDATA[5a75aaca956d97be686719218f275c6b]]></PicMd5Sum>
        </item>
        </PicList>
        </SendPicsInfo>
        </xml>"""

        event = parse_message(xml)

        self.assertTrue(isinstance(event, PicWeChatEvent))
        self.assertEqual(1, event.count)
        self.assertEqual(
            '5a75aaca956d97be686719218f275c6b',
            event.pictures[0]['PicMd5Sum']
        )

    def test_location_select_event(self):
        from wechatpy.events import LocationSelectEvent

        xml = """<xml>
        <ToUserName><![CDATA[gh_e136c6e50636]]></ToUserName>
        <FromUserName><![CDATA[oMgHVjngRipVsoxg6TuX3vz6glDg]]></FromUserName>
        <CreateTime>1408091189</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[location_select]]></Event>
        <EventKey><![CDATA[6]]></EventKey>
        <SendLocationInfo><Location_X><![CDATA[23]]></Location_X>
        <Location_Y><![CDATA[113]]></Location_Y>
        <Scale><![CDATA[15]]></Scale>
        <Label><![CDATA[广州市海珠区客村艺苑路 106号]]></Label>
        <Poiname><![CDATA[]]></Poiname>
        </SendLocationInfo>
        </xml>"""

        event = parse_message(xml)

        self.assertTrue(isinstance(event, LocationSelectEvent))
        self.assertEqual(('23', '113'), event.location)
        self.assertEqual('15', event.scale)
        self.assertTrue(event.poiname is None)
        self.assertEqual('广州市海珠区客村艺苑路 106号', event.label)

    def test_merchant_order_event(self):
        from wechatpy.events import MerchantOrderEvent

        xml = """<xml>
        <ToUserName><![CDATA[weixin_media1]]></ToUserName>
        <FromUserName><![CDATA[oDF3iYyVlek46AyTBbMRVV8VZVlI]]></FromUserName>
        <CreateTime>1398144192</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[merchant_order]]></Event>
        <OrderId><![CDATA[test_order_id]]></OrderId>
        <OrderStatus>2</OrderStatus>
        <ProductId><![CDATA[test_product_id]]></ProductId>
        <SkuInfo><![CDATA[10001:1000012;10002:100021]]></SkuInfo>
        </xml>"""

        event = parse_message(xml)

        self.assertTrue(isinstance(event, MerchantOrderEvent))
        self.assertEqual('test_order_id', event.order_id)
        self.assertEqual(2, event.order_status)
        self.assertEqual('test_product_id', event.product_id)
        self.assertEqual('10001:1000012;10002:100021', event.sku_info)
