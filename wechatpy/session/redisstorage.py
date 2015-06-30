# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from wechatpy.session import SessionStorage
from wechatpy._compat import json


class RedisStorage(SessionStorage):

    def __init__(self, redis, prefix='wechatpy'):
        for method_name in ('get', 'set', 'delete'):
            assert hasattr(redis, method_name)
        self.redis = redis
        self.prefix = prefix

    def key_name(self, key):
        return '{0}:{1}'.format(self.prefix, key)

    def get(self, key):
        key = self.key_name(key)
        value = self.redis.get(key)
        if not value:
            return None
        try:
            return json.loads(value)
        except ValueError:
            return value

    def set(self, key, value, ttl=None):
        key = self.key_name(key)
        value = json.dumps(value)
        self.redis.set(key, value, ex=ttl)

    def delete(self, key):
        key = self.key_name(key)
        self.redis.delete(key)
