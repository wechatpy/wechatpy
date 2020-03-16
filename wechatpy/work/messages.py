# -*- coding: utf-8 -*-


from wechatpy import messages
from wechatpy.fields import IntegerField, StringField

MESSAGE_TYPES = {}


def register_message(msg_type):
    def register(cls):
        MESSAGE_TYPES[msg_type] = cls
        return cls

    return register


@register_message("text")
class TextMessage(messages.TextMessage):
    agent = IntegerField("AgentID", 0)


@register_message("image")
class ImageMessage(messages.ImageMessage):
    agent = IntegerField("AgentID", 0)


@register_message("voice")
class VoiceMessage(messages.VoiceMessage):
    agent = IntegerField("AgentID", 0)


@register_message("shortvideo")
class ShortVideoMessage(messages.ShortVideoMessage):
    agent = IntegerField("AgentID", 0)


@register_message("video")
class VideoMessage(messages.VideoMessage):
    agent = IntegerField("AgentID", 0)


@register_message("location")
class LocationMessage(messages.LocationMessage):
    agent = IntegerField("AgentID", 0)


@register_message("link")
class LinkMessage(messages.LinkMessage):
    agent = IntegerField("AgentID", 0)
    pic_url = StringField("PicUrl")
