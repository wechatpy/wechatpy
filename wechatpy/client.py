from __future__ import absolute_import, unicode_literals
import time
import datetime
import requests
import six

from ._compat import json
from .utils import to_text
from .exceptions import WeChatClientException


class BaseWeChatClient(object):

    API_BASE_URL = ''

    def __init__(self, access_token=None):
        self._access_token = access_token
        self.expires_at = None

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            url = '{base}{endpoint}'.format(
                base=self.API_BASE_URL,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        if 'params' not in kwargs:
            kwargs['params'] = {}
        if 'access_token' not in kwargs['params']:
            kwargs['params']['access_token'] = self.access_token
        if isinstance(kwargs.get('data', ''), dict):
            body = json.dumps(kwargs['data'], ensure_ascii=False)
            body = body.encode('utf-8')
            kwargs['data'] = body

        res = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        res.raise_for_status()
        result = res.json()

        if 'errcode' in result and result['errcode'] != 0:
            if result['errcode'] == 42001:
                # access_token expired, fetch a new one and retry request
                self.fetch_access_token()
                return self._request(
                    method=method,
                    url=url,
                    **kwargs
                )
            else:
                raise WeChatClientException(
                    result['errcode'],
                    result['errmsg']
                )

        return result

    def _get(self, url, **kwargs):
        return self._request(
            method='get',
            url_or_endpoint=url,
            **kwargs
        )

    def _post(self, url, **kwargs):
        return self._request(
            method='post',
            url_or_endpoint=url,
            **kwargs
        )

    def _fetch_access_token(self, url, params):
        """ The real fetch access token """
        res = requests.get(
            url=url,
            params=params
        )
        result = res.json()
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatClientException(result['errcode'], result['errmsg'])

        self._access_token = result['access_token']
        expires_in = 7200
        if 'expires_in' in result:
            expires_in = result['expires_in']
        self.expires_at = int(time.time()) + expires_in
        return result

    def fetch_access_token(self):
        raise NotImplementedError()

    @property
    def access_token(self):
        if self._access_token:
            if not self.expires_at:
                # user provided access_token, just return it
                return self._access_token

            timestamp = time.time()
            if self.expires_at - timestamp > 60:
                return self._access_token

        self.fetch_access_token()
        return self._access_token


class WeChatClient(BaseWeChatClient):

    API_BASE_URL = 'https://api.weixin.qq.com/cgi-bin/'

    def __init__(self, appid, secret, access_token=None):
        self.appid = appid
        self.secret = secret
        self._access_token = access_token
        self.expires_at = None

    def fetch_access_token(self):
        """ Fetch access token"""
        return self._fetch_access_token(
            url='https://api.weixin.qq.com/cgi-bin/token',
            params={
                'grant_type': 'client_credential',
                'appid': self.appid,
                'secret': self.secret
            }
        )

    def send_text_message(self, user_id, content):
        return self._post(
            'message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'text',
                'text': {'content': content}
            }
        )

    def send_image_message(self, user_id, media_id):
        return self._post(
            'message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'image',
                'image': {
                    'media_id': media_id
                }
            }
        )

    def send_voice_message(self, user_id, media_id):
        return self._post(
            'message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'voice',
                'voice': {
                    'media_id': media_id
                }
            }
        )

    def send_video_message(self, user_id, media_id,
                           title=None, description=None):
        video_data = {
            'media_id': media_id,
        }
        if title:
            video_data['title'] = title
        if description:
            video_data['description'] = description

        return self._post(
            'message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'video',
                'video': video_data
            }
        )

    def send_music_message(self, user_id, url, hq_url, thumb_media_id,
                           title=None, description=None):
        music_data = {
            'musicurl': url,
            'hqmusicurl': hq_url,
            'thumb_media_id': thumb_media_id
        }
        if title:
            music_data['title'] = title
        if description:
            music_data['description'] = description

        return self._post(
            'message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'music',
                'music': music_data
            }
        )

    def send_articles_message(self, user_id, articles):
        articles_data = []
        for article in articles:
            articles_data.append({
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'picurl': article['image']
            })
        return self._post(
            'message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'news',
                'news': {
                    'articles': articles_data
                }
            }
        )

    def create_menu(self, menu_data):
        return self._post(
            'menu/create',
            data=menu_data
        )

    def get_menu(self):
        try:
            return self._get('menu/get')
        except WeChatClientException as e:
            if e.errcode == 46003:
                # menu not exist
                return None
            else:
                raise e

    def delete_menu(self):
        return self._get('menu/delete')

    def update_menu(self, menu_data):
        self.delete_menu()
        return self.create_menu(menu_data)

    def upload_media(self, media_type, media_file):
        return self._post(
            url='http://file.api.weixin.qq.com/cgi-bin/media/upload',
            params={
                'access_token': self.access_token,
                'type': media_type
            },
            files={
                'media': media_file
            }
        )

    def download_media(self, media_id):
        return requests.get(
            'http://file.api.weixin.qq.com/cgi-bin/media/get',
            params={
                'access_token': self.access_token,
                'media_id': media_id
            }
        )

    def upload_video(self, media_id, title, description):
        return self._post(
            url='https://file.api.weixin.qq.com/cgi-bin/media/uploadvideo',
            params={
                'access_token': self.access_token
            },
            data={
                'media_id': media_id,
                'title': title,
                'description': description
            }
        )

    def create_group(self, name):
        name = to_text(name)
        return self._post(
            'groups/create',
            data={'group': {'name': name}}
        )

    def get_groups(self):
        return self._get('groups/get')

    def get_group_by_user_id(self, user_id):
        return self._post(
            'groups/getid',
            data={'openid': user_id}
        )

    def update_group(self, group_id, name):
        name = to_text(name)
        return self._post(
            'groups/update',
            data={
                'group': {
                    'id': int(group_id),
                    'name': name
                }
            }
        )

    def move_user(self, user_id, group_id):
        return self._post(
            'groups/members/update',
            data={
                'openid': user_id,
                'to_groupid': group_id
            }
        )

    def get_user_info(self, user_id, lang='zh_CN'):
        assert lang in ('zh_CN', 'zh_TW', 'en'), 'lang can only be one of \
            zh_CN, zh_TW, en language codes'
        return self._get(
            'user/info',
            params={
                'openid': user_id,
                'lang': lang
            }
        )

    def get_followers(self, first_user_id=None):
        params = {}
        if first_user_id:
            params['next_openid'] = first_user_id
        return self._get(
            'user/get',
            params=params
        )

    def create_qrcode(self, **data):
        return self._post(
            'qrcode/create',
            data=data
        )

    def show_qrcode(self, ticket):
        return requests.get(
            url='https://mp.weixin.qq.com/cgi-bin/showqrcode',
            params={
                'ticket': ticket
            }
        )

    @classmethod
    def get_qrcode_url(cls, ticket):
        url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={ticket}'
        if isinstance(ticket, dict):
            ticket = ticket['ticket']
        ticket = six.moves.urllib.parse.quote(ticket)
        return url.format(ticket=ticket)

    def short_url(self, long_url):
        return self._post(
            'shorturl',
            data={
                'action': 'long2short',
                'long_url': long_url
            }
        )

    def upload_articles(self, articles):
        articles_data = []
        for article in articles:
            articles_data.append({
                'thumb_media_id': article['thumb_media_id'],
                'title': article['title'],
                'content': article['content'],
                'author': article.get('author', ''),
                'content_source_url': article.get('content_source_url', ''),
                'digest': article.get('digest', ''),
                'show_cover_pic': article.get('show_cover_pic', 0)
            })
        return self._post(
            'media/uploadnews',
            data={
                'articles': articles_data
            }
        )

    def delete_mass_message(self, msg_id):
        return self._post(
            'message/mass/delete',
            data={
                'msg_id': msg_id
            }
        )

    def _send_mass_message(self, group_or_users, msg_type, msg):
        data = {
            'msgtype': msg_type
        }
        if isinstance(group_or_users, (tuple, list)):
            # send by user ids
            data['touser'] = group_or_users
        else:
            data['filter'] = {'group_id': group_or_users}

        data.update(msg)
        return self._post(
            'message/mass/sendall',
            data=data
        )

    def send_mass_text_message(self, group_or_users, content):
        return self._send_mass_message(
            group_or_users,
            'text',
            {
                'text': {
                    'content': content
                }
            }
        )

    def send_mass_image_message(self, group_or_users, media_id):
        return self._send_mass_message(
            group_or_users,
            'image',
            {
                'image': {
                    'media_id': media_id
                }
            }
        )

    def send_mass_voice_message(self, group_or_users, media_id):
        return self._send_mass_message(
            group_or_users,
            'voice',
            {
                'voice': {
                    'media_id': media_id
                }
            }
        )

    def send_mass_video_message(self, group_or_users, media_id,
                                title=None, description=None):
        video_data = {
            'media_id': media_id
        }
        if title:
            video_data['title'] = title
        if description:
            video_data['description'] = description
        return self._send_mass_message(
            group_or_users,
            'video',
            {
                'video': video_data
            }
        )

    def send_mass_article_message(self, group_or_users, media_id):
        return self._send_mass_message(
            group_or_users,
            'mpnews',
            {
                'mpnews': {
                    'media_id': media_id
                }
            }
        )

    def send_template_message(self, user_id, template_id, url,
                              top_color, data):
        return self._post(
            'message/template/send',
            data={
                'touser': user_id,
                'template_id': template_id,
                'url': url,
                'topcolor': top_color,
                'data': data
            }
        )

    def get_customservice_record(self, start_time, end_time, page_index,
                                 page_size=10, user_id=None):
        if isinstance(start_time, datetime.datetime):
            start_time = time.mktime(start_time.timetuple())
        if isinstance(end_time, datetime.datetime):
            end_time = time.mktime(end_time.timetuple())
        record_data = {
            'starttime': int(start_time),
            'endtime': int(end_time),
            'pageindex': page_index,
            'pagesize': page_size
        }
        if user_id:
            record_data['openid'] = user_id
        return self._post(
            'customservice/getrecord',
            data=record_data
        )
