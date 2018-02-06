# -*- coding: utf-8 -*-
"""
    wechatpy.component
    ~~~~~~~~~~~~~~~

    This module provides client library for WeChat Open Platform

    :copyright: (c) 2015 by hunter007.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals

import logging
import time

import requests
import six
import xmltodict
from six.moves.urllib.parse import quote

from wechatpy.client import WeChatComponentClient
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import APILimitedException, WeChatClientException, WeChatOAuthException
from wechatpy.fields import DateTimeField, StringField
from wechatpy.messages import MessageMetaClass
from wechatpy.session.memorystorage import MemoryStorage
from wechatpy.utils import get_querystring, json, to_binary, to_text

logger = logging.getLogger(__name__)


class BaseComponentMessage(six.with_metaclass(MessageMetaClass)):
    """Base class for all component messages and events"""
    type = 'unknown'
    appid = StringField('AppId')
    create_time = DateTimeField('CreateTime')

    def __init__(self, message):
        self._data = message

    def __repr__(self):
        _repr = "{klass}({msg})".format(
            klass=self.__class__.__name__,
            msg=repr(self._data)
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)


class ComponentVerifyTicketMessage(BaseComponentMessage):
    """
    component_verify_ticket协议
    """
    type = 'component_verify_ticket'
    verify_ticket = StringField('ComponentVerifyTicket')


class ComponentUnauthorizedMessage(BaseComponentMessage):
    """
    取消授权通知
    """
    type = 'unauthorized'
    authorizer_appid = StringField('AuthorizerAppid')


class BaseWeChatComponent(object):

    _http = requests.Session()

    API_BASE_URL = 'https://api.weixin.qq.com/cgi-bin'

    def __init__(self,
                 component_appid,
                 component_appsecret,
                 component_token,
                 encoding_aes_key,
                 session=None):
        """
        :param component_appid: 第三方平台appid
        :param component_appsecret: 第三方平台appsecret
        :param component_token: 公众号消息校验Token
        :param encoding_aes_key: 公众号消息加解密Key
        """
        self.component_appid = component_appid
        self.component_appsecret = component_appsecret
        self.expires_at = None
        self.crypto = WeChatCrypto(
            component_token, encoding_aes_key, component_appid)
        self.session = session or MemoryStorage()

        if isinstance(session, six.string_types):
            from shove import Shove
            from wechatpy.session.shovestorage import ShoveStorage

            querystring = get_querystring(session)
            prefix = querystring.get('prefix', ['wechatpy'])[0]

            shove = Shove(session)
            storage = ShoveStorage(shove, prefix)
            self.session = storage

    @property
    def component_verify_ticket(self):
        return self.session.get('component_verify_ticket')

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = '{base}{endpoint}'.format(
                base=api_base_url,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        if 'params' not in kwargs:
            kwargs['params'] = {}
        if isinstance(kwargs['params'], dict) and \
                'component_access_token' not in kwargs['params']:
            kwargs['params'][
                'component_access_token'] = self.access_token
        if isinstance(kwargs['data'], dict):
            kwargs['data'] = json.dumps(kwargs['data'])

        res = self._http.request(
            method=method,
            url=url,
            **kwargs
        )
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise WeChatClientException(
                errcode=None,
                errmsg=None,
                client=self,
                request=reqe.request,
                response=reqe.response
            )

        return self._handle_result(res, method, url, **kwargs)

    def _handle_result(self, res, method=None, url=None, **kwargs):
        result = json.loads(res.content.decode('utf-8', 'ignore'), strict=False)
        if 'errcode' in result:
            result['errcode'] = int(result['errcode'])

        if 'errcode' in result and result['errcode'] != 0:
            errcode = result['errcode']
            errmsg = result['errmsg']
            if errcode == 42001:
                logger.info('Component access token expired, fetch a new one and retry request')
                self.fetch_access_token()
                kwargs['params']['component_access_token'] = self.session.get(
                    'component_access_token'
                )
                return self._request(
                    method=method,
                    url_or_endpoint=url,
                    **kwargs
                )
            elif errcode == 45009:
                # api freq out of limit
                raise APILimitedException(
                    errcode,
                    errmsg,
                    client=self,
                    request=res.request,
                    response=res
                )
            else:
                raise WeChatClientException(
                    errcode,
                    errmsg,
                    client=self,
                    request=res.request,
                    response=res
                )

        return result

    def fetch_access_token(self):
        """
        获取 component_access_token
        详情请参考 https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list\
        &t=resource/res_list&verify=1&id=open1419318587&token=&lang=zh_CN

        :return: 返回的 JSON 数据包
        """
        url = '{0}{1}'.format(
            self.API_BASE_URL,
            '/component/api_component_token'
        )
        return self._fetch_access_token(
            url=url,
            data=json.dumps({
                'component_appid': self.component_appid,
                'component_appsecret': self.component_appsecret,
                'component_verify_ticket': self.component_verify_ticket
            })
        )

    def _fetch_access_token(self, url, data):
        """ The real fetch access token """
        logger.info('Fetching component access token')
        res = self._http.post(
            url=url,
            data=data
        )
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise WeChatClientException(
                errcode=None,
                errmsg=None,
                client=self,
                request=reqe.request,
                response=reqe.response
            )
        result = res.json()
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatClientException(
                result['errcode'],
                result['errmsg'],
                client=self,
                request=res.request,
                response=res
            )

        expires_in = 7200
        if 'expires_in' in result:
            expires_in = result['expires_in']
        self.session.set(
            'component_access_token',
            result['component_access_token'],
            expires_in
        )
        self.expires_at = int(time.time()) + expires_in
        return result

    @property
    def access_token(self):
        """ WeChat component access token """
        access_token = self.session.get('component_access_token')
        if access_token:
            if not self.expires_at:
                # user provided access_token, just return it
                return access_token

            timestamp = time.time()
            if self.expires_at - timestamp > 60:
                return access_token

        self.fetch_access_token()
        return self.session.get('component_access_token')

    def get(self, url, **kwargs):
        return self._request(
            method='get',
            url_or_endpoint=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self._request(
            method='post',
            url_or_endpoint=url,
            **kwargs
        )


class WeChatComponent(BaseWeChatComponent):

    def create_preauthcode(self):
        """
        获取预授权码
        """
        return self.post(
            '/component/api_create_preauthcode',
            data={
                'component_appid': self.component_appid
            }
        )

    def query_auth(self, authorization_code):
        """
        使用授权码换取公众号的授权信息

        :params authorization_code: 授权code,会在授权成功时返回给第三方平台，详见第三方平台授权流程说明
        """
        return self.post(
            '/component/api_query_auth',
            data={
                'component_appid': self.component_appid,
                'authorization_code': authorization_code
            }
        )

    def refresh_authorizer_token(
            self, authorizer_appid, authorizer_refresh_token):
        """
        获取（刷新）授权公众号的令牌

        :params authorizer_appid: 授权方appid
        :params authorizer_refresh_token: 授权方的刷新令牌
        """
        return self.post(
            '/component/api_authorizer_token',
            data={
                'component_appid': self.component_appid,
                'authorizer_appid': authorizer_appid,
                'authorizer_refresh_token': authorizer_refresh_token
            }
        )

    def get_authorizer_info(self, authorizer_appid):
        """
        获取授权方的账户信息

        :params authorizer_appid: 授权方appid
        """
        return self.post(
            '/component/api_get_authorizer_info',
            data={
                'component_appid': self.component_appid,
                'authorizer_appid': authorizer_appid,
            }
        )

    def get_authorizer_option(self, authorizer_appid, option_name):
        """
        获取授权方的选项设置信息

        :params authorizer_appid: 授权公众号appid
        :params option_name: 选项名称
        """
        return self.post(
            '/component/api_get_authorizer_option',
            data={
                'component_appid': self.component_appid,
                'authorizer_appid': authorizer_appid,
                'option_name': option_name
            }
        )

    def set_authorizer_option(
            self, authorizer_appid, option_name, option_value):
        """
        设置授权方的选项信息

        :params authorizer_appid: 授权公众号appid
        :params option_name: 选项名称
        :params option_value: 设置的选项值
        """
        return self.post(
            '/component/api_set_authorizer_option',
            data={
                'component_appid': self.component_appid,
                'authorizer_appid': authorizer_appid,
                'option_name': option_name,
                'option_value': option_value
            }
        )

    def get_client_by_authorization_code(self, authorization_code):
        """
        通过授权码直接获取 Client 对象

        :params authorization_code: 授权code,会在授权成功时返回给第三方平台，详见第三方平台授权流程说明
        """
        result = self.query_auth(authorization_code)
        access_token = result['authorization_info']['authorizer_access_token']
        refresh_token = result['authorization_info']['authorizer_refresh_token']  # NOQA
        authorizer_appid = result['authorization_info']['authorizer_appid']  # noqa
        return WeChatComponentClient(
            authorizer_appid, self, access_token, refresh_token,
            session=self.session
        )

    def get_client_by_appid(self, authorizer_appid):
        """
        通过 authorizer_appid 获取 Client 对象

        :params authorizer_appid: 授权公众号appid
        """
        access_token_key = '{0}_access_token'.format(authorizer_appid)
        refresh_token_key = '{0}_refresh_token'.format(authorizer_appid)
        access_token = self.session.get(access_token_key)
        refresh_token = self.session.get(refresh_token_key)

        if not access_token:
            ret = self.refresh_authorizer_token(
                authorizer_appid,
                refresh_token
            )
            access_token = ret['authorizer_access_token']
            refresh_token = ret['authorizer_refresh_token']

        return WeChatComponentClient(
            authorizer_appid,
            self,
            access_token,
            refresh_token,
            session=self.session
        )

    def cache_component_verify_ticket(self, msg, signature, timestamp, nonce):
        """
        处理 wechat server 推送的 component_verify_ticket消息

        :params msg: 加密内容
        :params signature: 消息签名
        :params timestamp: 时间戳
        :params nonce: 随机数
        """
        content = self.crypto.decrypt_message(msg, signature, timestamp, nonce)
        message = xmltodict.parse(to_text(content))['xml']
        o = ComponentVerifyTicketMessage(message)
        self.session.set(o.type, o.verify_ticket, 1200)

    def get_unauthorized(self, msg, signature, timestamp, nonce):
        """
        处理取消授权通知

        :params msg: 加密内容
        :params signature: 消息签名
        :params timestamp: 时间戳
        :params nonce: 随机数
        """
        content = self.crypto.decrypt_message(msg, signature, timestamp, nonce)
        message = xmltodict.parse(to_text(content))['xml']
        return ComponentUnauthorizedMessage(message)


class ComponentOAuth(object):
    """ 微信开放平台 代公众号 OAuth 网页授权

    详情请参考
    https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&id=open1419318590
    """

    _http = requests.Session()

    API_BASE_URL = 'https://api.weixin.qq.com/'
    OAUTH_BASE_URL = 'https://open.weixin.qq.com/connect/'

    def __init__(self, app_id, component_appid, component_access_token, redirect_uri, scope='snsapi_base', state=''):
        """

        :param app_id: 微信公众号 app_id
        :param component_appid: 服务方的appid
        :param component_access_token: 服务方的access_token
        :param redirect_uri: 重定向地址，需要urlencode，这里填写的应是服务开发方的回调地址
        :param scope: 可选，微信公众号 OAuth2 scope，默认为 ``snsapi_base``
        :param state: 可选，重定向后会带上state参数，开发者可以填写任意参数值，最多128字节
        """
        self.app_id = app_id
        self.component_appid = component_appid
        self.component_access_token = component_access_token
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.state = state

    @property
    def authorize_url(self):
        """ 获取授权跳转地址

        严格按照以下格式，包括顺序和大小写，并请将参数替换为实际内容。
        https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&
        response_type=code&scope=SCOPE&state=STATE&component_appid=component_appid#wechat_redirect

        :return: URL 地址
        """
        redirect_uri = quote(self.redirect_uri, safe='')
        url_list = [
            self.OAUTH_BASE_URL,
            'oauth2/authorize?appid=',
            self.app_id,
            '&redirect_uri=',
            redirect_uri,
            '&response_type=code&scope=',
            self.scope,
        ]
        if self.state:
            url_list.extend(['&state=', self.state])
        url_list.extend([
            '&component_appid=',
            self.component_appid,
        ])
        url_list.append('#wechat_redirect')
        return ''.join(url_list)

    def fetch_access_token(self, code):
        """获取 access_token

        :param code: 授权完成跳转回来后 URL 中的 code 参数
        :return: JSON 数据包
        """
        res = self._get(
            'sns/oauth2/component/access_token',
            params={
                'appid': self.app_id,
                'component_appid': self.component_appid,
                'component_access_token': self.component_access_token,
                'code': code,
                'grant_type': 'authorization_code',
            }
        )
        self.access_token = res['access_token']
        self.open_id = res['openid']
        self.refresh_token = res['refresh_token']
        self.expires_in = res['expires_in']
        self.scope = res['scope']
        return res

    def refresh_access_token(self, refresh_token):
        """刷新 access token

        :param refresh_token: OAuth2 refresh token
        :return: JSON 数据包
        """
        res = self._get(
            'sns/oauth2/component/refresh_token',
            params={
                'appid': self.app_id,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'component_appid': self.component_appid,
                'component_access_token': self.component_access_token,
            }
        )
        self.access_token = res['access_token']
        self.open_id = res['openid']
        self.refresh_token = res['refresh_token']
        self.expires_in = res['expires_in']
        self.scope = res['scope']
        return res

    def get_user_info(self, openid=None, access_token=None, lang='zh_CN'):
        """ 获取用户基本信息（需授权作用域为snsapi_userinfo）

        如果网页授权作用域为snsapi_userinfo，则此时开发者可以通过access_token和openid拉取用户信息了。

        :param openid: 可选，微信 openid，默认获取当前授权用户信息
        :param access_token: 可选，access_token，默认使用当前授权用户的 access_token
        :param lang: 可选，语言偏好, 默认为 ``zh_CN``
        :return: JSON 数据包
        """
        openid = openid or self.open_id
        access_token = access_token or self.access_token
        return self._get(
            'sns/userinfo',
            params={
                'access_token': access_token,
                'openid': openid,
                'lang': lang
            }
        )

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            url = '{base}{endpoint}'.format(
                base=self.API_BASE_URL,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        if isinstance(kwargs.get('data', ''), dict):
            body = json.dumps(kwargs['data'], ensure_ascii=False)
            body = body.encode('utf-8')
            kwargs['data'] = body

        res = self._http.request(
            method=method,
            url=url,
            **kwargs
        )
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise WeChatOAuthException(
                errcode=None,
                errmsg=None,
                client=self,
                request=reqe.request,
                response=reqe.response
            )
        result = json.loads(res.content.decode('utf-8', 'ignore'), strict=False)

        if 'errcode' in result and result['errcode'] != 0:
            errcode = result['errcode']
            errmsg = result['errmsg']
            raise WeChatOAuthException(
                errcode,
                errmsg,
                client=self,
                request=res.request,
                response=res
            )

        return result

    def _get(self, url, **kwargs):
        return self._request(
            method='get',
            url_or_endpoint=url,
            **kwargs
        )
