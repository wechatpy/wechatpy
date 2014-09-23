from __future__ import absolute_import, unicode_literals
from ..fields import IntegerField
from .. import messages


MESSAGE_TYPES = {}


def register_message(msg_type):
    def register(cls):
        MESSAGE_TYPES[msg_type] = cls
        return cls
    return register


@register_message('text')
class TextMessage(messages.TextMessage):
    agent = IntegerField('AgentID', 0)


@register_message('image')
class ImageMessage(messages.ImageMessage):
    agent = IntegerField('AgentID', 0)


@register_message('voice')
class VoiceMessage(messages.VoiceMessage):
    agent = IntegerField('AgentID', 0)


@register_message('video')
class VideoMessage(messages.VideoMessage):
    agent = IntegerField('AgentID', 0)


@register_message('location')
class LocationMessage(messages.LocationMessage):
    agent = IntegerField('AgentID', 0)
