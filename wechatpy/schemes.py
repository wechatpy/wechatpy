import warnings
from json import dumps
from time import time
from typing import Any, Text
from dataclasses import dataclass

from wechatpy.utils import random_string


@dataclass
class JsapiCardExt:
    """本类用于指示 jsapi 中批量添加卡券接口的某个参数格式.

    文档中要求本结构应为 JSON 字符串, 因此使用时注意转换.
    参数含义: https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/JS-SDK.html#65
    """

    signature: str
    code: str = ""
    openid: str = ""
    timestamp: str = ""
    nonce_str: str = ""
    fixed_begintimestamp: int = None
    outer_str: str = ""

    def __post_init__(self):
        self.timestamp = self.timestamp or str(int(time()))
        self.nonce_str = self.nonce_str or random_string()

    def dict(self):
        ret = {}
        for key in self.__dict__:
            if not key.startswith("__") and self.__dict__[key]:
                ret[key] = self.__dict__[key]
        return ret

    def __str__(self):
        return dumps(self.dict())

    def dump(self):
        return self.__str__()
