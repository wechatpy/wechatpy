from __future__ import absolute_import, unicode_literals
import copy
import six

from .fields import BaseField, StringField, IntegerField, FieldDescriptor
from .utils import to_text, to_binary


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
            if not hasattr(b, '_fields'):
                continue

            for k, v in b.__dict__.items():
                if k in attrs:
                    continue
                if isinstance(v, FieldDescriptor):
                    attrs[k] = copy.deepcopy(v.field)

        cls = super(MessageMetaClass, cls).__new__(cls, name, bases, attrs)
        cls._fields = {}

        for name, field in cls.__dict__.items():
            if isinstance(field, BaseField):
                field.add_to_class(cls, name)
        return cls


class BaseMessage(six.with_metaclass(MessageMetaClass)):
    type = 'unknown'
    id = IntegerField('MsgId', 0)
    source = StringField('FromUserName')
    target = StringField('ToUserName')
    time = IntegerField('CreateTime', 0)

    def __init__(self, message):
        self._data = message

    def __repr__(self):
        _repr = "{klass}({msg})".format(
            klass=self.__class__.__name__,
            msg=repr(self._data)
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)


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

    @property
    def location(self):
        return self.location_x, self.location_y


@register_message('link')
class LinkMessage(BaseMessage):
    type = 'link'
    title = StringField('Title')
    description = StringField('Description')
    url = StringField('Url')


class UnknownMessage(BaseMessage):
    pass
