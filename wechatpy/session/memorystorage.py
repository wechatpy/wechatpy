# -*- coding: utf-8 -*-

from wechatpy.session import SessionStorage


class MemoryStorage(SessionStorage):
    def __init__(self):
        self._data = {}

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value, ttl=None):
        if value is None:
            return
        self._data[key] = value

    def delete(self, key):
        self._data.pop(key, None)
