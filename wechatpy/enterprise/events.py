# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from ..fields import IntegerField
from .. import events


EVENT_TYPES = {}


def register_event(event_type):
    def register(cls):
        EVENT_TYPES[event_type] = cls
        return cls
    return register


@register_event('subscribe')
class SubscribeEvent(events.SubscribeEvent):
    agent = IntegerField('AgentID', 0)


@register_event('unsubscribe')
class UnsubscribeEvent(events.UnsubscribeEvent):
    agent = IntegerField('AgentID', 0)


@register_event('click')
class ClickEvent(events.ClickEvent):
    agent = IntegerField('AgentID', 0)


@register_event('view')
class ViewEvent(events.ViewEvent):
    agent = IntegerField('AgentID', 0)


@register_event('location')
class LocationEvent(events.LocationEvent):
    agent = IntegerField('AgentID', 0)


@register_event('scancode_push')
class ScanCodePushEvent(events.ScanCodePushEvent):
    agent = IntegerField('AgentID', 0)


@register_event('scancode_waitmsg')
class ScanCodeWaitMsgEvent(events.ScanCodeWaitMsgEvent):
    agent = IntegerField('AgentID', 0)


@register_event('pic_sysphoto')
class PicSysPhotoEvent(events.PicSysPhotoEvent):
    agent = IntegerField('AgentID', 0)


@register_event('pic_photo_or_album')
class PicPhotoOrAlbumEvent(events.PicPhotoOrAlbumEvent):
    agent = IntegerField('AgentID', 0)


@register_event('pic_weixin')
class PicWeChatEvent(events.PicWeChatEvent):
    agent = IntegerField('AgentID', 0)


@register_event('location_select')
class LocationSelectEvent(events.LocationSelectEvent):
    agent = IntegerField('AgentID', 0)


@register_event('enter_agent')
class EnterAgentEvent(events.BaseEvent):
    """
    用户进入应用的事件推送
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=%E6%8E%A5%E6%94%B6%E4%BA%8B%E4%BB%B6#.E7.94.A8.E6.88.B7.E8.BF.9B.E5.85.A5.E5.BA.94.E7.94.A8.E7.9A.84.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
    """
    agent = IntegerField('AgentID', 0)
    event = 'enter_agent'
