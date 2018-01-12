# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import copy
import hashlib
import socket
import xml.etree.ElementTree as ElementTree

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
        if isinstance(v, six.integer_types) or v.isdigit():
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


def dict2xml(data):
    # return to_text( xmltodict.unparse({'xml': data_dict}, pretty=True) )
    root = ElementTree.Element('xml')
    for k in data:
        v = data[k]
        child = ElementTree.SubElement(root, k)
        child.text = str(v)
    return to_text(ElementTree.tostring(root, encoding='utf-8'))


def xml2dict(xml_str):
    # return xmltodict.parse(xml_str)['xml']
    root = ElementTree.fromstring(xml_str)
    assert to_text(root.tag) == to_text('xml')
    result = {}
    for child in root:
        tag = child.tag
        text = child.text
        result[tag] = text
    return result
