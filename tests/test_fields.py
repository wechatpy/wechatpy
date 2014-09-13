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
