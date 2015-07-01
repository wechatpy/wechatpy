# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from wechatpy.fields import IntegerField, BaseField
from wechatpy import events


EVENT_TYPES = {}


def register_event(event_type):
    def register(cls):
        EVENT_TYPES[event_type] = cls
        return cls
    return register


@register_event('subscribe')
class SubscribeEvent(events.SubscribeEvent):
    """
    成员关注事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接受事件
    """
    agent = IntegerField('AgentID', 0)


@register_event('unsubscribe')
class UnsubscribeEvent(events.UnsubscribeEvent):
    """
    成员取消关注事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接受事件
    """
    agent = IntegerField('AgentID', 0)


@register_event('click')
class ClickEvent(events.ClickEvent):
    """
    点击菜单拉取消息事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接受事件
    """
    agent = IntegerField('AgentID', 0)


@register_event('view')
class ViewEvent(events.ViewEvent):
    """
    点击菜单跳转链接事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接受事件
    """
    agent = IntegerField('AgentID', 0)


@register_event('location')
class LocationEvent(events.LocationEvent):
    """
    上报地理位置事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接受事件
    """
    agent = IntegerField('AgentID', 0)


@register_event('scancode_push')
class ScanCodePushEvent(events.ScanCodePushEvent):
    """
    扫码推事件的事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接受事件
    """
    agent = IntegerField('AgentID', 0)


@register_event('scancode_waitmsg')
class ScanCodeWaitMsgEvent(events.ScanCodeWaitMsgEvent):
    """
    扫码推事件且弹出“消息接收中”提示框的事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接受事件
    """
    agent = IntegerField('AgentID', 0)


@register_event('pic_sysphoto')
class PicSysPhotoEvent(events.PicSysPhotoEvent):
    """
    弹出系统拍照发图事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接受事件
    """
    agent = IntegerField('AgentID', 0)


@register_event('pic_photo_or_album')
class PicPhotoOrAlbumEvent(events.PicPhotoOrAlbumEvent):
    """
    弹出拍照或相册发图事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接受事件
    """
    agent = IntegerField('AgentID', 0)


@register_event('pic_weixin')
class PicWeChatEvent(events.PicWeChatEvent):
    """
    弹出微信相册发图器事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接受事件
    """
    agent = IntegerField('AgentID', 0)


@register_event('location_select')
class LocationSelectEvent(events.LocationSelectEvent):
    """
    弹出地理位置选择器事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接受事件
    """
    agent = IntegerField('AgentID', 0)


@register_event('enter_agent')
class EnterAgentEvent(events.BaseEvent):
    """
    用户进入应用的事件推送
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接受事件
    """
    agent = IntegerField('AgentID', 0)
    event = 'enter_agent'


@register_event('batch_job_result')
class BatchJobResultEvent(events.BaseEvent):
    """
    异步任务完成事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接受事件
    """
    event = 'batch_job_result'
    batch_job = BaseField('BatchJob')

    @property
    def job_id(self):
        return self.batch_job['JobId']

    @property
    def job_type(self):
        return self.batch_job['JobType']

    @property
    def err_code(self):
        return self.batch_job['ErrCode']

    @property
    def err_msg(self):
        return self.batch_job['ErrMsg']
