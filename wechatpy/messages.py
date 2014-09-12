from __future__ import absolute_import, unicode_literals
import functools

from .fields import StringField, IntegerField, FloatField


MESSAGE_TYPES = {}


def register_message(type):
    @functools.wraps
    def register(cls):
        MESSAGE_TYPES[type] = cls
        return cls
    return register


class BaseMessage(object):
    type = 'unknown'
    id = IntegerField('MsgId', 0)
    source = StringField('FromUserName')
    target = StringField('ToUserName')
    time = IntegerField('CreateTime', 0)


@register_message('text')
class TextMessage(BaseMessage):
    type = 'text'
    content = StringField('Content')


@register_message('image')
class ImageMessage(BaseMessage):
    type = 'image'
    image = StringField('PicUrl')


@register_message('voice')
class VoiceMessage(BaseMessage):
    type = 'voice'
    media_id = StringField('MediaId')
    format = StringField('Format')
    recognition = StringField('Recognition')


@register_message('video')
class VideoMessage(BaseMessage):
    type = 'video'
    media_id = StringField('MediaId')
    thumb_media_id = StringField('ThumbMediaId')


@register_message('location')
class LocationMessage(BaseMessage):
    type = 'location'
    location_x = StringField('Location_X')
    location_y = StringField('Location_Y')
    scale = StringField('Scale')
    label = StringField('Label')


@register_message('link')
class LinkMessage(BaseMessage):
    type = 'link'
    title = StringField('Title')
    description = StringField('Description')
    url = StringField('Url')


@register_message('event')
class EventMessage(BaseMessage):
    type = StringField('Event')
    key = StringField('EventKey')
    latitude = FloatField('Latitude')
    longitude = FloatField('Longitude')
    precision = FloatField('Precision')
