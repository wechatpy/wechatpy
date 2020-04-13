# -*- coding: utf-8 -*-


from wechatpy import replies
from wechatpy.fields import IntegerField

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
