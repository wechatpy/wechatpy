from __future__ import absolute_import, unicode_literals
import hashlib
import six


class ObjectDict(dict):

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


def check_signature(token, signature, timestamp, nonce):
    tmparr = [token, timestamp, nonce]
    tmparr.sort()
    tmpstr = ''.join(tmparr)
    tmpstr = to_binary(tmpstr)
    digest = hashlib.sha1(tmpstr).hexdigest()
    if digest != signature:
        from .exceptions import InvalidSignatureException

        raise InvalidSignatureException()


def to_text(value, encoding='utf-8'):
    if not value:
        return ''
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def to_binary(value, encoding='utf-8'):
    if not value:
        return b''
    if isinstance(value, six.binary_type):
        return value
    if isinstance(value, six.text_type):
        return value.encode(encoding)
    return six.binary_type(value)


class WeChatCardSigner(object):

    def __init__(self):
        self._data = []

    def add_data(self, data):
        self._data.append(to_binary(data))

    def get_signature(self):
        self._data.sort()
        str_to_sign = b''.join(self._data)
        return hashlib.sha1(str_to_sign).hexdigest()
