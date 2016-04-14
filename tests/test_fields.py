# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import base64
from datetime import datetime
import unittest

from wechatpy.utils import to_text


class FieldsTestCase(unittest.TestCase):

    def test_string_field_to_xml(self):
        from wechatpy.fields import StringField

        name = 'Content'
        value = 'test'
        expected = '<{name}><![CDATA[{value}]]></{name}>'.format(
            name=name,
            value=value
        )

        field = StringField(name)
        self.assertEqual(expected, field.to_xml(value))

    def test_integer_field_to_xml(self):
        from wechatpy.fields import IntegerField

        name = 'Content'
        value = 0
        expected = '<{name}>{value}</{name}>'.format(
            name=name,
            value=value
        )

        field = IntegerField(name)
        self.assertEqual(expected, field.to_xml(value))

    def test_float_field_to_xml(self):
        from wechatpy.fields import FloatField

        name = 'Content'
        value = 0.0
        expected = '<{name}>{value}</{name}>'.format(
            name=name,
            value=value
        )

        field = FloatField(name)
        self.assertEqual(expected, field.to_xml(value))

    def test_image_field_to_xml(self):
        from wechatpy.fields import ImageField

        value = '123456'
        expected = """<Image>
        <MediaId><![CDATA[{value}]]></MediaId>
        </Image>""".format(
            value=value
        )

        field = ImageField('Image')
        self.assertEqual(expected, field.to_xml(value))

    def test_voice_field_to_xml(self):
        from wechatpy.fields import VoiceField

        value = '123456'
        expected = """<Voice>
        <MediaId><![CDATA[{value}]]></MediaId>
        </Voice>""".format(
            value=value
        )

        field = VoiceField('Voice')
        self.assertEqual(expected, field.to_xml(value))

    def test_video_field_to_xml(self):
        from wechatpy.fields import VideoField

        value = {
            'media_id': '123456',
            'title': 'test',
            'description': 'test'
        }
        expected = """<Video>
        <MediaId><![CDATA[{media_id}]]></MediaId>
        <Title><![CDATA[{title}]]></Title>
        <Description><![CDATA[{description}]]></Description>
        </Video>""".format(
            media_id=value['media_id'],
            title=value['title'],
            description=value['description']
        )

        field = VideoField('Video')
        self.assertEqual(expected, field.to_xml(value))

    def test_music_field_to_xml(self):
        from wechatpy.fields import MusicField

        value = {
            'thumb_media_id': '123456',
            'title': 'test',
            'description': 'test',
            'music_url': '',
            'hq_music_url': ''
        }
        expected = """<Music>
        <ThumbMediaId><![CDATA[{thumb_media_id}]]></ThumbMediaId>
        <Title><![CDATA[{title}]]></Title>
        <Description><![CDATA[{description}]]></Description>
        <MusicUrl><![CDATA[{music_url}]]></MusicUrl>
        <HQMusicUrl><![CDATA[{hq_music_url}]]></HQMusicUrl>
        </Music>""".format(
            thumb_media_id=value['thumb_media_id'],
            title=value['title'],
            description=value['description'],
            music_url=value['music_url'],
            hq_music_url=value['hq_music_url']
        )

        field = MusicField('Music')
        self.assertEqual(expected, field.to_xml(value))

    def test_article_field_to_xml(self):
        from wechatpy.fields import ArticlesField

        articles = [
            {
                'title': 'test 1',
                'description': 'test 1',
                'image': 'http://www.qq.com/1.png',
                'url': 'http://www.qq.com/1'
            },
            {
                'title': 'test 2',
                'description': 'test 2',
                'image': 'http://www.qq.com/2.png',
                'url': 'http://www.qq.com/2'
            },
            {
                'title': 'test 3',
                'description': 'test 3',
                'image': 'http://www.qq.com/3.png',
                'url': 'http://www.qq.com/3'
            },
        ]
        article_count = len(articles)

        field = ArticlesField('Article')
        expected = '<ArticleCount>{article_count}</ArticleCount>'.format(
            article_count=article_count
        )
        assert expected in field.to_xml(articles)

    def test_base64encode_field_to_xml(self):
        from wechatpy.fields import Base64EncodeField

        content = b'test'
        field = Base64EncodeField('Content')
        expected = '<Content><![CDATA[{content}]]></Content>'.format(
            content=to_text(base64.b64encode(content))
        )
        self.assertEqual(expected, field.to_xml(content))

    def test_base64decode_field_to_xml(self):
        from wechatpy.fields import Base64DecodeField

        content = to_text(base64.b64encode(b'test'))
        field = Base64DecodeField('Content')
        expected = '<Content><![CDATA[test]]></Content>'
        self.assertEqual(expected, field.to_xml(content))

    def test_datetime_field_to_xml(self):
        from wechatpy.fields import DateTimeField

        content = 1442401156
        content = datetime.fromtimestamp(content)
        field = DateTimeField('ExpiredTime')
        expected = '<ExpiredTime>1442401156</ExpiredTime>'
        self.assertEqual(expected, field.to_xml(content))
