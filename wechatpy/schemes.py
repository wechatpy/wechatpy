import time
import json
import dataclasses
from typing import Dict, Optional
from dataclasses import dataclass

from wechatpy.utils import random_string


@dataclass
class Scheme:
    def to_dict(self) -> Dict:
        return dataclasses.asdict(self)


@dataclass
class JsApiCardExt(Scheme):
    """本类用于指示 jsapi 中批量添加卡券接口的某个参数格式.

    参数含义: https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/JS-SDK.html#65

    文档中要求本结构应为 JSON 字符串, 因此使用时注意转换:

    .. highlight:: python
    .. code-block:: python

        from wechatpy import WeChatClient
        from wechatpy.schemes import JsApiCardExt

        client = WeChatClient('appid', 'appsecret')
        card_ext = client.jsapi.get_jsapi_add_card_params(
            card_ticket=card_ticket, timestamp=timestamp, card_id=card_id, nonce_str=nonce_str
        )
        card_ext_json = card_ext.to_json()
    """

    signature: str
    code: str = ""
    openid: str = ""
    timestamp: str = ""
    nonce_str: str = ""
    fixed_begintimestamp: Optional[int] = None
    outer_str: str = ""

    def __post_init__(self):
        self.timestamp = self.timestamp or str(int(time.time()))
        self.nonce_str = self.nonce_str or random_string()

    def to_json(self) -> str:
        d = {k: v for k, v in dataclasses.asdict(self).items() if v}
        return json.dumps(d, ensure_ascii=False)
