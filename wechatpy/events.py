# -*- coding: utf-8 -*-
"""
    wechatpy.events
    ~~~~~~~~~~~~~~~~

    This module contains all the events WeChat callback uses.

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals

from wechatpy.fields import (
    StringField,
    FloatField,
    IntegerField,
    BaseField,
    Base64DecodeField,
    DateTimeField
)
from wechatpy.messages import BaseMessage


EVENT_TYPES = {}


def register_event(event_type):
    """
    Register the event class so that they can be accessed from EVENT_TYPES

    :param event_type: Event type
    """
    def register(cls):
        EVENT_TYPES[event_type] = cls
        return cls
    return register


class BaseEvent(BaseMessage):
    """Base class for all events"""
    type = 'event'
    event = ''


@register_event('subscribe')
class SubscribeEvent(BaseEvent):
    """
    用户关注事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/2/5baf56ce4947d35003b86a9805634b1e.html
    """
    event = 'subscribe'
    key = StringField('EventKey', '')


@register_event('unsubscribe')
class UnsubscribeEvent(BaseEvent):
    """
    用户取消关注事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/2/5baf56ce4947d35003b86a9805634b1e.html
    """
    event = 'unsubscribe'


@register_event('subscribe_scan')
class SubscribeScanEvent(BaseEvent):
    """
    用户扫描二维码关注事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/2/5baf56ce4947d35003b86a9805634b1e.html
    """
    event = 'subscribe_scan'
    scene_id = StringField('EventKey')
    ticket = StringField('Ticket')


@register_event('scan')
class ScanEvent(BaseEvent):
    """
    用户扫描二维码事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/2/5baf56ce4947d35003b86a9805634b1e.html
    """
    event = 'scan'
    scene_id = StringField('EventKey')
    ticket = StringField('Ticket')


@register_event('location')
class LocationEvent(BaseEvent):
    """
    上报地理位置事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/2/5baf56ce4947d35003b86a9805634b1e.html
    """
    event = 'location'
    latitude = FloatField('Latitude', 0.0)
    longitude = FloatField('Longitude', 0.0)
    precision = FloatField('Precision', 0.0)


@register_event('click')
class ClickEvent(BaseEvent):
    """
    点击菜单拉取消息事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/2/5baf56ce4947d35003b86a9805634b1e.html
    """
    event = 'click'
    key = StringField('EventKey')


@register_event('view')
class ViewEvent(BaseEvent):
    """
    点击菜单跳转链接事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/2/5baf56ce4947d35003b86a9805634b1e.html
    """
    event = 'view'
    url = StringField('EventKey')


@register_event('masssendjobfinish')
class MassSendJobFinishEvent(BaseEvent):
    """
    群发消息任务完成事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html
    """
    id = IntegerField('MsgID', 0)
    event = 'masssendjobfinish'
    status = StringField('Status')
    total_count = IntegerField('TotalCount', 0)
    filter_count = IntegerField('FilterCount', 0)
    sent_count = IntegerField('SentCount', 0)
    error_count = IntegerField('ErrorCount', 0)


@register_event('templatesendjobfinish')
class TemplateSendJobFinishEvent(BaseEvent):
    """
    模板消息任务完成事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html
    """
    id = IntegerField('MsgID')
    event = 'templatesendjobfinish'
    status = StringField('Status')


class BaseScanCodeEvent(BaseEvent):
    key = StringField('EventKey')
    scan_code_info = BaseField('ScanCodeInfo', {})

    @property
    def scan_type(self):
        return self.scan_code_info['ScanType']

    @property
    def scan_result(self):
        return self.scan_code_info['ScanResult']


@register_event('scancode_push')
class ScanCodePushEvent(BaseScanCodeEvent):
    """
    扫码推事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/9/981d772286d10d153a3dc4286c1ee5b5.html
    """
    event = 'scancode_push'


@register_event('scancode_waitmsg')
class ScanCodeWaitMsgEvent(BaseScanCodeEvent):
    """
    扫码推事件且弹出“消息接收中”提示框的事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/9/981d772286d10d153a3dc4286c1ee5b5.html
    """
    event = 'scancode_waitmsg'


class BasePictureEvent(BaseEvent):
    key = StringField('EventKey')
    pictures_info = BaseField('SendPicsInfo', {})

    @property
    def count(self):
        return int(self.pictures_info['Count'])

    @property
    def pictures(self):
        if self.pictures_info['PicList']:
            items = self.pictures_info['PicList']['item']
            if self.count > 1:
                return items
            return [items]
        return []


@register_event('pic_sysphoto')
class PicSysPhotoEvent(BasePictureEvent):
    """
    弹出系统拍照发图的事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/9/981d772286d10d153a3dc4286c1ee5b5.html
    """
    event = 'pic_sysphoto'


@register_event('pic_photo_or_album')
class PicPhotoOrAlbumEvent(BasePictureEvent):
    """
    弹出拍照或者相册发图的事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/9/981d772286d10d153a3dc4286c1ee5b5.html
    """
    event = 'pic_photo_or_album'


@register_event('pic_weixin')
class PicWeChatEvent(BasePictureEvent):
    """
    弹出微信相册发图器的事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/9/981d772286d10d153a3dc4286c1ee5b5.html
    """
    event = 'pic_weixin'


@register_event('location_select')
class LocationSelectEvent(BaseEvent):
    """
    弹出地理位置选择器的事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/9/981d772286d10d153a3dc4286c1ee5b5.html
    """
    event = 'location_select'
    key = StringField('EventKey')
    location_info = BaseField('SendLocationInfo', {})

    @property
    def location_x(self):
        return self.location_info['Location_X']

    @property
    def location_y(self):
        return self.location_info['Location_Y']

    @property
    def location(self):
        return self.location_x, self.location_y

    @property
    def scale(self):
        return self.location_info['Scale']

    @property
    def label(self):
        return self.location_info['Label']

    @property
    def poiname(self):
        return self.location_info['Poiname']


@register_event('card_pass_check')
class CardPassCheckEvent(BaseEvent):
    event = 'card_pass_check'
    card_id = StringField('CardId')


@register_event('card_not_pass_check')
class CardNotPassCheckEvent(BaseEvent):
    event = 'card_not_pass_check'
    card_id = StringField('CardId')


@register_event('user_get_card')
class UserGetCardEvent(BaseEvent):
    """
    领取事件推送

    详情请参阅
    http://mp.weixin.qq.com/wiki/16/28b34ee91675a04cb24853768debded4.html#.E9.A2.86.E5.8F.96.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
    """
    event = 'user_get_card'
    card_id = StringField('CardId')
    is_given_by_friend = IntegerField('IsGiveByFriend')
    friend = StringField('FriendUserName')
    code = StringField('UserCardCode')
    old_code = StringField('OldUserCardCode')
    outer_id = StringField('OuterId')


@register_event('user_del_card')
class UserDeleteCardEvent(BaseEvent):
    """
    卡券删除事件推送

    详情请参阅
    http://mp.weixin.qq.com/wiki/16/28b34ee91675a04cb24853768debded4.html#.E5.88.A0.E9.99.A4.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
    """
    event = 'user_del_card'
    card_id = StringField('CardId')
    code = StringField('UserCardCode')


@register_event('user_consume_card')
class UserConsumeCardEvent(BaseEvent):
    """
    卡券核销事件推送

    详情请参阅
    http://mp.weixin.qq.com/wiki/16/28b34ee91675a04cb24853768debded4.html#.E6.A0.B8.E9.94.80.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
    """
    event = 'user_consume_card'
    card_id = StringField('CardId')
    code = StringField('UserCardCode')
    consume_source = StringField('ConsumeSource')
    location_id = StringField('LocationId')
    staff = StringField('StaffOpenId')


@register_event('merchant_order')
class MerchantOrderEvent(BaseEvent):
    event = 'merchant_order'
    order_id = StringField('OrderId')
    order_status = IntegerField('OrderStatus')
    product_id = StringField('ProductId')
    sku_info = StringField('SkuInfo')


@register_event('kf_create_session')
class KfCreateSessionEvent(BaseEvent):
    event = 'kf_create_session'
    account = StringField('KfAccount')


@register_event('kf_close_session')
class KfCloseSessionEvent(BaseEvent):
    event = 'kf_close_session'
    account = StringField('KfAccount')


@register_event('kf_switch_session')
class KfSwitchSessionEvent(BaseEvent):
    event = 'kf_switch_session'
    from_account = StringField('FromKfAccount')
    to_account = StringField('ToKfAccount')


@register_event('device_text')
class DeviceTextEvent(BaseEvent):
    event = 'device_text'
    device_type = StringField('DeviceType')
    device_id = StringField('DeviceID')
    session_id = StringField('SessionID')
    content = Base64DecodeField('Content')
    open_id = StringField('OpenID')


@register_event('device_bind')
class DeviceBindEvent(BaseEvent):
    event = 'device_bind'
    device_type = StringField('DeviceType')
    device_id = StringField('DeviceID')
    session_id = StringField('SessionID')
    content = Base64DecodeField('Content')
    open_id = StringField('OpenID')


@register_event('device_unbind')
class DeviceUnbindEvent(BaseEvent):
    event = 'device_unbind'
    device_type = StringField('DeviceType')
    device_id = StringField('DeviceID')
    session_id = StringField('SessionID')
    content = Base64DecodeField('Content')
    open_id = StringField('OpenID')


@register_event('device_subscribe_status')
class DeviceSubscribeStatusEvent(BaseEvent):
    event = 'device_subscribe_status'
    device_type = StringField('DeviceType')
    device_id = StringField('DeviceID')
    open_id = StringField('OpenID')
    op_type = IntegerField('OpType')


@register_event('device_unsubscribe_status')
class DeviceUnsubscribeStatusEvent(BaseEvent):
    event = 'device_unsubscribe_status'
    device_type = StringField('DeviceType')
    device_id = StringField('DeviceID')
    open_id = StringField('OpenID')
    op_type = IntegerField('OpType')


@register_event('shakearoundusershake')
class ShakearoundUserShakeEvent(BaseEvent):
    event = 'shakearound_user_shake'
    _chosen_beacon = BaseField('ChosenBeacon', {})
    _around_beacons = BaseField('AroundBeacons', {})

    @property
    def chosen_beacon(self):
        beacon = self._chosen_beacon
        if not beacon:
            return {}
        return {
            'uuid': beacon['Uuid'],
            'major': beacon['Major'],
            'minor': beacon['Minor'],
            'distance': float(beacon['Distance']),
        }

    @property
    def around_beacons(self):
        beacons = self._around_beacons
        if not beacons:
            return []

        ret = []
        for beacon in beacons['AroundBeacon']:
            ret.append({
                'uuid': beacon['Uuid'],
                'major': beacon['Major'],
                'minor': beacon['Minor'],
                'distance': float(beacon['Distance']),
            })
        return ret


@register_event('poi_check_notify')
class PoiCheckNotifyEvent(BaseEvent):
    event = 'poi_check_notify'
    poi_id = StringField('PoiId')
    uniq_id = StringField('UniqId')
    result = StringField('Result')
    message = StringField('Msg')


@register_event('wificonnected')
class WiFiConnectedEvent(BaseEvent):
    event = 'wificconnected'
    connect_time = IntegerField('ConnectTime')
    expire_time = IntegerField('ExpireTime')
    vendor_id = StringField('VendorId')
    shop_id = StringField('PlaceId')
    bssid = StringField('DeviceNo')


# ============================================================================
# 微信认证事件推送
# ============================================================================
@register_event('qualification_verify_success')
class QualificationVerifySuccessEvent(BaseEvent):
    """
    资质认证成功事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/1/7f81dec16b801b34629091094c099439.html
    """
    event = 'qualification_verify_success'
    expired_time = DateTimeField('ExpiredTime')


@register_event('qualification_verify_fail')
class QualificationVerifyFailEvent(BaseEvent):
    """
    资质认证失败事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/1/7f81dec16b801b34629091094c099439.html
    """
    event = 'qualification_verify_fail'
    fail_time = DateTimeField('FailTime')
    fail_reason = StringField('FailReason')


@register_event('naming_verify_success')
class NamingVerifySuccessEvent(BaseEvent):
    """
    名称认证成功事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/1/7f81dec16b801b34629091094c099439.html
    """
    event = 'naming_verify_success'
    expired_time = DateTimeField('ExpiredTime')


@register_event('naming_verify_fail')
class NamingVerifyFailEvent(BaseEvent):
    """
    名称认证失败事件

    客户端不打勾，但仍有接口权限。详情请参阅
    http://mp.weixin.qq.com/wiki/1/7f81dec16b801b34629091094c099439.html
    """
    event = 'naming_verify_fail'
    fail_time = DateTimeField('FailTime')
    fail_reason = StringField('FailReason')


@register_event('annual_renew')
class AnnualRenewEvent(BaseEvent):
    """
    年审通知事件

    详情请参阅
    http://mp.weixin.qq.com/wiki/1/7f81dec16b801b34629091094c099439.html
    """
    event = 'annual_renew'
    expired_time = DateTimeField('ExpiredTime')


@register_event('verify_expired')
class VerifyExpiredEvent(BaseEvent):
    """
    认证过期失效通知

    详情请参阅
    http://mp.weixin.qq.com/wiki/1/7f81dec16b801b34629091094c099439.html
    """
    event = 'verify_expired'
    expired_time = DateTimeField('ExpiredTime')


@register_event('user_scan_product')
class UserScanProductEvent(BaseEvent):
    """
    打开商品主页事件

    详情请参考
    http://mp.weixin.qq.com/wiki/15/f4109a5e44b4bfbc7eb1337eb739f3e3.html
    """
    event = 'user_scan_product'
    standard = StringField('KeyStandard')
    key = StringField('KeyStr')
    country = StringField('Country')
    province = StringField('Province')
    city = StringField('City')
    sex = IntegerField('Sex')
    scene = IntegerField('Scene')


@register_event('user_scan_product_enter_session')
class UserScanProductEnterSessionEvent(BaseEvent):
    """
    进入公众号事件

    详情请参考
    http://mp.weixin.qq.com/wiki/15/f4109a5e44b4bfbc7eb1337eb739f3e3.html
    """
    event = 'user_scan_product_enter_session'
    standard = StringField('KeyStandard')
    key = StringField('KeyStr')


@register_event('user_scan_product_async')
class UserScanProductAsyncEvent(BaseEvent):
    """
    地理位置信息异步推送事件

    详情请参考
    http://mp.weixin.qq.com/wiki/15/f4109a5e44b4bfbc7eb1337eb739f3e3.html
    """
    event = 'user_scan_product_async'
    standard = StringField('KeyStandard')
    key = StringField('KeyStr')
    region_code = StringField('RegionCode')


@register_event('user_scan_product_verify_action')
class UserScanProductVerifyActionEvent(BaseEvent):
    """
    商品审核结果事件

    详情请参考
    http://mp.weixin.qq.com/wiki/15/f4109a5e44b4bfbc7eb1337eb739f3e3.html
    """
    event = 'user_scan_product_verify_action'
    standard = StringField('KeyStandard')
    key = StringField('KeyStr')
    result = StringField('Result')
    reason = StringField('ReasonMsg')


@register_event('subscribe_scan_product')
class SubscribeScanProductEvent(BaseEvent):
    """
    用户在商品主页中关注公众号事件

    详情请参考
    http://mp.weixin.qq.com/wiki/15/f4109a5e44b4bfbc7eb1337eb739f3e3.html
    """
    event = 'subscribe_scan_product'
    event_key = StringField('EventKey')

    @property
    def scene(self):
        return self.event_key.split('|', 1)[0]

    @property
    def standard(self):
        return self.event_key.split('|')[1]

    @property
    def key(self):
        return self.event_key.split('|')[2]


@register_event('user_authorize_invoice')
class UserAuthorizeInvoiceEvent(BaseEvent):
    """
    用户授权发票事件
    （会包含一个订单号，不成功就失败）

    详情请参考
    https://mp.weixin.qq.com/wiki?id=mp1497082828_r1cI2
    """
    event = 'user_authorize_invoice'
    success_order_id = StringField('SuccOrderId')  # 授权成功的订单号
    fail_order_id = StringField('FailOrderId')  # 授权失败的订单号
    app_id = StringField('AppId')  # 用于接收事件推送的公众号的AppId
    auth_source = StringField('Source')  # 授权来源，web表示来自微信内H5，app标识来自app


@register_event('update_invoice_status')
class UpdateInvoiceStatusEvent(BaseEvent):
    """
    发票状态更新事件

    详情请参考
    https://mp.weixin.qq.com/wiki?id=mp1497082828_r1cI2
    """
    event = 'update_invoice_status'
    status = StringField('Status')  # 发票报销状态
    card_id = StringField('CardId')  # 发票 Card ID
    code = StringField('Code')  # 发票 Code


@register_event('submit_invoice_title')
class SubmitInvoiceTitleEvent(BaseEvent):
    """
    用户提交发票抬头事件

    详情请参考
    https://mp.weixin.qq.com/wiki?id=mp1496554912_vfWU0
    """
    event = 'submit_invoice_title'
    title = StringField('title')  # 抬头
    phone = StringField('phone')  # 联系方式
    tax_no = StringField('tax_no')  # 税号
    addr = StringField('addr')  # 地址
    bank_type = StringField('bank_type')  # 银行类型
    bank_no = StringField('bank_no')  # 银行号码
    attach = StringField('attach')  # 附加字段
    title_type = StringField('title_type')  # 抬头类型，个人InvoiceUserTitlePersonType, 公司InvoiceUserTitleBusinessType
