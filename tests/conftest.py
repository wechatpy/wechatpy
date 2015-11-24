# -*- coding: utf-8 -*-
import sys


def pytest_ignore_collect(path, config):
    if 'asyncio' in str(path):
        if sys.version_info < (3, 4, 0):
            return True
