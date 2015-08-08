# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.session import SessionStorage


class ShoveStorage(SessionStorage):

    def __init__(self, shove, prefix='wechatpy'):
        self.shove = shove
        self.prefix = prefix

    def key_name(self, key):
        return '{0}:{1}'.format(self.prefix, key)

    def get(self, key, default=None):
        key = self.key_name(key)
        try:
            return self.shove[key]
        except KeyError:
            return default

    def set(self, key, value, ttl=None):
        if value is None:
            return

        key = self.key_name(key)
        self.shove[key] = value

    def delete(self, key):
        key = self.key_name(key)
        try:
            del self.shove[key]
        except KeyError:
            pass
