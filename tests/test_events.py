# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest
from datetime import datetime
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

    def test_kf_create_session_event(self):
        from wechatpy.events import KfCreateSessionEvent

        xml = """<xml>
        <ToUserName><![CDATA[touser]]></ToUserName>
        <FromUserName><![CDATA[fromuser]]></FromUserName>
        <CreateTime>1399197672</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[kf_create_session]]></Event>
        <KfAccount><![CDATA[test1@test]]></KfAccount>
        </xml>"""

        event = parse_message(xml)
        self.assertTrue(isinstance(event, KfCreateSessionEvent))
        self.assertEqual('test1@test', event.account)

    def test_kf_close_session_event(self):
        from wechatpy.events import KfCloseSessionEvent

        xml = """<xml>
        <ToUserName><![CDATA[touser]]></ToUserName>
        <FromUserName><![CDATA[fromuser]]></FromUserName>
        <CreateTime>1399197672</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[kf_close_session]]></Event>
        <KfAccount><![CDATA[test1@test]]></KfAccount>
        </xml>"""

        event = parse_message(xml)
        self.assertTrue(isinstance(event, KfCloseSessionEvent))
        self.assertEqual('test1@test', event.account)

    def test_kf_switch_session_event(self):
        from wechatpy.events import KfSwitchSessionEvent

        xml = """<xml>
        <ToUserName><![CDATA[touser]]></ToUserName>
        <FromUserName><![CDATA[fromuser]]></FromUserName>
        <CreateTime>1399197672</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[kf_switch_session]]></Event>
        <FromKfAccount><![CDATA[test1@test]]></FromKfAccount>
        <ToKfAccount><![CDATA[test2@test]]></ToKfAccount>
        </xml>"""

        event = parse_message(xml)
        self.assertTrue(isinstance(event, KfSwitchSessionEvent))
        self.assertEqual('test1@test', event.from_account)
        self.assertEqual('test2@test', event.to_account)

    def test_template_send_job_finish_event(self):
        from wechatpy.events import TemplateSendJobFinishEvent

        xml = """<xml>
        <ToUserName><![CDATA[touser]]></ToUserName>
        <FromUserName><![CDATA[fromuser]]></FromUserName>
        <CreateTime>1395658920</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[TEMPLATESENDJOBFINISH]]></Event>
        <MsgID>200163836</MsgID>
        <Status><![CDATA[success]]></Status>
        </xml>"""

        event = parse_message(xml)
        self.assertTrue(isinstance(event, TemplateSendJobFinishEvent))
        self.assertEqual(200163836, event.id)
        self.assertEqual('success', event.status)

    def test_shakearound_user_shake_event(self):
        from wechatpy.events import ShakearoundUserShakeEvent

        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1433332012</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[ShakearoundUserShake]]></Event>
        <ChosenBeacon>
            <Uuid><![CDATA[uuid]]></Uuid>
            <Major>major</Major>
            <Minor>minor</Minor>
            <Distance>0.057</Distance>
        </ChosenBeacon>
        <AroundBeacons>
            <AroundBeacon>
                <Uuid><![CDATA[uuid]]></Uuid>
                <Major>major</Major>
                <Minor>minor</Minor>
                <Distance>166.816</Distance>
            </AroundBeacon>
            <AroundBeacon>
                <Uuid><![CDATA[uuid]]></Uuid>
                <Major>major</Major>
                <Minor>minor</Minor>
                <Distance>15.013</Distance>
            </AroundBeacon>
        </AroundBeacons>
        </xml>"""
        event = parse_message(xml)
        self.assertTrue(isinstance(event, ShakearoundUserShakeEvent))

        chosen_beacon = {
            'uuid': 'uuid',
            'major': 'major',
            'minor': 'minor',
            'distance': 0.057,
        }
        self.assertEqual(chosen_beacon, event.chosen_beacon)
        self.assertEqual(2, len(event.around_beacons))

    def test_wifi_connected_event(self):
        from wechatpy.events import WiFiConnectedEvent

        xml = """
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[WifiConnected]]></Event>
        <ConnectTime>0</ConnectTime>
        <ExpireTime>0</ExpireTime>
        <VendorId><![CDATA[3001224419]]></VendorId>
        <PlaceId><![CDATA[1234]]></PlaceId>
        <DeviceNo><![CDATA[00:1f:7a:ad:5c:a8]]></DeviceNo>
        </xml>"""
        event = parse_message(xml)
        self.assertTrue(isinstance(event, WiFiConnectedEvent))

        self.assertEqual(0, event.connect_time)
        self.assertEqual('1234', event.shop_id)
        self.assertEqual('00:1f:7a:ad:5c:a8', event.bssid)

    def test_qualification_verify_success_event(self):
        from wechatpy.events import QualificationVerifySuccessEvent

        xml = """
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>1442401156</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[qualification_verify_success]]></Event>
        <ExpiredTime>1442401156</ExpiredTime>
        </xml>"""
        event = parse_message(xml)
        self.assertTrue(isinstance(event, QualificationVerifySuccessEvent))
        self.assertTrue(isinstance(event.expired_time, datetime))

    def test_qualification_verify_fail_event(self):
        from wechatpy.events import QualificationVerifyFailEvent

        xml = """
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>1442401156</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[qualification_verify_fail]]></Event>
        <FailTime>1442401122</FailTime>
        <FailReason><![CDATA[by time]]></FailReason>
        </xml>"""
        event = parse_message(xml)
        self.assertTrue(isinstance(event, QualificationVerifyFailEvent))
        self.assertTrue(isinstance(event.fail_time, datetime))
        self.assertEqual(event.fail_reason, 'by time')

    def test_naming_verify_success_event(self):
        from wechatpy.events import NamingVerifySuccessEvent

        xml = """
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>1442401093</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[naming_verify_success]]></Event>
        <ExpiredTime>1442401093</ExpiredTime>
        </xml>"""
        event = parse_message(xml)
        self.assertTrue(isinstance(event, NamingVerifySuccessEvent))
        self.assertTrue(isinstance(event.expired_time, datetime))

    def test_naming_verify_fail_event(self):
        from wechatpy.events import NamingVerifyFailEvent

        xml = """
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>1442401061</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[naming_verify_fail]]></Event>
        <FailTime>1442401061</FailTime>
        <FailReason><![CDATA[by time]]></FailReason>
        </xml>"""
        event = parse_message(xml)
        self.assertTrue(isinstance(event, NamingVerifyFailEvent))
        self.assertTrue(isinstance(event.fail_time, datetime))
        self.assertEqual(event.fail_reason, 'by time')

    def test_annual_renew_event(self):
        from wechatpy.events import AnnualRenewEvent

        xml = """
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>1442401004</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[annual_renew]]></Event>
        <ExpiredTime>1442401004</ExpiredTime>
        </xml>"""
        event = parse_message(xml)
        self.assertTrue(isinstance(event, AnnualRenewEvent))
        self.assertTrue(isinstance(event.expired_time, datetime))

    def test_verify_expired_event(self):
        from wechatpy.events import VerifyExpiredEvent

        xml = """
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>1442400900</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[verify_expired]]></Event>
        <ExpiredTime>1442400900</ExpiredTime>
        </xml>"""
        event = parse_message(xml)
        self.assertTrue(isinstance(event, VerifyExpiredEvent))
        self.assertTrue(isinstance(event.expired_time, datetime))
