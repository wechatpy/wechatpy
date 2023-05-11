import hmac
import base64
import hashlib
import logging
import traceback
import datetime
from urllib.parse import urlencode
from dateutil import parser
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from wechatpy.utils import to_binary, to_text

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def iso8601_parse_date(iso8601_string):
    if isinstance(iso8601_string, int):
        iso8601_string = str(iso8601_string)
    _datetime = parser.parse(iso8601_string)
    _datetime = _datetime.replace(tzinfo=None)
    return _datetime


def date_parse_iso8601(date):
    if isinstance(date, datetime.datetime):
        return date.strftime('%Y%m%d%H%M%S')
    else:
        logger.warning('请传入 datetime.datetime 类型的日期')


def build_request_sign_str(method, endpoint, timestamp, nonce_str, request_body_or_data=None, meta=None) -> str:
    """build_request_sign_str
    构造签名串

    https://wechatpay-api.gitbook.io/wechatpay-api-v3/qian-ming-zhi-nan-1/qian-ming-sheng-cheng
    :param method: HTTP请求方法
    :param endpoint: URL 路径
    :param timestamp: 请求时间戳
    :param nonce_str: 请求随机串
    :param request_body_or_data: 请求报文主体，当请求方法为POST或PUT时，请使用真实发送的JSON报文，请求方法为GET时，报文主体为空
    :param meta: 图片上传API，请使用meta对应的JSON报文
    :rtype: str
    """
    _method = method.upper()
    if _method == 'GET':
        endpoint += '?' + urlencode(request_body_or_data)
    if not endpoint.startswith('/'):
        endpoint = '/' + endpoint
    sign_str = ''
    sign_str += method.upper() + '\n'
    sign_str += endpoint + '\n'
    sign_str += timestamp + '\n'
    sign_str += nonce_str + '\n'
    if meta:
        sign_str += meta + '\n'
    elif _method == 'GET':
        sign_str += '\n'
    elif _method == 'POST' or _method == 'PUT':
        if not isinstance(request_body_or_data, str):
            raise TypeError('request_body should be str')
        else:
            sign_str += request_body_or_data + '\n'
    else:
        raise TypeError('method invalid')
    return sign_str


def build_response_sign_str(timestamp, nonce_str, response_body) -> str:
    """build_response_sign_str
    构造验签名串

    https://wechatpay-api.gitbook.io/wechatpay-api-v3/qian-ming-zhi-nan-1/qian-ming-yan-zheng
    :param timestamp: 应答时间戳
    :param nonce_str: 应答随机串
    :param response_body: 应答报文主体
    :rtype: str
    """
    sign_str = ''
    sign_str += timestamp + '\n'
    sign_str += nonce_str + '\n'
    sign_str += response_body + '\n'
    logger.debug('sign_str:' + sign_str)
    return sign_str


def calculate_signature_hmac(api_key, signature_string):
    signature = to_text(hmac.new(api_key.encode(), msg=signature_string.encode('utf-8'), digestmod=hashlib.sha256).hexdigest().upper())
    return signature


def calculate_signature_rsa(sign_str, mch_key):
    sign_str = to_binary(sign_str)
    with open(mch_key, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    signature = private_key.sign(
        sign_str,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    signature = base64.b64encode(signature).decode('utf-8')
    return signature


def check_signature_rsa(public_key, signature, message):
    message = to_binary(message)
    signature = base64.b64decode(signature)
    try:
        public_key.verify(
            signature,
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    except:
        logger.warning(traceback.format_exc())
        return False
    return True


def decrypt(apiv3_key, nonce, ciphertext, associated_data):
    key_bytes = to_binary(apiv3_key)
    nonce_bytes = to_binary(nonce)
    ad_bytes = to_binary(associated_data)
    data = base64.b64decode(ciphertext)
    aesgcm = AESGCM(key_bytes)
    return aesgcm.decrypt(nonce_bytes, data, ad_bytes)


def get_public_key(cert_pem):
    public_key = cert_pem.public_key()
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise TypeError('cert explortion failed')
    return public_key


def get_serial_no(cert_pem):
    serial_no = '{0:x}'.format(cert_pem.serial_number).upper()
    return serial_no
