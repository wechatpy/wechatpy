# -*- coding: utf-8 -*-
import json

from wechatpy.pay.utils import aes_decrypt
from wechatpy.utils import to_text


def parse_message(apiv3_key, content):
    if not content:
        return {}
    message = json.loads(to_text(content))

    # 解密数据
    resource = message.get("resource")
    if resource.get("algorithm") == "AEAD_AES_256_GCM":
        nonce = resource.get("nonce")
        ciphertext = resource.get("ciphertext")
        associated_data = resource.get("associated_data")
        encrypt_data = aes_decrypt(nonce, ciphertext, associated_data, apiv3_key)
        message["decrypt_data"] = encrypt_data
    return message
