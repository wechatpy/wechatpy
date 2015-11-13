# -*- coding: utf-8 -*-
"""
    wechatpy.fields
    ~~~~~~~~~~~~~~~~

    This module defines some useful field types for parse WeChat messages

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import time
from datetime import datetime
import base64
import copy

import six

from wechatpy.utils import to_text, to_binary, ObjectDict, timezone


default_timezone = timezone('Asia/Shanghai')


class FieldDescriptor(object):

    def __init__(self, field):
        self.field = field
        self.attr_name = field.name

    def __get__(self, instance, instance_type=None):
        if instance is not None:
            value = instance._data.get(self.attr_name)
            if value is None:
                value = copy.deepcopy(self.field.default)
                instance._data[self.attr_name] = value
            if isinstance(value, dict):
                value = ObjectDict(value)
            if value and not isinstance(value, (dict, list, tuple)) and \
                    six.callable(self.field.converter):
                value = self.field.converter(value)
            return value
        return self.field

    def __set__(self, instance, value):
        instance._data[self.attr_name] = value


class BaseField(object):
    converter = None

    def __init__(self, name, default=None):
        self.name = name
        self.default = default

    def to_xml(self, value):
        raise NotImplementedError()

    def __repr__(self):
        _repr = '{klass}({name})'.format(
            klass=self.__class__.__name__,
            name=repr(self.name)
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)

    def add_to_class(self, klass, name):
        self.klass = klass
        klass._fields[name] = self
        setattr(klass, name, FieldDescriptor(self))


class StringField(BaseField):

    def __to_text(self, value):
        return to_text(value)

    converter = __to_text

    def to_xml(self, value):
        value = self.converter(value)
        tpl = '<{name}><![CDATA[{value}]]></{name}>'
        return tpl.format(name=self.name, value=value)


class IntegerField(BaseField):
    converter = int

    def to_xml(self, value):
        value = self.converter(value) if value is not None else self.default
        tpl = '<{name}>{value}</{name}>'
        return tpl.format(name=self.name, value=value)


class DateTimeField(BaseField):
    def __converter(self, value):
        v = int(value)
        return datetime.fromtimestamp(v, tz=default_timezone)
    converter = __converter

    def to_xml(self, value):
        value = time.mktime(datetime.timetuple(value))
        value = int(value)
        tpl = '<{name}>{value}</{name}>'
        return tpl.format(name=self.name, value=value)


class FloatField(BaseField):
    converter = float

    def to_xml(self, value):
        value = self.converter(value) if value is not None else self.default
        tpl = '<{name}>{value}</{name}>'
        return tpl.format(name=self.name, value=value)


class ImageField(StringField):

    def to_xml(self, value):
        value = self.converter(value)
        tpl = """<Image>
        <MediaId><![CDATA[{value}]]></MediaId>
        </Image>"""
        return tpl.format(value=value)


class VoiceField(StringField):

    def to_xml(self, value):
        value = self.converter(value)
        tpl = """<Voice>
        <MediaId><![CDATA[{value}]]></MediaId>
        </Voice>"""
        return tpl.format(value=value)


class VideoField(StringField):

    def to_xml(self, value):
        media_id = self.converter(value['media_id'])
        if 'title' in value:
            title = self.converter(value['title'])
        if 'description' in value:
            description = self.converter(value['description'])
        tpl = """<Video>
        <MediaId><![CDATA[{media_id}]]></MediaId>
        <Title><![CDATA[{title}]]></Title>
        <Description><![CDATA[{description}]]></Description>
        </Video>"""
        return tpl.format(
            media_id=media_id,
            title=title,
            description=description
        )


class MusicField(StringField):

    def to_xml(self, value):
        thumb_media_id = self.converter(value['thumb_media_id'])
        if 'title' in value:
            title = self.converter(value['title'])
        if 'description' in value:
            description = self.converter(value['description'])
        if 'music_url' in value:
            music_url = self.converter(value['music_url'])
        if 'hq_music_url' in value:
            hq_music_url = self.converter(value['hq_music_url'])
        tpl = """<Music>
        <ThumbMediaId><![CDATA[{thumb_media_id}]]></ThumbMediaId>
        <Title><![CDATA[{title}]]></Title>
        <Description><![CDATA[{description}]]></Description>
        <MusicUrl><![CDATA[{music_url}]]></MusicUrl>
        <HQMusicUrl><![CDATA[{hq_music_url}]]></HQMusicUrl>
        </Music>"""
        return tpl.format(
            thumb_media_id=thumb_media_id,
            title=title,
            description=description,
            music_url=music_url,
            hq_music_url=hq_music_url
        )


class ArticlesField(StringField):

    def to_xml(self, articles):
        article_count = len(articles)
        items = []
        for article in articles:
            title = self.converter(article.get('title', ''))
            description = self.converter(article.get('description', ''))
            image = self.converter(article.get('image', ''))
            url = self.converter(article.get('url', ''))
            item_tpl = """<item>
            <Title><![CDATA[{title}]]></Title>
            <Description><![CDATA[{description}]]></Description>
            <PicUrl><![CDATA[{image}]]></PicUrl>
            <Url><![CDATA[{url}]]></Url>
            </item>"""
            item = item_tpl.format(
                title=title,
                description=description,
                image=image,
                url=url
            )
            items.append(item)
        items_str = '\n'.join(items)
        tpl = """<ArticleCount>{article_count}</ArticleCount>
        <Articles>{items}</Articles>"""
        return tpl.format(
            article_count=article_count,
            items=items_str
        )


class Base64EncodeField(StringField):

    def __base64_encode(self, text):
        return to_text(base64.b64encode(to_binary(text)))

    converter = __base64_encode


class Base64DecodeField(StringField):

    def __base64_decode(self, text):
        return to_text(base64.b64decode(to_binary(text)))

    converter = __base64_decode


class HardwareField(StringField):

    def to_xml(self, value=None):
        value = value or {'view': 'myrank', 'action': 'ranklist'}
        tpl = """<{name}>
        <MessageView><![CDATA[{view}]]></MessageView>
        <MessageAction><![CDATA[{action}]]></MessageAction>
        </{name}>"""
        return tpl.format(
            name=self.name,
            view=value.get('view'),
            action=value.get('action')
        )
