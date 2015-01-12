# -*- coding: utf-8 -*-
"""
    wechatpy.events
    ~~~~~~~~~~~~~~~~

    This module contains all the events WeChat callback uses.

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals

from .fields import StringField, FloatField, IntegerField, BaseField
from .messages import BaseMessage


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
    event = 'user_get_card'
    card_id = StringField('CardId')
    is_given_by_friend = IntegerField('IsGiveByFriend')
    code = StringField('UserCardCode')


@register_event('user_del_card')
class UserDeleteCardEvent(BaseEvent):
    event = 'user_del_card'
    card_id = StringField('CardId')
    code = StringField('UserCardCode')


@register_event('merchant_order')
class MerchantOrderEvent(BaseEvent):
    event = 'merchant_order'
    order_id = StringField('OrderId')
    order_status = IntegerField('OrderStatus')
    product_id = StringField('ProductId')
    sku_info = StringField('SkuInfo')
