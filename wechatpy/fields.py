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
        value = self.converter(value)
        tpl = '<{name}>{value}</{name}>'
        return tpl.format(name=self.name, value=value)
