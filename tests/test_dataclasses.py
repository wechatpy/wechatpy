# -*- coding: utf-8 -*-
import unittest
import warnings

from wechatpy.schemes import DataclassesBase
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
        self.assertEqual(a1.a, a)
        self.assertEqual(a1.b, b)
        self.assertEqual(a1.c, c)
        self.assertEqual(a1.d, self.A.d)

    def test_dataclasses_todict(self):
        a = 1
        b = random_string()
        c = {random_string(): random_string()}

        a1 = self.A(a=a, b=b, c=c)
        self.assertDictEqual(a1.dict(), {"a": a, "b": b, "c": c, "d": self.A.d})

    def test_unexpected_key(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            random_key = random_string()

            self.A(a=2, b="asd", c={}, **{random_key: random_string()})
            self.assertEqual(f"Got an unexpected key {random_key}", str(w[-1].message))

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            random_key = random_string()

            a1 = self.A(a=2, b="asd", c={})
            setattr(a1, random_key, random_string())
            self.assertEqual(f"Got an unexpected key {random_key}", str(w[-1].message))

    def test_type_error(self):
        try:
            self.A(a=2, b="asd", c={}, d=2)
        except Exception as e:
            self.assertIn("The type of value of d should be <class 'str'>, but got <class 'int'>", str(e))
        else:
            self.fail("Here shoule be an TypeError, but failed to trigger it")

    def test_set_type_error(self):
        a1 = self.A(a=2, b="asd", c={})
        try:
            a1.d = 2
        except Exception as e:
            self.assertIn("The type of value of d should be <class 'str'>, but got <class 'int'>", str(e))
        else:
            self.fail("Here shoule be an TypeError, but failed to trigger it")

    def test_missing_values(self):
        try:
            self.A(a=2, c={})
        except Exception as e:
            self.assertIn("There are some missing values", str(e))
        else:
            self.fail("Here shoule be an TypeError, but failed to trigger it")
