from __future__ import absolute_import, unicode_literals
import time
import requests

from .._compat import json
from ..exceptions import WeChatClientException


class WeChatClient(object):

    API_BASE_URL = 'https://qyapi.weixin.qq.com/cgi-bin/'

    def __init__(self, corp_id, secret, access_token=None):
        self.corp_id = corp_id
        self.secret = secret
        self.access_token = access_token
        self.expires_at = None

    def _request(self, method, url_or_endpoint, **kwargs):
        if not (url_or_endpoint.startswith('http://') or
                url_or_endpoint.startswith('https://')):
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
                _token = self.fetch_access_token()
                self._access_token = _token['access_token']
                self.expires_at = int(time.time()) + _token['expires_in']
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

    def fetch_access_token(self):
        """ Fetch access token"""
        res = requests.get(
            url='https://qyapi.weixin.qq.com/cgi-bin/gettoken',
            params={
                'corpid': self.corp_id,
                'corpsecret': self.secret
            }
        )
        result = res.json()
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatClientException(result['errcode'], result['errmsg'])
        return result

    @property
    def access_token(self):
        if self._access_token:
            if not self.expires_at:
                # user provided access_token, just return it
                return self._access_token

            timestamp = time.time()
            if self.expires_at - timestamp > 60:
                return self._access_token

        result = self.fetch_access_token()
        self._access_token = result['access_token']
        self.expires_at = int(time.time()) + 7200
        return self._access_token

    def create_department(self, name, parent_id=1):
        return self._post(
            'department/create',
            data={
                'name': name,
                'parentid': parent_id
            }
        )

    def update_department(self, id, name):
        return self._post(
            'department/update',
            data={
                'id': id,
                'name': name
            }
        )

    def delete_department(self, id):
        return self._get(
            'department/delete',
            params={
                'id': id
            }
        )

    def get_departments(self):
        return self._get('department/list')

    def create_user(self, user_id, name, department=None, position=None,
                    mobile=None, gender=0, tel=None, email=None,
                    weixin_id=None):
        user_data = {
            'userid': user_id,
            'name': name,
            'gender': gender
        }
        if department:
            user_data['department'] = department
        if position:
            user_data['position'] = position
        if mobile:
            user_data['mobile'] = mobile
        if tel:
            user_data['tel'] = tel
        if email:
            user_data['email'] = email
        if weixin_id:
            user_data['weixinid'] = weixin_id

        return self._post(
            'user/create',
            data=user_data
        )

    def update_user(self, user_id, name=None, department=None, position=None,
                    mobile=None, gender=None, tel=None, email=None,
                    weixin_id=None, enable=None):
        user_data = {
            'userid': user_id
        }
        if name:
            user_data['name'] = name
        if gender is not None:
            user_data['gender'] = gender
        if department:
            user_data['department'] = department
        if position:
            user_data['position'] = position
        if mobile:
            user_data['mobile'] = mobile
        if tel:
            user_data['tel'] = tel
        if email:
            user_data['email'] = email
        if weixin_id:
            user_data['weixinid'] = weixin_id
        if enable is not None:
            user_data['enable'] = 1 if enable else 0

        return self._post(
            'user/update',
            data=user_data
        )

    def delete_user(self, user_id):
        return self._get(
            'user/delete',
            params={
                'userid': user_id
            }
        )

    def get_user(self, user_id):
        return self._get(
            'user/get',
            params={
                'userid': user_id
            }
        )

    def get_department_users(self, department, status=0, fetch_child=0):
        fetch_child = 1 if fetch_child else 0
        return self._get(
            'user/simplelist',
            params={
                'department_id': department,
                'status': status,
                'fetch_child': fetch_child
            }
        )

    def create_tag(self, name):
        return self._post(
            'tag/create',
            data={
                'tagname': name
            }
        )

    def update_tag(self, tag_id, name):
        return self._post(
            'tag/update',
            data={
                'tagid': tag_id,
                'tagname': name
            }
        )

    def delete_tag(self, tag_id):
        return self._get(
            'tag/delete',
            params={
                'tagid': tag_id
            }
        )

    def get_tag_users(self, tag_id):
        return self._get(
            'tag/get',
            params={
                'tagid': tag_id
            }
        )

    def add_tag_users(self, tag_id, user_ids):
        return self._post(
            'tag/addtagusers',
            data={
                'tagid': tag_id,
                'userlist': user_ids
            }
        )

    def delete_tag_users(self, tag_id, user_ids):
        return self._post(
            'tag/deltagusers',
            data={
                'tagid': tag_id,
                'userlist': user_ids
            }
        )

    def upload_media(self, media_type, media_file):
        return self._post(
            'media/upload',
            params={
                'type': media_type
            },
            files={
                'media': media_file
            }
        )

    def download_media(self, media_id):
        return self._get(
            'media/get',
            params={
                'media_id': media_id
            }
        )

    def verify_user(self, user_id):
        return self._get(
            'user/authsucc',
            params={
                'userid': user_id
            }
        )

    def create_menu(self, agent_id, menu_data):
        return self._post(
            'menu/create',
            params={
                'agentid': agent_id
            },
            data=menu_data
        )

    def get_menu(self, agent_id):
        try:
            return self._get(
                'menu/get',
                params={
                    'agentid': agent_id
                }
            )
        except WeChatClientException as e:
            if e.errcode == 46003:
                # menu not exist
                return None
            else:
                raise e

    def delete_menu(self, agent_id):
        return self._get(
            'menu/delete',
            params={
                'agentid': agent_id
            }
        )

    def get_user_info(self, agent_id, code):
        return self._get(
            'user/getuserinfo',
            params={
                'agentid': agent_id,
                'code': code
            }
        )

    def _send_message(self, agent_id, user_ids, party_ids='',
                      tag_ids='', msg=None):
        msg = msg or {}
        if isinstance(user_ids, (tuple, list)):
            user_ids = '|'.join(user_ids)
        if isinstance(party_ids, (tuple, list)):
            party_ids = '|'.join(party_ids)
        if isinstance(tag_ids, (tuple, list)):
            tag_ids = '|'.join(tag_ids)

        data = {
            'touser': user_ids,
            'toparty': party_ids,
            'totag': tag_ids,
            'agentid': agent_id
        }
        data.update(msg)
        return self._post(
            'message/send',
            data=data
        )

    def send_text_message(self, agent_id, user_ids, content,
                          party_ids='', tag_ids='', safe=0):
        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'text',
                'text': {'content': content},
                'safe': safe
            }
        )

    def send_image_message(self, agent_id, user_ids, media_id,
                           party_ids='', tag_ids='', safe=0):
        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'image',
                'image': {
                    'media_id': media_id
                },
                'safe': safe
            }
        )

    def send_voice_message(self, agent_id, user_ids, media_id,
                           party_ids='', tag_ids='', safe=0):
        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'voice',
                'voice': {
                    'media_id': media_id
                },
                'safe': safe
            }
        )

    def send_video_message(self, agent_id, user_ids, media_id, title=None,
                           description=None, party_ids='', tag_ids='',
                           safe=0):
        video_data = {
            'media_id': media_id
        }
        if title:
            video_data['title'] = title
        if description:
            video_data['description'] = description

        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'video',
                'video': video_data,
                'safe': safe
            }
        )

    def send_file_message(self, agent_id, user_ids, media_id,
                          party_ids='', tag_ids='', safe=0):
        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'file',
                'file': {
                    'media_id': media_id
                },
                'safe': safe
            }
        )

    def send_article_message(self, agent_id, user_ids, articles,
                             party_ids='', tag_ids=''):
        articles_data = []
        for article in articles:
            articles_data.append({
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'picurl': article['image']
            })
        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'news',
                'news': {
                    'articles': articles_data
                }
            }
        )

    def send_mp_article_message(self, agent_id, user_ids, articles,
                                party_ids='', tag_ids='', safe=0):
        articles_data = []
        for article in articles:
            articles_data.append({
                'thumb_media_id': article['thumb_media_id'],
                'author': article['author'],
                'content': article['content'],
                'content_source_url': article['content_source_url'],
                'digest': article['digest'],
                'show_cover_pic': article['show_cover_pic']
            })
        return self._send_message(
            agent_id,
            user_ids,
            party_ids,
            tag_ids,
            msg={
                'msgtype': 'mpnews',
                'mpnews': {
                    'articles': articles_data
                },
                'safe': safe
            }
        )
