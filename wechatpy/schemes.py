from pydantic import BaseModel
from time import time
from wechatpy.utils import random_string
from json import dumps


class JsapiCardExt(BaseModel):
    """本类用于指示 jsapi 中批量添加卡券接口的某个参数格式.

    文档中要求本结构应为 JSON 字符串, 因此使用时注意转换.
    参数含义: https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/JS-SDK.html#65
    """
    code: str = ""
    openid: str = ""
    timestamp: str = ""
    nonce_str: str = ""
    fixed_begintimestamp: int = None
    outer_str: str = ""
    signature: str

    def __init__(self, **data):
        super().__init__(**data)
        self.timestamp = self.timestamp or str(int(time.time()))
        self.nonce_str = self.nonce_str or random_string()

    def __str__(self):
        ret = {}
        for key in self.__dict__:
            if not key.startswith("__") and self.__dict__[key]:
                ret[key] = self.__dict__[key]
        return dumps(ret)

    def dump(self):
        return self.__str__()
