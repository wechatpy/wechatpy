# -*- coding: utf-8 -*-
"""
    wechatpy.oauth
    ~~~~~~~~~~~~~~~

    This module provides OAuth2 library for WeChat

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
try:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)
except ImportError:
    from pkg_resources import declare_namespace
    declare_namespace(__name__)

import six
import requests

from wechatpy.utils import json
from wechatpy.exceptions import WeChatOAuthException


class WeChatOAuth(object):
    """ 微信公众平台 OAuth 网页授权 """

    API_BASE_URL = 'https://api.weixin.qq.com/'
    OAUTH_BASE_URL = 'https://open.weixin.qq.com/connect/'

    def __init__(self, app_id, secret, redirect_uri,
                 scope='snsapi_base', state=''):
        """
        :param app_id: WeChat app id
        :param secret: WeChat app secret
        :param redirect_uri: OAuth2 redirect URI
        :param scope: WeChat OAuth2 scope
        :param state: WeChat OAuth2 state
        """
        self.app_id = app_id
        self.secret = secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.state = state

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

        res = requests.request(
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
        res.encoding = 'UTF-8'
        result = res.json()

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

    @property
    def authorize_url(self):
        """Generate authorize url
        :return: An url
        """
        redirect_uri = six.moves.urllib.parse.quote(self.redirect_uri)
        url_list = [
            self.OAUTH_BASE_URL,
            'oauth2/authorize?appid=',
            self.app_id,
            '&redirect_uri=',
            redirect_uri,
            '&response_type=code&scope=',
            self.scope
        ]
        if self.state:
            url_list.extend(['&state=', self.state])
        url_list.append('#wechat_redirect')
        return ''.join(url_list)

    @property
    def qrconnect_url(self):
        """Generate qrconnect url
        :return: An url
        """
        redirect_uri = six.moves.urllib.parse.quote(self.redirect_uri)
        url_list = [
            self.OAUTH_BASE_URL,
            'qrconnect?appid=',
            self.app_id,
            '&redirect_uri=',
            redirect_uri,
            '&response_type=code&scope=',
            'snsapi_login'  # scope
        ]
        if self.state:
            url_list.extend(['&state=', self.state])
        url_list.append('#wechat_redirect')
        return ''.join(url_list)

    def fetch_access_token(self, code):
        """Fetch OAuth2 access token
        :param code: code argument from url
        :return: JSON data
        """
        res = self._get(
            'sns/oauth2/access_token',
            params={
                'appid': self.app_id,
                'secret': self.secret,
                'code': code,
                'grant_type': 'authorization_code'
            }
        )
        self.access_token = res['access_token']
        self.open_id = res['openid']
        self.refresh_token = res['refresh_token']
        self.expires_in = res['expires_in']
        return res

    def refresh_access_token(self, refresh_token):
        """Refresh OAuth2 access token
        :param refresh_token: OAuth2 refresh token
        :return: JSON data
        """
        res = self._get(
            'sns/oauth2/refresh_token',
            params={
                'appid': self.app_id,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
        )
        self.access_token = res['access_token']
        self.open_id = res['openid']
        self.refresh_token = res['refresh_token']
        self.expires_in = res['expires_in']
        return res

    def get_user_info(self, openid=None, access_token=None, lang='zh_CN'):
        """Get user infomation
        :param openid: WeChat openid, optional
        :param access_token: WeChat OAuth2 access token, optional
        :param lang: Preferred language code, optional
        :return: JSON data
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

    def check_access_token(self, openid=None, access_token=None):
        """Check whether access token is valid or not
        :param openid: WeChat openid, optional
        :param access_token: WeChat OAuth2 access token, optional
        :return: True if valid, else False
        """
        openid = openid or self.open_id
        access_token = access_token or self.access_token
        res = self._get(
            'sns/auth',
            params={
                'access_token': access_token,
                'openid': openid
            }
        )
        if res['errcode'] == 0:
            return True
        return False
