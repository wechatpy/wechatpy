from __future__ import absolute_import, unicode_literals
import hashlib
from xml.etree import ElementTree
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


class XMLList(list):

    def __init__(self, xml):
        if isinstance(xml, six.string_types):
            xml = ElementTree.fromstring(xml)
        for element in xml:
            if len(element):
                if len(element) == 1 or element[0].tag != element[1].tag:
                    # treat like dict
                    self.append(XMLDict(element))
                elif element[0].tag == element[1].tag:
                    # treat like list
                    self.append(XMLList(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(to_text(text))


class XMLDict(dict):

    def __init__(self, parent_element):
        if isinstance(parent_element, six.string_types):
            parent_element = ElementTree.fromstring(parent_element)
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if len(element):
                if len(element) == 1 or element[0].tag != element[1].tag:
                    # treat like dict - we assume that if the first two tags
                    # in a series are different, then they are all different.
                    _dict = XMLDict(element)
                else:
                    # treat like list - we assume that if the first two tags
                    # in a series are the same, then the rest are the same.
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    _dict = {element[0].tag: XMLList(element)}
                if element.items():
                    _dict.update(dict(element.items()))
                self.update({element.tag: _dict})
            elif element.items():
                # this assumes that if you've got an attribute in a tag,
                # you won't be having any text. This may or may not be a
                # good idea -- time will tell. It works for the way we are
                # currently doing XML configuration files...
                self.update({element.tag: dict(element.items())})
            else:
                # finally, if there are no child tags and no attributes,
                # extract the text
                self.update({element.tag: to_text(element.text)})


class WeChatCardSigner(object):

    def __init__(self):
        self._data = []

    def add_data(self, data):
        self._data.append(to_binary(data))

    def get_signature(self):
        self._data.sort()
        str_to_sign = b''.join(self._data)
        return hashlib.sha1(str_to_sign).hexdigest()
