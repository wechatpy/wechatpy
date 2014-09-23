from __future__ import absolute_import, unicode_literals
import six
from .. import replies


REPLY_TYPES = {}


def register_reply(reply_type):
    def register(cls):
        REPLY_TYPES[reply_type] = cls
        return cls
    return register


@register_reply('text')
class TextReply(replies.TextReply):
    pass


@register_reply('image')
class ImageReply(replies.ImageReply):
    pass


@register_reply('voice')
class VoiceReply(replies.VoiceReply):
    pass


@register_reply('video')
class VideoReply(replies.VideoReply):
    pass


@register_reply('news')
class ArticleReply(replies.ArticleReply):
    pass


def create_reply(reply, message=None, render=False):
    r = None
    if isinstance(reply, replies.BaseReply):
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
        r = ArticleReply(
            message=message,
            articles=reply
        )
    if r and render:
        return r.render()
    return r
