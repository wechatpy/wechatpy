from __future__ import absolute_import, unicode_literals
import copy
import six

from .fields import BaseField, StringField, IntegerField
from .utils import ObjectDict, to_text, to_binary


MESSAGE_TYPES = {}


def register_message(msg_type):
    def register(cls):
        MESSAGE_TYPES[msg_type] = cls
        return cls
    return register


class MessageMetaClass(type):
    """Metaclass for all messages"""
    def __new__(cls, name, bases, attrs):  # NOQA
        super_new = super(MessageMetaClass, cls).__new__
        # six.with_metaclass() inserts an extra class called 'NewBase' in the
        # inheritance tree: BaseMessage -> NewBase -> object.
        # But the initialization
        # should be executed only once for a given message class

        # attrs will never be empty for classes declared in the standard way
        # (ie. with the `class` keyword). This is quite robust.
        if name == 'NewBase' and attrs == {}:
            return super_new(cls, name, bases, attrs)
        # Ensure initialization is only performed for subclasses of
        # BaseMessage excluding BaseMessage class itself
        parents = [b for b in bases if isinstance(b, MessageMetaClass) and
                   not (b.__name__ == 'NewBase' and b.__mro__ == (b, object))]
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

            if hasattr(parent, '_fields') and isinstance(parent._fields, dict):
                for field_name, field in parent._fields.items():
                    if isinstance(field, BaseField):
                        new_class._fields[field_name] = copy.deepcopy(field)

        return new_class


class BaseMessage(six.with_metaclass(MessageMetaClass)):
    type = 'unknown'
    id = IntegerField('MsgId', 0)
    source = StringField('FromUserName')
    target = StringField('ToUserName')
    time = IntegerField('CreateTime', 0)

    def __init__(self, message):
        self._message = message
        for name, field in self._fields.items():
            value = message.get(field.name, field.default)
            if value and six.callable(field.converter):
                value = field.converter(value)
            setattr(self, name, value)

    def __repr__(self):
        _repr = "{klass}({msg})".format(
            klass=self.__class__.__name__,
            msg=repr(self._message)
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
