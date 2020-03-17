# -*- coding: utf-8 -*-
"""
    wechatpy.messages
    ~~~~~~~~~~~~~~~~~~

    This module defines all the messages you can get from WeChat server

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
import copy

from wechatpy.fields import (
    BaseField,
    StringField,
    IntegerField,
    DateTimeField,
    FieldDescriptor,
)


MESSAGE_TYPES = {}


def register_message(msg_type):
    def register(cls):
        MESSAGE_TYPES[msg_type] = cls
        return cls

    return register


class MessageMetaClass(type):
    """Metaclass for all messages"""

    def __new__(cls, name, bases, attrs):
        for b in bases:
            if not hasattr(b, "_fields"):
                continue

            for k, v in b.__dict__.items():
                if k in attrs:
                    continue
                if isinstance(v, FieldDescriptor):
                    attrs[k] = copy.deepcopy(v.field)

        cls = super().__new__(cls, name, bases, attrs)
        cls._fields = {}

        for name, field in cls.__dict__.items():
            if isinstance(field, BaseField):
                field.add_to_class(cls, name)
        return cls


class BaseMessage(metaclass=MessageMetaClass):
    """Base class for all messages and events"""

    type = "unknown"
    id = IntegerField("MsgId", 0)
    source = StringField("FromUserName")
    target = StringField("ToUserName")
    create_time = DateTimeField("CreateTime")
    time = IntegerField("CreateTime")

    def __init__(self, message):
        self._data = message

    def __repr__(self):
        _repr = "{klass}({msg})".format(klass=self.__class__.__name__, msg=repr(self._data))
        return _repr


@register_message("text")
class TextMessage(BaseMessage):
    """
    文本消息
    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_standard_messages.html
    """

    type = "text"
    content = StringField("Content")


@register_message("image")
class ImageMessage(BaseMessage):
    """
    图片消息
    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_standard_messages.html
    """

    type = "image"
    media_id = StringField("MediaId")
    image = StringField("PicUrl")


@register_message("voice")
class VoiceMessage(BaseMessage):
    """
    语音消息
    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_standard_messages.html
    """

    type = "voice"
    media_id = StringField("MediaId")
    format = StringField("Format")
    recognition = StringField("Recognition")


@register_message("shortvideo")
class ShortVideoMessage(BaseMessage):
    """
    短视频消息
    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_standard_messages.html
    """

    type = "shortvideo"
    media_id = StringField("MediaId")
    thumb_media_id = StringField("ThumbMediaId")


@register_message("video")
class VideoMessage(BaseMessage):
    """
    视频消息
    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_standard_messages.html
    """

    type = "video"
    media_id = StringField("MediaId")
    thumb_media_id = StringField("ThumbMediaId")


@register_message("location")
class LocationMessage(BaseMessage):
    """
    地理位置消息
    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_standard_messages.html
    """

    type = "location"
    location_x = StringField("Location_X")
    location_y = StringField("Location_Y")
    scale = StringField("Scale")
    label = StringField("Label")

    @property
    def location(self):
        return self.location_x, self.location_y


@register_message("link")
class LinkMessage(BaseMessage):
    """
    链接消息
    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_standard_messages.html
    """

    type = "link"
    title = StringField("Title")
    description = StringField("Description")
    url = StringField("Url")


class UnknownMessage(BaseMessage):
    """未知消息类型"""

    pass
