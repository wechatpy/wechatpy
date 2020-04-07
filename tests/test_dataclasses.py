# -*- coding: utf-8 -*-
import unittest
from wechatpy.schemes import DataclassesBase
import warnings
from wechatpy.utils import random_string


class DataclassesBaseTestCase(unittest.TestCase):
    class A(DataclassesBase):
        a: int
        b: str
        c: dict
        d: str = "2"

    def test_dataclasses_init(self):
        a = 1
        b = random_string()
        c = {random_string(): random_string()}

        a1 = self.A(a=a, b=b, c=c)
        assert a1.a == a
        assert a1.b == b
        assert a1.c == c
        assert a1.d == self.A.d

    def test_unexpected_key(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            random_key = random_string()

            self.A(a=2, b="asd", c={}, **{random_key: random_string()})
            assert "Got an unexpected key %s" % random_key == str(w[-1].message)

    def test_type_error(self):
        try:
            self.A(a=2, b="asd", c={}, d=2)
        except Exception as e:
            assert "The type of value of d should be <class 'str'>, but got <class 'int'>" in str(e)
        else:
            assert "Here shoule be an TypeError, but failed to trigger it" and False

    def test_missing_values(self):
        try:
            self.A(a=2, c={})
        except Exception as e:
            assert "There are some missing values" in str(e)
        else:
            assert "Here shoule be an NameError, but failed to trigger it" and False
