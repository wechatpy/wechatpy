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
