from time import time
from wechatpy.utils import random_string
from json import dumps
import warnings


class DataclassesBase:
    def __init__(self, **data):
        annotations = self.__annotations__.copy() if hasattr(self, "__annotations__") else {}
        for key, value in data.items():
            if key in annotations:
                if isinstance(value, annotations[key]):
                    self.__dict__[key] = value
                    annotations.pop(key)
                else:
                    raise TypeError(
                        "The type of value of %s should be %s, but got %s" % (key, annotations[key], type(value))
                    )
            else:
                warnings.warn("Got an unexpected key %s" % key)

        for annotation in annotations:
            error_msg = []
            if not hasattr(self, annotation):
                error_msg.append("\tname: %s, type: %s" % (annotation, annotations[annotation]))

            if error_msg:
                raise NameError("There are some missing values\n" + "\n\b".join(error_msg))


class JsapiCardExt(DataclassesBase):
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
