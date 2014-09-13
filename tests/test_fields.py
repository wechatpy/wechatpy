# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest


class FieldsTestCase(unittest.TestCase):

    def test_string_field_to_xml(self):
        from wechatpy.fields import StringField

        name = 'Content'
        value = 'test'
        expected = '<{name}>![CDATA[{value}]]</{name}>'.format(
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
        <MediaId>![CDATA[{value}]]</MediaId>
        </Image>""".format(
            value=value
        )

        field = ImageField('Image')
        self.assertEqual(expected, field.to_xml(value))

    def test_voice_field_to_xml(self):
        from wechatpy.fields import VoiceField

        value = '123456'
        expected = """<Voice>
        <MediaId>![CDATA[{value}]]</MediaId>
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
        <MediaId>![CDATA[{media_id}]]</MediaId>
        <Title>![CDATA[{title}]]</Title>
        <Description>![CDATA[{description}]]</Description>
        </Video>
        """.format(
            media_id=value['media_id'],
            title=value['title'],
            description=value['description']
        )

        field = VideoField('Video')
        self.assertEqual(expected, field.to_xml(value))
