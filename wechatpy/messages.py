from __future__ import absolute_import, unicode_literals
import copy
from xml.etree import ElementTree
import six

from .fields import BaseField, StringField, IntegerField, FloatField
from .utils import ObjectDict


MESSAGE_TYPES = {}


def register_message(type):
    def register(cls):
        MESSAGE_TYPES[type] = cls
        return cls
    return register


class MessageMetaClass(type):
    """Metaclass for all messages"""
    def __new__(cls, name, bases, attrs):
        super_new = super(MessageMetaClass, cls).__new__
        # Ensure initialization is only performed for subclasses of
        # BaseMessage excluding BaseMessage class itself
        parents = [b for b in bases if isinstance(b, MessageMetaClass)]
        if not parents:
            return super_new(cls, name, bases, attrs)
        # Create the class
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        setattr(new_class, '_fields', ObjectDict())

        # Add all attributes to the class
        for obj_name, obj in attrs.items():
            if isinstance(obj, BaseField):
                new_class._fields[obj_name] = obj
            else:
                setattr(new_class, obj_name, obj)
        # Add the fields inherited from parent classes
        for parent in parents:
            for obj_name, obj in parent.__dict__.items():
                if isinstance(obj, BaseField):
                    new_class._fields[obj_name] = copy.deepcopy(obj)
        return new_class


class BaseMessage(six.with_metaclass(MessageMetaClass)):
    type = 'unknown'
    id = IntegerField('MsgId', 0)
    source = StringField('FromUserName')
    target = StringField('ToUserName')
    time = IntegerField('CreateTime', 0)

    def __init__(self, message):
        for name, field in self._fields.items():
            value = message.get(field.name, field.default)
            if value and field.converter:
                value = field.converter(value)
            setattr(self, name, value)


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
    latitude = FloatField('Latitude', 0.0)
    longitude = FloatField('Longitude', 0.0)
    precision = FloatField('Precision', 0.0)


class UnknownMessage(BaseMessage):
    pass


def parse_message(xml):
    if not xml:
        return
    to_text = six.text_type
    parser = ElementTree.fromstring(xml)
    message = dict((child.tag, to_text(child.text)) for child in parser)
    message_type = message['MsgType'].lower()
    message_class = MESSAGE_TYPES.get(message_type, UnknownMessage)
    return message_class(message)
