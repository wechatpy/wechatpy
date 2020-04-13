# -*- coding: utf-8 -*-
import base64
import unittest
from datetime import datetime

import xmltodict

from wechatpy.utils import to_text


class FieldsTestCase(unittest.TestCase):
    def test_string_field_to_xml(self):
        from wechatpy.fields import StringField

        name = "Content"
        value = "test"
        expected = f"<{name}><![CDATA[{value}]]></{name}>"

        field = StringField(name)
        self.assertEqual(expected, field.to_xml(value))

    def test_integer_field_to_xml(self):
        from wechatpy.fields import IntegerField

        name = "Content"
        value = 0
        expected = f"<{name}>{value}</{name}>"

        field = IntegerField(name)
        self.assertEqual(expected, field.to_xml(value))

    def test_float_field_to_xml(self):
        from wechatpy.fields import FloatField

        name = "Content"
        value = 0.0
        expected = f"<{name}>{value}</{name}>"

        field = FloatField(name)
        self.assertEqual(expected, field.to_xml(value))

    def test_image_field_to_xml(self):
        from wechatpy.fields import ImageField

        value = "123456"
        expected = f"""<Image>
        <MediaId><![CDATA[{value}]]></MediaId>
        </Image>"""

        field = ImageField("Image")
        self.assertEqual(expected, field.to_xml(value))

    def test_voice_field_to_xml(self):
        from wechatpy.fields import VoiceField

        value = "123456"
        expected = f"""<Voice>
        <MediaId><![CDATA[{value}]]></MediaId>
        </Voice>"""

        field = VoiceField("Voice")
        self.assertEqual(expected, field.to_xml(value))

    def test_video_field_to_xml(self):
        from wechatpy.fields import VideoField

        value = {"media_id": "123456", "title": "test", "description": "test"}
        expected = f"""<Video>
        <MediaId><![CDATA[{value["media_id"]}]]></MediaId>
        <Title><![CDATA[{value["title"]}]]></Title>
        <Description><![CDATA[{value["description"]}]]></Description>
        </Video>"""

        field = VideoField("Video")
        self.assertXMLEqual(expected, field.to_xml(value))

    def test_music_field_to_xml(self):
        from wechatpy.fields import MusicField

        value = {
            "thumb_media_id": "123456",
            "title": "test",
            "description": "test",
            "music_url": "",
            "hq_music_url": "",
        }
        expected = f"""<Music>
        <ThumbMediaId><![CDATA[{value["thumb_media_id"]}]]></ThumbMediaId>
        <Title><![CDATA[{value["title"]}]]></Title>
        <Description><![CDATA[{value["description"]}]]></Description>
        <MusicUrl><![CDATA[{value["music_url"]}]]></MusicUrl>
        <HQMusicUrl><![CDATA[{value["hq_music_url"]}]]></HQMusicUrl>
        </Music>"""

        field = MusicField("Music")
        self.assertXMLEqual(expected, field.to_xml(value))

    def test_article_field_to_xml(self):
        from wechatpy.fields import ArticlesField

        articles = [
            {
                "title": "test 1",
                "description": "test 1",
                "image": "http://www.qq.com/1.png",
                "url": "http://www.qq.com/1",
            },
            {
                "title": "test 2",
                "description": "test 2",
                "image": "http://www.qq.com/2.png",
                "url": "http://www.qq.com/2",
            },
            {
                "title": "test 3",
                "description": "test 3",
                "image": "http://www.qq.com/3.png",
                "url": "http://www.qq.com/3",
            },
        ]
        article_count = len(articles)

        field = ArticlesField("Article")
        expected = f"<ArticleCount>{article_count}</ArticleCount>"
        self.assertIn(expected, field.to_xml(articles))

    def test_base64encode_field_to_xml(self):
        from wechatpy.fields import Base64EncodeField

        content = b"test"
        field = Base64EncodeField("Content")
        expected = f"<Content><![CDATA[{to_text(base64.b64encode(content))}]]></Content>"
        self.assertEqual(expected, field.to_xml(content))

    def test_base64decode_field_to_xml(self):
        from wechatpy.fields import Base64DecodeField

        content = to_text(base64.b64encode(b"test"))
        field = Base64DecodeField("Content")
        expected = "<Content><![CDATA[test]]></Content>"
        self.assertEqual(expected, field.to_xml(content))

    def test_datetime_field_to_xml(self):
        from wechatpy.fields import DateTimeField

        content = 1442401156
        content = datetime.fromtimestamp(content)
        field = DateTimeField("ExpiredTime")
        expected = "<ExpiredTime>1442401156</ExpiredTime>"
        self.assertEqual(expected, field.to_xml(content))

    def assertXMLEqual(self, expected, xml):
        expected = xmltodict.unparse(xmltodict.parse(expected))
        xml = xmltodict.unparse(xmltodict.parse(xml))
        self.assertEqual(expected, xml)
