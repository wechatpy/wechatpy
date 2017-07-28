# -*- coding: utf-8 -*-
"""
Define some useful constants
"""
from __future__ import absolute_import, unicode_literals


class ReimburseStatus(object):
    """ 发票报销状态 """
    INIT = 'INVOICE_REIMBURSE_INIT'  # 初始状态，未锁定，可提交报销
    LOCK = 'INVOICE_REIMBURSE_LOCK'  # 已锁定，无法重复提交报销
    CLOSURE = 'INVOICE_REIMBURSE_CLOSURE'  # 已核销，从用户卡包中移除

    @classmethod
    def values(cls):
        return {cls.INIT, cls.LOCK, cls.CLOSURE}
