from __future__ import absolute_import, unicode_literals
import time
import copy
import six

from .fields import BaseField, StringField, IntegerField, ImageField
from .fields import VoiceField, VideoField, MusicField, ArticlesField
from .messages import BaseMessage
from .utils import ObjectDict, to_text, to_binary


REPLY_TYPES = {}


def register_reply(reply_type):
    def register(cls):
        REPLY_TYPES[reply_type] = cls
        return cls
    return register


class ReplyMetaClass(type):
    """Metaclass for all repies"""
    def __new__(cls, name, bases, attrs):
        super_new = super(ReplyMetaClass, cls).__new__
        # six.with_metaclass() inserts an extra class called 'NewBase' in the
        # inheritance tree: BaseReply -> NewBase -> object. But the
        # initialization should be executed only once for a given model class.

        # attrs will never be empty for classes declared in the standard way
        # (ie. with the `class` keyword). This is quite robust.
        if name == 'NewBase' and attrs == {}:
            return super_new(cls, name, bases, attrs)

        # Ensure initialization is only performed for subclasses of
        # BaseReply excluding BaseReply class itself
        parents = [b for b in bases if isinstance(b, ReplyMetaClass) and
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


class BaseReply(six.with_metaclass(ReplyMetaClass)):
    source = StringField('FromUserName')
    target = StringField('ToUserName')
    time = IntegerField('CreateTime', int(time.time()))
    type = 'unknown'

    def __init__(self, **kwargs):
        message = kwargs.pop('message', None)
        if message and isinstance(message, BaseMessage):
            if 'source' not in kwargs:
                kwargs['source'] = message.target
            if 'target' not in kwargs:
                kwargs['target'] = message.source
            if hasattr(message, 'agent') and 'agent' not in kwargs:
                kwargs['agent'] = message.agent
        for name, field in self._fields.items():
            if name == 'time' and 'time' not in kwargs:
                # set CreateTime to current timestamp if time not present
                value = int(time.time())
            else:
                value = kwargs.pop(name, field.default)
                if value is not None and six.callable(field.converter):
                    value = field.converter(value)
            setattr(self, name, value)
        if kwargs:
            # unknown arguments
            args = ', '.join(kwargs.keys())
            raise AttributeError('Unknown argument(s): {args}'.format(
                args=args
            ))

    def render(self):
        tpl = '<xml>\n{data}\n</xml>'
        nodes = []
        msg_type = '<MsgType><![CDATA[{msg_type}]]></MsgType>'.format(
            msg_type=self.type
        )
        nodes.append(msg_type)
        for name, field in self._fields.items():
            value = getattr(self, name, field.default)
            node_xml = field.to_xml(value)
            nodes.append(node_xml)
        data = '\n'.join(nodes)
        return tpl.format(data=data)

    def __str__(self):
        if six.PY2:
            return to_binary(self.render())
        else:
            return to_text(self.render())


@register_reply('text')
class TextReply(BaseReply):
    type = 'text'
    content = StringField('Content')


@register_reply('image')
class ImageReply(BaseReply):
    type = 'image'
    image = ImageField('Image')

    @property
    def media_id(self):
        return self.image

    @media_id.setter
    def media_id(self, value):
        self.image = value


@register_reply('voice')
class VoiceReply(BaseReply):
    type = 'voice'
    voice = VoiceField('Voice')

    @property
    def media_id(self):
        return self.voice

    @media_id.setter
    def media_id(self, value):
        self.voice = value


@register_reply('video')
class VideoReply(BaseReply):
    type = 'video'
    video = VideoField('Video', {})

    @property
    def media_id(self):
        if not isinstance(self.video, dict):
            self.video = {}
        return self.video.get('media_id', None)

    @media_id.setter
    def media_id(self, value):
        if not isinstance(self.video, dict):
            self.video = {}
        self.video['media_id'] = value

    @property
    def title(self):
        if not isinstance(self.video, dict):
            self.video = {}
        return self.video.get('title', None)

    @title.setter
    def title(self, value):
        if not isinstance(self.video, dict):
            self.video = {}
        self.video['title'] = value

    @property
    def description(self):
        if not isinstance(self.video, dict):
            self.video = {}
        return self.video.get('description', None)

    @description.setter
    def description(self, value):
        if not isinstance(self.video, dict):
            self.video = {}
        self.video['description'] = value


@register_reply('music')
class MusicReply(BaseReply):
    type = 'music'
    music = MusicField('Music', {})

    @property
    def thumb_media_id(self):
        if not isinstance(self.music, dict):
            self.music = {}
        return self.music.get('thumb_media_id', None)

    @thumb_media_id.setter
    def thumb_media_id(self, value):
        if not isinstance(self.music, dict):
            self.music = {}
        self.music['thumb_media_id'] = value

    @property
    def title(self):
        if not isinstance(self.music, dict):
            self.music = {}
        return self.music.get('title', None)

    @title.setter
    def title(self, value):
        if not isinstance(self.music, dict):
            self.music = {}
        self.music['title'] = value

    @property
    def description(self):
        if not isinstance(self.music, dict):
            self.music = {}
        return self.music.get('description', None)

    @description.setter
    def description(self, value):
        if not isinstance(self.music, dict):
            self.music = {}
        self.music['description'] = value

    @property
    def music_url(self):
        if not isinstance(self.music, dict):
            self.music = {}
        return self.music.get('music_url', None)

    @music_url.setter
    def music_url(self, value):
        if not isinstance(self.music, dict):
            self.music = {}
        self.music['music_url'] = value

    @property
    def hq_music_url(self):
        if not isinstance(self.music, dict):
            self.music = {}
        return self.music.get('hq_music_url', None)

    @hq_music_url.setter
    def hq_music_url(self, value):
        if not isinstance(self.music, dict):
            self.music = {}
        self.music['hq_music_url'] = value


@register_reply('news')
class ArticlesReply(BaseReply):
    type = 'news'
    articles = ArticlesField('Articles', [])

    def add_article(self, article):
        if not self.articles or not isinstance(self.articles, list):
            self.articles = []
        if len(self.articles) == 10:
            raise AttributeError("Can't add more than 10 articles"
                                 " in an ArticlesReply")
        self.articles.append(article)


@register_reply('transfer_customer_service')
class TransferCustomerServiceReply(BaseReply):
    type = 'transfer_customer_service'


def create_reply(reply, message=None, render=False):
    r = None
    if isinstance(reply, BaseReply):
        r = reply
    elif isinstance(reply, six.string_types):
        r = TextReply(
            message=message,
            content=reply
        )
    elif isinstance(reply, (tuple, list)):
        if len(reply) > 10:
            raise AttributeError("Can't add more than 10 articles"
                                 " in an ArticlesReply")
        r = ArticlesReply(
            message=message,
            articles=reply
        )
    if r and render:
        return r.render()
    return r
