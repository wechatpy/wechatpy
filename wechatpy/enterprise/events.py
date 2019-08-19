# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from wechatpy import events
from wechatpy.fields import BaseField, IntegerField

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
    https://qydev.weixin.qq.com/wiki/index.php?title=接收事件#.E6.88.90.E5.91.98.E5.85.B3.E6.B3.A8.2F.E5.8F.96.E6.B6.88.E5.85.B3.E6.B3.A8.E4.BA.8B.E4.BB.B6
    """
    agent = IntegerField('AgentID', 0)
    event = 'subscribe'


@register_event('unsubscribe')
class UnsubscribeEvent(events.UnsubscribeEvent):
    """
    成员取消关注事件
    详情请参阅
    https://qydev.weixin.qq.com/wiki/index.php?title=接收事件#.E6.88.90.E5.91.98.E5.85.B3.E6.B3.A8.2F.E5.8F.96.E6.B6.88.E5.85.B3.E6.B3.A8.E4.BA.8B.E4.BB.B6
    """
    agent = IntegerField('AgentID', 0)
    event = 'unsubscribe'


@register_event('click')
class ClickEvent(events.ClickEvent):
    """
    点击菜单拉取消息事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接收事件#.E7.82.B9.E5.87.BB.E8.8F.9C.E5.8D.95.E6.8B.89.E5.8F.96.E6.B6.88.E6.81.AF.E7.9A.84.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
    """
    agent = IntegerField('AgentID', 0)
    event = 'click'


@register_event('view')
class ViewEvent(events.ViewEvent):
    """
    点击菜单跳转链接事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接收事件#.E7.82.B9.E5.87.BB.E8.8F.9C.E5.8D.95.E8.B7.B3.E8.BD.AC.E9.93.BE.E6.8E.A5.E7.9A.84.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
    """
    agent = IntegerField('AgentID', 0)
    event = 'view'


@register_event('location')
class LocationEvent(events.LocationEvent):
    """
    上报地理位置事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接收事件#.E4.B8.8A.E6.8A.A5.E5.9C.B0.E7.90.86.E4.BD.8D.E7.BD.AE.E4.BA.8B.E4.BB.B6
    """
    agent = IntegerField('AgentID', 0)
    event = 'location'


@register_event('scancode_push')
class ScanCodePushEvent(events.ScanCodePushEvent):
    """
    扫码推事件的事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接收事件#.E6.89.AB.E7.A0.81.E6.8E.A8.E4.BA.8B.E4.BB.B6.E7.9A.84.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
    """
    agent = IntegerField('AgentID', 0)
    event = 'scancode_push'


@register_event('scancode_waitmsg')
class ScanCodeWaitMsgEvent(events.ScanCodeWaitMsgEvent):
    """
    扫码推事件且弹出“消息接收中”提示框的事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接收事件#.E6.89.AB.E7.A0.81.E6.8E.A8.E4.BA.8B.E4.BB.B6.E4.B8.94.E5.BC.B9.E5.87.BA.E2.80.9C.E6.B6.88.E6.81.AF.E6.8E.A5.E6.94.B6.E4.B8.AD.E2.80.9D.E6.8F.90.E7.A4.BA.E6.A1.86.E7.9A.84.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
    """
    agent = IntegerField('AgentID', 0)
    event = 'scancode_waitmsg'


@register_event('pic_sysphoto')
class PicSysPhotoEvent(events.PicSysPhotoEvent):
    """
    弹出系统拍照发图事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接收事件#.E5.BC.B9.E5.87.BA.E7.B3.BB.E7.BB.9F.E6.8B.8D.E7.85.A7.E5.8F.91.E5.9B.BE.E7.9A.84.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
    """
    agent = IntegerField('AgentID', 0)
    event = 'pic_sysphoto'


@register_event('pic_photo_or_album')
class PicPhotoOrAlbumEvent(events.PicPhotoOrAlbumEvent):
    """
    弹出拍照或相册发图事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接收事件#.E5.BC.B9.E5.87.BA.E6.8B.8D.E7.85.A7.E6.88.96.E8.80.85.E7.9B.B8.E5.86.8C.E5.8F.91.E5.9B.BE.E7.9A.84.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
    """
    agent = IntegerField('AgentID', 0)
    event = 'pic_photo_or_album'


@register_event('pic_weixin')
class PicWeChatEvent(events.PicWeChatEvent):
    """
    弹出微信相册发图器事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接收事件#.E5.BC.B9.E5.87.BA.E5.BE.AE.E4.BF.A1.E7.9B.B8.E5.86.8C.E5.8F.91.E5.9B.BE.E5.99.A8.E7.9A.84.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
    """
    agent = IntegerField('AgentID', 0)
    event = 'pic_weixin'


@register_event('location_select')
class LocationSelectEvent(events.LocationSelectEvent):
    """
    弹出地理位置选择器事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接收事件#.E5.BC.B9.E5.87.BA.E5.9C.B0.E7.90.86.E4.BD.8D.E7.BD.AE.E9.80.89.E6.8B.A9.E5.99.A8.E7.9A.84.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
    """
    agent = IntegerField('AgentID', 0)
    event = 'location_select'


@register_event('enter_agent')
class EnterAgentEvent(events.BaseEvent):
    """
    用户进入应用的事件推送
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接收事件#.E6.88.90.E5.91.98.E8.BF.9B.E5.85.A5.E5.BA.94.E7.94.A8.E7.9A.84.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
    """
    agent = IntegerField('AgentID', 0)
    event = 'enter_agent'


@register_event('batch_job_result')
class BatchJobResultEvent(events.BaseEvent):
    """
    异步任务完成事件
    详情请参阅
    http://qydev.weixin.qq.com/wiki/index.php?title=接收事件#.E5.BC.82.E6.AD.A5.E4.BB.BB.E5.8A.A1.E5.AE.8C.E6.88.90.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
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
