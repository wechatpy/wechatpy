# -*- coding: utf-8 -*-


import base64
import copy
import hashlib
import hmac
import socket
import logging

from wechatpy.utils import to_binary, to_text

logger = logging.getLogger(__name__)


def format_url(params, api_key=None):
    data = [to_binary(f"{k}={params[k]}") for k in sorted(params) if params[k]]
    if api_key:
        data.append(to_binary(f"key={api_key}"))
    return b"&".join(data)


def calculate_signature(params, api_key):
    url = format_url(params, api_key)
    logger.debug("Calculate Signature URL: %s", url)
    return to_text(hashlib.md5(url).hexdigest().upper())


def calculate_signature_hmac(params, api_key):
    url = format_url(params, api_key)
    sign = to_text(hmac.new(api_key.encode(), msg=url, digestmod=hashlib.sha256).hexdigest().upper())
    return sign


def _check_signature(params, api_key):
    _params = copy.deepcopy(params)
    sign = _params.pop("sign", "")
    return sign == calculate_signature(_params, api_key)


def dict_to_xml(d, sign=None):
    xml = ["<xml>\n"]
    for k in sorted(d):
        # use sorted to avoid test error on Py3k
        v = d[k]
        if isinstance(v, int) or (isinstance(v, str) and v.isdigit()):
            xml.append(f"<{to_text(k)}>{to_text(v)}</{to_text(k)}>\n")
        else:
            xml.append(f"<{to_text(k)}><![CDATA[{to_text(v)}]]></{to_text(k)}>\n")
    if sign:
        xml.append(f"<sign><![CDATA[{to_text(sign)}]]></sign>\n</xml>")
    else:
        xml.append("</xml>")
    return "".join(xml)


def get_external_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        wechat_ip = socket.gethostbyname("api.mch.weixin.qq.com")
        sock.connect((wechat_ip, 80))
        addr, port = sock.getsockname()
        sock.close()
        return addr
    except socket.error:
        return "127.0.0.1"


def rsa_encrypt(data, pem, b64_encode=True):
    """
    rsa 加密
    :param data: 待加密字符串/binary
    :param pem: RSA public key 内容/binary
    :param b64_encode: 是否对输出进行 base64 encode
    :return: 如果 b64_encode=True 的话，返回加密并 base64 处理后的 string；否则返回加密后的 binary
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding

    encoded_data = to_binary(data)
    pem = to_binary(pem)
    public_key = serialization.load_pem_public_key(pem, backend=default_backend())
    encrypted_data = public_key.encrypt(
        encoded_data,
        padding=padding.OAEP(
            mgf=padding.MGF1(hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None,
        ),
    )
    if b64_encode:
        encrypted_data = base64.b64encode(encrypted_data).decode("utf-8")
    return encrypted_data


def rsa_decrypt(encrypted_data, pem, password=None):
    """
    rsa 解密
    :param encrypted_data: 待解密 bytes
    :param pem: RSA private key 内容/binary
    :param password: RSA private key pass phrase
    :return: 解密后的 binary
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding

    encrypted_data = to_binary(encrypted_data)
    pem = to_binary(pem)
    private_key = serialization.load_pem_private_key(pem, password, backend=default_backend())
    data = private_key.decrypt(
        encrypted_data,
        padding=padding.OAEP(
            mgf=padding.MGF1(hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None,
        ),
    )
    return data
