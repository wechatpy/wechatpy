# -*- coding: utf-8 -*-


import base64
import copy
import hashlib
import hmac
import random
import socket
import logging
import string
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA256

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

    encoded_data = to_binary(data)
    pem = to_binary(pem)
    public_key = serialization.load_pem_public_key(pem)
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
    encrypted_data = to_binary(encrypted_data)
    pem = to_binary(pem)
    private_key = serialization.load_pem_private_key(pem, password)
    data = private_key.decrypt(
        encrypted_data,
        padding=padding.OAEP(
            mgf=padding.MGF1(hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None,
        ),
    )
    return data


def calculate_signature_rsa(private_key, request_method, request_path, request_body, timestamp=None, nonce_str=None):
    """
    v3接口 rsa 签名

    :param private_key: RSA private key
    :param request_method: 请求方法
    :param request_path: 请求路径
    :param request_body: 请求内容
    :param timestamp: 时间戳（可选，不填自动当前时间）
    :param nonce_str: 随机字符串（可选，不填自动生成）
    :return: 返回加密并 base64 处理后的 string
    """
    timestamp = timestamp or str(int(time.time()))
    nonce_str = nonce_str or "".join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    data = f"{request_method.upper()}\n{request_path}\n{timestamp}\n{nonce_str}\n{request_body}\n"
    logger.debug("Calculate Signature: %s", data)
    encoded_data = to_binary(data)
    pem = to_binary(private_key)
    public_key = serialization.load_pem_private_key(pem, password=None, backend=default_backend())
    encrypted_data = public_key.sign(encoded_data, padding=padding.PKCS1v15(), algorithm=SHA256())
    encrypted_data = base64.b64encode(encrypted_data)
    return to_text(encrypted_data)


def calculate_pay_params_signature_rsa(private_key, app_id, package, timestamp=None, nonce_str=None):
    """
    v3接口 支付rsa签名

    :param private_key: RSA private key
    :param app_id: 小程序app_id
    :param package: 订单详情扩展字符串
    :param timestamp: 时间戳（可选，不填自动当前时间）
    :param nonce_str: 随机字符串（可选，不填自动生成）
    :return: 返回加密并 base64 处理后的 string
    """
    timestamp = timestamp or str(int(time.time()))
    nonce_str = nonce_str or "".join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    data = f"{app_id}\n{timestamp}\n{nonce_str}\n{package}\n"
    logger.debug("Calculate Signature: %s", data)
    encoded_data = to_binary(data)
    pem = to_binary(private_key)
    public_key = serialization.load_pem_private_key(pem, password=None, backend=default_backend())
    encrypted_data = public_key.sign(encoded_data, padding=padding.PKCS1v15(), algorithm=SHA256())
    encrypted_data = base64.b64encode(encrypted_data)
    return to_text(encrypted_data)


def check_rsa_signature(certificate, timestamp, nonce_str, response_body, signature):
    """
    v3接口 rsa 签名验证
    :param certificate: RSA 证书
    :param timestamp: 时间戳
    :param nonce_str: 随机字符串
    :param response_body: 响应内容
    :param signature: 签名
    """
    sign_str = f"{timestamp}\n{nonce_str}\n{response_body}\n"
    message = sign_str.encode("UTF-8")
    signature = base64.b64decode(signature)
    public_key = certificate.public_key()
    try:
        public_key.verify(signature, message, padding.PKCS1v15(), SHA256())
    except InvalidSignature:
        return False
    return True


def aes_decrypt(nonce, ciphertext, associated_data, apiv3_key):
    key_bytes = to_binary(apiv3_key)
    nonce_bytes = to_binary(nonce)
    associated_data_bytes = to_binary(associated_data)
    data = base64.b64decode(ciphertext)
    aes_gcm = AESGCM(key=key_bytes)
    try:
        result = aes_gcm.decrypt(nonce=nonce_bytes, data=data, associated_data=associated_data_bytes)
    except InvalidTag:
        result = None
    return to_text(result)


def rsa_public_encrypt(data, certificate):
    """
    rsa 加密
    :param data: 待加密字符串/binary
    :param pem: RSA public key 内容/binary
    :param b64_encode: 是否对输出进行 base64 encode
    :return: 如果 b64_encode=True 的话，返回加密并 base64 处理后的 string；否则返回加密后的 binary
    """
    encoded_data = to_binary(data)
    public_key = certificate.public_key()
    encrypted_data = public_key.encrypt(
        encoded_data,
        padding=padding.OAEP(
            mgf=padding.MGF1(hashes.SHA1()),  # skipcq: PTC-W1003
            algorithm=hashes.SHA1(),  # skipcq: PTC-W1003
            label=None,
        ),
    )
    encrypted_data = base64.b64encode(encrypted_data).decode("utf-8")
    return encrypted_data


def get_serial_no(cert_pem):
    serial_no = f"{cert_pem.serial_number:x}".upper()
    return serial_no


def filter_none_values(dict_obj):
    filtered_data = {k: v for k, v in dict_obj.items() if v is not None}
    return filtered_data
