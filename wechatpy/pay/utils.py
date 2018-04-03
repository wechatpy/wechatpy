# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import base64
import copy
import hashlib
import socket

import six

from wechatpy.utils import to_binary, to_text


def format_url(params, api_key=None):
    data = [to_binary('{0}={1}'.format(k, params[k])) for k in sorted(params) if params[k]]
    if api_key:
        data.append(to_binary('key={0}'.format(api_key)))
    return b"&".join(data)


def calculate_signature(params, api_key):
    url = format_url(params, api_key)
    return to_text(hashlib.md5(url).hexdigest().upper())


def _check_signature(params, api_key):
    _params = copy.deepcopy(params)
    sign = _params.pop('sign', '')
    return sign == calculate_signature(_params, api_key)


def dict_to_xml(d, sign):
    xml = ['<xml>\n']
    for k in sorted(d):
        # use sorted to avoid test error on Py3k
        v = d[k]
        if isinstance(v, six.integer_types) or (isinstance(v, six.string_types) and v.isdigit()):
            xml.append('<{0}>{1}</{0}>\n'.format(to_text(k), to_text(v)))
        else:
            xml.append(
                '<{0}><![CDATA[{1}]]></{0}>\n'.format(to_text(k), to_text(v))
            )
    xml.append('<sign><![CDATA[{0}]]></sign>\n</xml>'.format(to_text(sign)))
    return ''.join(xml)


def get_external_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        wechat_ip = socket.gethostbyname('api.mch.weixin.qq.com')
        sock.connect((wechat_ip, 80))
        addr, port = sock.getsockname()
        sock.close()
        return addr
    except socket.error:
        return '127.0.0.1'


def rsa_encrypt(data, pem):
    """
    加密
    :param data: 待加密字符串
    :param pem: RSA key 内容
    :return:
    """
    encoded_data = data.encode() if not isinstance(data, bytes) else data
    try:
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_OAEP
        rsakey = RSA.importKey(pem)
        cipher = PKCS1_OAEP.new(rsakey)
        encrypted_data = cipher.encrypt(encoded_data)
    except ModuleNotFoundError:
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding

        private_key = serialization.load_pem_private_key(pem, password=None, backend=default_backend())
        encrypted_data = private_key.sign(
            data=encoded_data,
            padding=padding.OAEP(
                mgf=padding.MGF1(hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None,
            ),
            algorithm=hashes.SHA1()
        )
    except ModuleNotFoundError:
        raise ModuleNotFoundError('either crypto or cryptography is required')
    return base64.b64encode(encrypted_data).decode()
