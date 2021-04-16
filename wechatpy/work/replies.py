# -*- coding: utf-8 -*-


from wechatpy import replies
from wechatpy.fields import IntegerField, TaskCardField

REPLY_TYPES = {}


def register_reply(reply_type):
    def register(cls):
        REPLY_TYPES[reply_type] = cls
        return cls

    return register


@register_reply("text")
class TextReply(replies.TextReply):
    agent = IntegerField("AgentID", 0)


@register_reply("image")
class ImageReply(replies.ImageReply):
    agent = IntegerField("AgentID", 0)


@register_reply("voice")
class VoiceReply(replies.VoiceReply):
    agent = IntegerField("AgentID", 0)


@register_reply("video")
class VideoReply(replies.VideoReply):
    agent = IntegerField("AgentID", 0)


@register_reply("news")
class ArticlesReply(replies.ArticlesReply):
    agent = IntegerField("AgentID", 0)


@register_reply("update_taskcard")
class TaskCardReply(replies.BaseReply):
    """被动回复格式-任务卡更新消息
    接口详细文档：
    https://work.weixin.qq.com/api/doc/90000/90135/90241#%E4%BB%BB%E5%8A%A1%E5%8D%A1%E7%89%87%E6%9B%B4%E6%96%B0%E6%B6%88%E6%81%AF
    """

    agent = IntegerField("AgentID", 0)
    type = "update_taskcard"
    taskcard = TaskCardField("")

    @property
    def replace_name(self):
        return self.taskcard

    @replace_name.setter
    def replace_name(self, value):
        self.taskcard = value


def create_reply(reply, message=None, render=False):
    r = None
    if isinstance(reply, replies.BaseReply):
        r = reply
        if message:
            r.source = message.target
            r.target = message.source
            r.agent = message.agent
    elif isinstance(reply, str):
        r = TextReply(message=message, content=reply)
    elif isinstance(reply, (tuple, list)):
        if len(reply) > 10:
            raise AttributeError("Can't add more than 10 articles in an ArticlesReply")
        r = ArticlesReply(message=message, articles=reply)
    if r and render:
        return r.render()
    return r
