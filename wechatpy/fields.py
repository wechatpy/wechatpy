from __future__ import absolute_import, unicode_literals
import six


class BaseField(object):
    converter = None

    def __init__(self, name, default=None):
        self.name = name
        self.default = default

    def to_xml(self):
        raise NotImplementedError()


class StringField(BaseField):
    converter = six.text_type

    def to_xml(self, value):
        value = self.converter(value)
        tpl = '<{name}>![CDATA[{value}]]</{name}>'
        return tpl.format(name=self.name, value=value)


class IntegerField(BaseField):
    converter = int

    def to_xml(self, value):
        value = self.converter(value) if value else self.default
        tpl = '<{name}>{value}</{name}>'
        return tpl.format(name=self.name, value=value)


class FloatField(BaseField):
    converter = float

    def to_xml(self, value):
        value = self.converter(value) if value else self.default
        tpl = '<{name}>{value}</{name}>'
        return tpl.format(name=self.name, value=value)


class ImageField(StringField):

    def to_xml(self, value):
        value = self.converter(value)
        tpl = '<Image>\n<MediaId>![CDATA[{value}]]</MediaId>\n</Image>'
        return tpl.format(value=value)


class VoiceField(StringField):

    def to_xml(self, value):
        value = self.converter(value)
        tpl = '<Voice>\n<MediaId>![CDATA[{value}]]</MediaId>\n</Voice>'
        return tpl.format(value=value)


class VideoField(StringField):

    def to_xml(self, value):
        media_id = self.converter(value['media_id'])
        if 'title' in value:
            title = self.converter(value['title'])
        if 'description' in value:
            description = self.converter(value['description'])
        tpl = """<Video>
        <MediaId>![CDATA[{media_id}]]</MediaId>
        <Title>![CDATA[{title}]]</Title>
        <Description>![CDATA[{description}]]</Description>
        </Video>
        """
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
        <ThumbMediaId>![CDATA[{thumb_media_id}]]</ThumbMediaId>
        <Title>![CDATA[{title}]]</Title>
        <Description>![CDATA[{description}]]</Description>
        <MusicUrl>![CDATA[{music_url}]]</MusicUrl>
        <HQMusicUrl>![CDATA[{hq_music_url}]]</HQMusicUrl>
        </Music>"""
        return tpl.format(
            thumb_media_id=thumb_media_id,
            title=title,
            description=description,
            music_url=music_url,
            hq_music_url=hq_music_url
        )


class ArticleField(StringField):

    def to_xml(self, articles):
        article_count = len(articles)
        items = []
        for article in articles:
            title = self.converter(article.get('title', ''))
            description = self.converter(article.get('description', ''))
            image = self.converter(article.get('image', ''))
            url = self.converter(article.get('url', ''))
            item_tpl = """<item>
            <Title>![CDATA[{title}]]</Title>
            <Description>![CDATA[{description}]]</Description>
            <PicUrl>![CDATA[{image}]]</PicUrl>
            <Url>![CDATA[{url}]]</Url>
            </item>
            """
            item = item_tpl.format(
                title=title,
                description=description,
                image=image,
                url=url
            )
            items.append(item)
        items_str = '\n'.join(items)
        tpl = """<ArticleCount>{article_count}</ArticleCount>
        <Articles>{items}</Articles>
        """
        return tpl.format(
            article_count=article_count,
            items=items_str
        )
