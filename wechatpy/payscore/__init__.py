import time
import json
import inspect
import logging
import traceback

import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import datetime
from urllib.parse import urlparse

from wechatpy.utils import random_string
from wechatpy.exceptions import WeChatPayScoreException
from . base import BaseWeChatPayScoreAPI
from . utils import (
    calculate_signature_rsa, check_signature_rsa, decrypt, get_serial_no, get_public_key, build_request_sign_str, build_response_sign_str
)
from . import api


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _is_api_endpoint(obj):
    return isinstance(obj, BaseWeChatPayScoreAPI)


class WeChatPayscore(object):
    """
    微信支付分接口

    :param appid: 小程序 appid
    :param apiv3_key: apiv3 密钥
    :param mch_id: 商户号
    :param wechatpay_cert: 必填，微信支付平台证书路径(若不存在会自动创建并下载证书)
    :param mch_cert: 必填，商户证书路径
    :param mch_key: 必填，商户证书私钥路径
    :param service_id: 必填，支付分服务 id
    :param timeout: 可选，请求超时时间，单位秒，默认无超时设置
    """

    payscore = api.PayScore()
    payafter = api.PayAfter()
    """支付分接口"""

    API_BASE_URL = 'https://api.mch.weixin.qq.com/'

    def __new__(cls, *args, **kwargs):
        self = super(WeChatPayscore, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, _api in api_endpoints:
            api_cls = type(_api)
            _api = api_cls(self)
            setattr(self, name, _api)
        return self

    def __init__(self, appid, mch_id, apiv3_key, wechatpay_cert, service_id, mch_cert, mch_key, timeout=None):
        self.appid = appid
        self.apiv3_key = apiv3_key
        self.wechatpay_cert = wechatpay_cert
        self.service_id = service_id
        self.mch_id = mch_id
        self.mch_cert = mch_cert
        self.mch_key = mch_key
        self.timeout = timeout
        self._sandbox_api_key = None
        self._http = requests.Session()
        self._mch_cert_pem = None
        self._wechatpay_cert_pem = None

    def _handle_result(self, response):
        response.encoding = 'utf-8'
        try:
            data = response.json()
            logger.debug('Response from WeChat API \n %s' % (data))
            return data
        except:
            logger.debug('WeChat payment result json parsing error', exc_info=True)
            logger.warning(traceback.format_exc())

    def _request_apiv3(self, method, url_or_endpoint, wechatpay_serial=None, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = '{base}{endpoint}'.format(
                base=api_base_url,
                endpoint=url_or_endpoint
            )
            endpoint = url_or_endpoint
        else:
            url = url_or_endpoint
            endpoint = urlparse(url).path
        if isinstance(kwargs.get('data', ''), dict):
            data = kwargs.pop('data')
            data.setdefault('service_id', self.service_id)
            data.setdefault('appid', self.appid)
            if method.upper() == 'GET':
                kwargs['params'] = data
            else:
                data = json.dumps(data)
                kwargs['data'] = data

        nonce_str = random_string(32)
        timestamp = str(int(time.time()))
        sign_str = build_request_sign_str(method, endpoint, timestamp, nonce_str, data)
        signature = calculate_signature_rsa(sign_str, self.mch_key)
        algorithm = 'WECHATPAY2-SHA256-RSA2048'
        mch_serial = get_serial_no(self.mch_cert_pem)
        authorization = '{algorithm} mchid="{mchid}",nonce_str="{nonce_str}",signature="{signature}",timestamp="{timestamp}",serial_no="{mch_serial}"'.format(
            algorithm=algorithm,
            mchid=self.mch_id,
            nonce_str=nonce_str,
            signature=signature,
            timestamp=timestamp,
            mch_serial=mch_serial,
        )
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': authorization,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        if wechatpay_serial:
            headers['Wechatpay-Serial'] = wechatpay_serial

        kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        logger.info('Request to WeChat API: \n%s \n%s\n%s', method, url, kwargs)
        response = self._http.request(
            method=method,
            url=url,
            headers=headers,
            **kwargs
        )
        try:
            response.raise_for_status()
        except requests.RequestException as reqe:
            logger.debug(reqe)
            raise WeChatPayScoreException(
                return_code=response.status_code,
                errmsg=response.json().get('message'),
                errcode=response.json().get('code'),
                client=self,
                request=reqe.request,
                response=reqe.response
            )
        return response

    def get(self, url, **kwargs):
        return self._handle_request(
            method='get',
            url_or_endpoint=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self._handle_request(
            method='post',
            url_or_endpoint=url,
            **kwargs
        )

    def _handle_request(self, method, url_or_endpoint, **kwargs):
        """_handle_request
        为了保证更换过程中不影响 API 的使用，请求和应答的 HTTP 头部中包括证书序列号，以声明签名或者加密所用的密钥对和证书。

        :param method:
        :param url_or_endpoint:
        :param **kwargs:
        """
        wechatpay_serial = get_serial_no(self.wechatpay_cert_pem)
        logger.debug('wechatpay_serial is: %s' % wechatpay_serial)
        response = self._request_apiv3(
            method=method,
            url_or_endpoint=url_or_endpoint,
            wechatpay_serial=wechatpay_serial,
            **kwargs
        )
        if not self.check_signature(response=response):
            raise TypeError('Response signature verification failed')
        return self._handle_result(response)

    def check_serial_no(self, headers, cert_pem):
        wechatpay_serial = get_serial_no(cert_pem)
        wechatpay_headers_serial = headers.get('Wechatpay-Serial')
        if wechatpay_serial != wechatpay_headers_serial:
            logger.error('serial 验证失败，收到假冒消息或证书错误，多次异常可尝试手动更新证书')
            raise TypeError('Invalid certificate')
        return True

    def check_signature(self, response=None, request=None, cert_pem=None):
        if not cert_pem:
            cert_pem = self.wechatpay_cert_pem
        if response:
            headers = response.headers
            body = response.text
        elif request:
            headers = request.headers
            body = request.get_data().decode('utf-8')
        self.check_serial_no(headers, cert_pem)
        wechatpay_timestamp = headers.get('Wechatpay-Timestamp')
        wechatpay_signature = headers.get('Wechatpay-Signature')
        wechatpay_nonce = headers.get('Wechatpay-Nonce')
        sign_str = build_response_sign_str(wechatpay_timestamp, wechatpay_nonce, body)
        public_key = get_public_key(cert_pem)
        if not check_signature_rsa(public_key, wechatpay_signature, sign_str):
            return False
        return True

    @property
    def mch_cert_pem(self):
        if self._mch_cert_pem is None:
            with open(self.mch_cert, 'rb') as _file:
                self._mch_cert_pem = x509.load_pem_x509_certificate(_file.read(), default_backend())
        return self._mch_cert_pem

    @property
    def wechatpay_cert_pem(self):
        '''
        查询和下载平台证书工具
        如果证书不存在，则下载证书并储存；如果证书已存在，则检查有效性

        微信支付会不定期的更换平台证书，建议更换周期为一年，证书有效期五年
        https://wechatpay-api.gitbook.io/wechatpay-api-v3/chang-jian-wen-ti/zheng-shu-xiang-guan
        '''
        if self._wechatpay_cert_pem is None:
            '''export cert'''
            import os
            cert_path, cert_name = os.path.split(self.wechatpay_cert)
            if not os.path.exists(self.wechatpay_cert):
                if not os.path.exists(cert_path):
                    os.makedirs(cert_path)
                self._wechatpay_cert_pem = self.download_wechatpay_cert()
            else:
                with open(self.wechatpay_cert, 'rb') as _file:
                    cert_pem = x509.load_pem_x509_certificate(_file.read(), default_backend())
                    # 失效替换（有效期：五年）
                    if cert_pem.not_valid_after < datetime.datetime.now() + datetime.timedelta(days=30):
                        logger.warn('平台证书一个月后失效，自动更换')
                        self._wechatpay_cert_pem = self.download_wechatpay_cert()
                    else:
                        self._wechatpay_cert_pem = cert_pem
                    # 例行替换（周期：一年）实际并没有，若想定期更新，只需移动或删除已有的证书即可，会自动下载更新
                    #  time_regular_update = cert_pem.not_valid_before + datetime.timedelta(days=366)
                    #  if time_regular_update < datetime.datetime.now():
                    #      logger.warn('远端平台证书例行更换，自动更新本地证书')
                    #      self._wechatpay_cert_pem = self.download_wechatpay_cert()
        return self._wechatpay_cert_pem

    def download_wechatpay_cert(self):
        """download_wechatpay_cert
        证书下载和验证
        通过下载的证书对下载证书的响应验签
        """
        response = self._request_apiv3(
            method='get',
            url_or_endpoint='v3/certificates',
        )
        certificates = response.json()
        encrypt_data = certificates.get('data')[0].get('encrypt_certificate')
        associated_data = encrypt_data.get('associated_data')
        nonce = encrypt_data.get('nonce')
        algorithm = encrypt_data.get('algorithm')
        ciphertext = encrypt_data.get('ciphertext')
        wechatpay_cert = decrypt(self.apiv3_key, nonce, ciphertext, associated_data)
        cert_pem = x509.load_pem_x509_certificate(wechatpay_cert, default_backend())
        if self.check_signature(response=response, cert_pem=cert_pem):
            with open(self.wechatpay_cert, "wb") as f:
                f.write(cert_pem.public_bytes(serialization.Encoding.PEM))
        else:
            raise TypeError('新下载的证书签名验证失败')
        return cert_pem
