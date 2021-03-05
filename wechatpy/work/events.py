# -*- coding: utf-8 -*-
from wechatpy import events
from wechatpy.fields import BaseField, IntegerField, StringField

EVENT_TYPES = {}


def register_event(event_type):
    def register(cls):
        EVENT_TYPES[event_type] = cls
        return cls

    return register


@register_event("subscribe")
class SubscribeEvent(events.SubscribeEvent):
    """
    成员关注事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E6%88%90%E5%91%98%E5%85%B3%E6%B3%A8%E5%8F%8A%E5%8F%96%E6%B6%88%E5%85%B3%E6%B3%A8%E4%BA%8B%E4%BB%B6
    """

    agent = IntegerField("AgentID", 0)
    event = "subscribe"


@register_event("unsubscribe")
class UnsubscribeEvent(events.UnsubscribeEvent):
    """
    成员取消关注事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E6%88%90%E5%91%98%E5%85%B3%E6%B3%A8%E5%8F%8A%E5%8F%96%E6%B6%88%E5%85%B3%E6%B3%A8%E4%BA%8B%E4%BB%B6
    """

    agent = IntegerField("AgentID", 0)
    event = "unsubscribe"


@register_event("click")
class ClickEvent(events.ClickEvent):
    """
    点击菜单拉取消息事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E7%82%B9%E5%87%BB%E8%8F%9C%E5%8D%95%E6%8B%89%E5%8F%96%E6%B6%88%E6%81%AF%E7%9A%84%E4%BA%8B%E4%BB%B6%E6%8E%A8%E9%80%81
    """

    agent = IntegerField("AgentID", 0)
    event = "click"


@register_event("view")
class ViewEvent(events.ViewEvent):
    """
    点击菜单跳转链接事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E7%82%B9%E5%87%BB%E8%8F%9C%E5%8D%95%E8%B7%B3%E8%BD%AC%E9%93%BE%E6%8E%A5%E7%9A%84%E4%BA%8B%E4%BB%B6%E6%8E%A8%E9%80%81
    """

    agent = IntegerField("AgentID", 0)
    event = "view"


@register_event("location")
class LocationEvent(events.LocationEvent):
    """
    上报地理位置事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E4%B8%8A%E6%8A%A5%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE
    """

    agent = IntegerField("AgentID", 0)
    event = "location"


@register_event("scancode_push")
class ScanCodePushEvent(events.ScanCodePushEvent):
    """
    扫码推事件的事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E6%89%AB%E7%A0%81%E6%8E%A8%E4%BA%8B%E4%BB%B6%E7%9A%84%E4%BA%8B%E4%BB%B6%E6%8E%A8%E9%80%81
    """

    agent = IntegerField("AgentID", 0)
    event = "scancode_push"


@register_event("scancode_waitmsg")
class ScanCodeWaitMsgEvent(events.ScanCodeWaitMsgEvent):
    """
    扫码推事件且弹出“消息接收中”提示框的事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E6%89%AB%E7%A0%81%E6%8E%A8%E4%BA%8B%E4%BB%B6%E4%B8%94%E5%BC%B9%E5%87%BA%E2%80%9C%E6%B6%88%E6%81%AF%E6%8E%A5%E6%94%B6%E4%B8%AD%E2%80%9D%E6%8F%90%E7%A4%BA%E6%A1%86%E7%9A%84%E4%BA%8B%E4%BB%B6%E6%8E%A8%E9%80%81
    """

    agent = IntegerField("AgentID", 0)
    event = "scancode_waitmsg"


@register_event("pic_sysphoto")
class PicSysPhotoEvent(events.PicSysPhotoEvent):
    """
    弹出系统拍照发图事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E5%BC%B9%E5%87%BA%E7%B3%BB%E7%BB%9F%E6%8B%8D%E7%85%A7%E5%8F%91%E5%9B%BE%E7%9A%84%E4%BA%8B%E4%BB%B6%E6%8E%A8%E9%80%81
    """

    agent = IntegerField("AgentID", 0)
    event = "pic_sysphoto"


@register_event("pic_photo_or_album")
class PicPhotoOrAlbumEvent(events.PicPhotoOrAlbumEvent):
    """
    弹出拍照或相册发图事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E5%BC%B9%E5%87%BA%E6%8B%8D%E7%85%A7%E6%88%96%E8%80%85%E7%9B%B8%E5%86%8C%E5%8F%91%E5%9B%BE%E7%9A%84%E4%BA%8B%E4%BB%B6%E6%8E%A8%E9%80%81
    """

    agent = IntegerField("AgentID", 0)
    event = "pic_photo_or_album"


@register_event("pic_weixin")
class PicWeChatEvent(events.PicWeChatEvent):
    """
    弹出微信相册发图器事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E5%BC%B9%E5%87%BA%E5%BE%AE%E4%BF%A1%E7%9B%B8%E5%86%8C%E5%8F%91%E5%9B%BE%E5%99%A8%E7%9A%84%E4%BA%8B%E4%BB%B6%E6%8E%A8%E9%80%81
    """

    agent = IntegerField("AgentID", 0)
    event = "pic_weixin"


@register_event("location_select")
class LocationSelectEvent(events.LocationSelectEvent):
    """
    弹出地理位置选择器事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E5%BC%B9%E5%87%BA%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE%E9%80%89%E6%8B%A9%E5%99%A8%E7%9A%84%E4%BA%8B%E4%BB%B6%E6%8E%A8%E9%80%81
    """

    agent = IntegerField("AgentID", 0)
    event = "location_select"


@register_event("enter_agent")
class EnterAgentEvent(events.BaseEvent):
    """
    用户进入应用的事件推送

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E8%BF%9B%E5%85%A5%E5%BA%94%E7%94%A8
    """

    agent = IntegerField("AgentID", 0)
    event = "enter_agent"


@register_event("batch_job_result")
class BatchJobResultEvent(events.BaseEvent):
    """
    异步任务完成事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1%E5%AE%8C%E6%88%90%E4%BA%8B%E4%BB%B6%E6%8E%A8%E9%80%81
    """

    event = "batch_job_result"
    batch_job = BaseField("BatchJob")

    @property
    def job_id(self):
        return self.batch_job["JobId"]

    @property
    def job_type(self):
        return self.batch_job["JobType"]

    @property
    def err_code(self):
        return self.batch_job["ErrCode"]

    @property
    def err_msg(self):
        return self.batch_job["ErrMsg"]


@register_event("open_approval_change")
class OpenApprovalChangeEvent(events.BaseEvent):
    """
    审批状态通知事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E5%AE%A1%E6%89%B9%E7%8A%B6%E6%80%81%E9%80%9A%E7%9F%A5%E4%BA%8B%E4%BB%B6
    """

    event = "open_approval_change"
    agent = IntegerField("AgentID", 0)
    approval_info = BaseField("ApprovalInfo")

    @property
    def third_no(self):
        return self.approval_info["ThirdNo"]

    @property
    def open_sp_name(self):
        return self.approval_info["OpenSpName"]

    @property
    def open_template_id(self):
        return self.approval_info["OpenTemplateId"]

    @property
    def open_sp_status(self):
        return self.approval_info["OpenSpStatus"]

    @property
    def apply_time(self):
        return self.approval_info["ApplyTime"]

    @property
    def apply_user_name(self):
        return self.approval_info["ApplyUserName"]

    @property
    def apply_user_id(self):
        return self.approval_info["ApplyUserId"]

    @property
    def apply_user_party(self):
        return self.approval_info["ApplyUserParty"]

    @property
    def apply_user_image(self):
        return self.approval_info["ApplyUserImage"]

    @property
    def approval_nodes(self):
        return self.approval_info["ApprovalNodes"]

    @property
    def notify_nodes(self):
        return self.approval_info["NotifyNodes"]

    @property
    def approver_step(self):
        return self.approval_info["approverstep"]


@register_event("taskcard_click")
class TaskCardClickEvent(events.BaseEvent):
    """
    任务卡片事件推送

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/90240#%E4%BB%BB%E5%8A%A1%E5%8D%A1%E7%89%87%E4%BA%8B%E4%BB%B6%E6%8E%A8%E9%80%81
    """

    event = "taskcard_click"
    event_key = StringField("EventKey")
    agent = IntegerField("AgentID", 0)
    task_id = StringField("TaskId")


@register_event("change_external_contact")
class ChangeExternalContactEvent(events.BaseEvent):
    """
    外部联系人事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/92130#%E6%B7%BB%E5%8A%A0%E5%A4%96%E9%83%A8%E8%81%94%E7%B3%BB%E4%BA%BA%E4%BA%8B%E4%BB%B6
    """

    event = "change_external_contact"
    change_type = StringField("ChangeType")
    welcome_code = StringField("WelcomeCode")
    state = StringField("State")
    user_id = StringField("UserID")
    external_user_id = StringField("ExternalUserID")


@register_event("sys_approval_change")
class SysApprovalChangeEvent(events.BaseEvent):
    """
    系统审批状态通知事件

    详情请参阅
    https://work.weixin.qq.com/api/doc/90000/90135/91815
    """

    event = "sys_approval_change"
    agent = IntegerField("AgentID", 0)
    approval_info = BaseField("ApprovalInfo")

    @property
    def sp_no(self):
        return self.approval_info["SpNo"]

    @property
    def sp_name(self):
        return self.approval_info["SpName"]

    @property
    def template_id(self):
        return self.approval_info["TemplateId"]

    @property
    def sp_status(self):
        return self.approval_info["SpStatus"]

    @property
    def apply_time(self):
        return self.approval_info["ApplyTime"]

    @property
    def apply_user_id(self):
        return self.approval_info["Applyer"]["UserId"]

    @property
    def apply_user_party(self):
        return self.approval_info["Applyer"]["Party"]

    @property
    def sp_record(self):
        return self.approval_info["SpRecord"]

    @property
    def notifyer(self):
        return self.approval_info["Notifyer"]

    @property
    def comments(self):
        return self.approval_info["Comments"]

    @property
    def statu_change_event(self):
        return self.approval_info["StatuChangeEvent"]
