# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import time
import datetime
import requests
import six

from ._compat import json
from .utils import to_text
from .exceptions import WeChatClientException, APILimitedException


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
            errcode = result['errcode']
            errmsg = result['errmsg']
            if errcode == 42001:
                # access_token expired, fetch a new one and retry request
                self.fetch_access_token()
                return self._request(
                    method=method,
                    url=url,
                    **kwargs
                )
            elif errcode == 45009:
                # api freq out of limit
                raise APILimitedException(errcode, errmsg)
            else:
                raise WeChatClientException(errcode, errmsg)

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
        """ WeChat access token """
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
    """
    微信 API 操作类
    通过这个类可以操作微信 API，发送主动消息、群发消息和创建自定义菜单等。
    """

    API_BASE_URL = 'https://api.weixin.qq.com/cgi-bin/'

    def __init__(self, appid, secret, access_token=None):
        self.appid = appid
        self.secret = secret
        self._access_token = access_token
        self.expires_at = None

    def fetch_access_token(self):
        """
        获取 access token
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=通用接口文档

        :return: 返回的 JSON 数据包
        """
        return self._fetch_access_token(
            url='https://api.weixin.qq.com/cgi-bin/token',
            params={
                'grant_type': 'client_credential',
                'appid': self.appid,
                'secret': self.secret
            }
        )

    def send_text_message(self, user_id, content):
        """
        发送文本消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param content: 消息正文
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'text',
                'text': {'content': content}
            }
        )

    def send_image_message(self, user_id, media_id):
        """
        发送图片消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 图片的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        """
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
        """
        发送语音消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 发送的语音的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        """
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
        """
        发送视频消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 发送的视频的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        :return: 返回的 JSON 数据包
        """
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
        """
        发送音乐消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param url: 音乐链接
        :param hq_url: 高品质音乐链接，wifi环境优先使用该链接播放音乐
        :param thumb_media_id: 缩略图的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 音乐标题
        :param description: 音乐描述
        :return: 返回的 JSON 数据包
        """
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
        """
        发送图文消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param articles: 一个包含至多10个图文的数组
        :return: 返回的 JSON 数据包
        """
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
        """
        创建自定义菜单 ::

            client = WeChatClient("id", "secret")
            client.create_menu({
                "button":[
                    {
                        "type":"click",
                        "name":"今日歌曲",
                        "key":"V1001_TODAY_MUSIC"
                    },
                    {
                        "type":"click",
                        "name":"歌手简介",
                        "key":"V1001_TODAY_SINGER"
                    },
                    {
                        "name":"菜单",
                        "sub_button":[
                            {
                                "type":"view",
                                "name":"搜索",
                                "url":"http://www.soso.com/"
                            },
                            {
                                "type":"view",
                                "name":"视频",
                                "url":"http://v.qq.com/"
                            },
                            {
                                "type":"click",
                                "name":"赞一下我们",
                                "key":"V1001_GOOD"
                            }
                        ]
                    }
                ]
            })

        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单创建接口

        :param menu_data: Python 字典

        :return: 返回的 JSON 数据包
        """
        return self._post(
            'menu/create',
            data=menu_data
        )

    def get_menu(self):
        """
        查询自定义菜单。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单查询接口

        :return: 返回的 JSON 数据包
        """
        try:
            return self._get('menu/get')
        except WeChatClientException as e:
            if e.errcode == 46003:
                # menu not exist
                return None
            else:
                raise e

    def delete_menu(self):
        """
        删除自定义菜单。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单删除接口

        :return: 返回的 JSON 数据包
        """
        return self._get('menu/delete')

    def update_menu(self, menu_data):
        """
        更新自定义菜单
        等同于先调用 :func:`delete_menu` 删除自定义菜单后，
        再调用 :func:`create_menu` 创建自定义菜单。
        """
        self.delete_menu()
        return self.create_menu(menu_data)

    def upload_media(self, media_type, media_file):
        """
        上传多媒体文件。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=上传下载多媒体文件

        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param media_file: 要上传的文件，一个 File-object

        :return: 返回的 JSON 数据包
        """
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
        """
        下载多媒体文件。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=上传下载多媒体文件

        :param media_id: 媒体文件 ID

        :return: requests 的 Response 实例
        """
        return requests.get(
            'http://file.api.weixin.qq.com/cgi-bin/media/get',
            params={
                'access_token': self.access_token,
                'media_id': media_id
            }
        )

    def upload_video(self, media_id, title, description):
        """
        群发视频消息时获取视频 media_id
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=高级群发接口

        :param media_id: 需通过基础支持中的上传下载多媒体文件 :func:`upload_media` 来得到
        :param title: 视频标题
        :param description: 视频描述

        :return: 返回的 JSON 数据包
        """
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
        """
        创建分组
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口

        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包

        """
        name = to_text(name)
        return self._post(
            'groups/create',
            data={'group': {'name': name}}
        )

    def get_groups(self):
        """
        查询所有分组
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口

        :return: 返回的 JSON 数据包
        """
        return self._get('groups/get')

    def get_group_by_user_id(self, user_id):
        """
        查询用户所在分组
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口

        :param user_id: 用户的 OpenID
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'groups/getid',
            data={'openid': user_id}
        )

    def update_group(self, group_id, name):
        """
        修改分组名
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口

        :param group_id: 分组id，由微信分配
        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包
        """
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
        """
        移动用户分组
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param group_id: 分组 ID
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'groups/members/update',
            data={
                'openid': user_id,
                'to_groupid': group_id
            }
        )

    def get_user_info(self, user_id, lang='zh_CN'):
        """
        获取用户基本信息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=获取用户基本信息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return: 返回的 JSON 数据包
        """
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
        """
        获取关注者列表
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=获取关注者列表

        :param first_user_id: 可选。第一个拉取的 OPENID，不填默认从头开始拉取
        :return: 返回的 JSON 数据包
        """
        params = {}
        if first_user_id:
            params['next_openid'] = first_user_id
        return self._get(
            'user/get',
            params=params
        )

    def create_qrcode(self, **data):
        """
        创建二维码
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=生成带参数的二维码

        :param data: 你要发送的参数 dict
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'qrcode/create',
            data=data
        )

    def show_qrcode(self, ticket):
        """
        通过ticket换取二维码
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=生成带参数的二维码

        :param ticket: 二维码 ticket 。可以通过 :func:`create_qrcode` 获取到
        :return: 返回的 Request 对象
        """
        return requests.get(
            url='https://mp.weixin.qq.com/cgi-bin/showqrcode',
            params={
                'ticket': ticket
            }
        )

    @classmethod
    def get_qrcode_url(cls, ticket):
        """
        通过ticket换取二维码地址
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=生成带参数的二维码

        :param ticket: 二维码 ticket 。可以通过 :func:`create_qrcode` 获取到
        :return: 返回的二维码地址
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={ticket}'
        if isinstance(ticket, dict):
            ticket = ticket['ticket']
        ticket = six.moves.urllib.parse.quote(ticket)
        return url.format(ticket=ticket)

    def short_url(self, long_url):
        """
        将一条长链接转成短链接
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=长链接转短链接接口

        :param long_url: 长链接地址
        :return: 返回的 JSON 数据包
        """
        return self._post(
            'shorturl',
            data={
                'action': 'long2short',
                'long_url': long_url
            }
        )

    def upload_articles(self, articles):
        """
        上传图文消息素材
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=高级群发接口

        :param articles: 图文消息数组
        :return: 返回的 JSON 数据包
        """
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
        """
        删除群发消息
        http://mp.weixin.qq.com/wiki/index.php?title=高级群发接口

        :param msg_id: 要删除的群发消息 ID
        :return: 返回的 JSON 数据包
        """
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
        """
        群发文本消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=高级群发接口

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param content: 消息正文

        :return: 返回的 JSON 数据包
        """
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
        """
        群发图片消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=高级群发接口

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param media_id: 图片的媒体 ID。 可以通过 :func:`upload_media` 上传。

        :return: 返回的 JSON 数据包
        """
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
        """
        群发语音消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=高级群发接口

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param media_id: 语音的媒体 ID。可以通过 :func:`upload_media` 上传。

        :return: 返回的 JSON 数据包
        """
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
        """
        群发视频消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=高级群发接口

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param media_id: 视频的媒体 ID。可以通过 :func:`upload_video` 上传。
        :param title: 视频标题
        :param description: 视频描述

        :return: 返回的 JSON 数据包
        """
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
        """
        群发图文消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=高级群发接口

        :param group_or_users: 值为整型数字时为按分组群发，值为列表/元组时为按 OpenID 列表群发
        :param media_id: 图文的媒体 ID。可以通过 :func:`upload_articles` 上传。

        :return: 返回的 JSON 数据包
        """
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
        """
        发送模板消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=模板消息接口

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param template_id: 模板 ID。在公众平台线上模板库中选用模板获得
        :param url: 链接地址
        :param top_color: 消息顶部颜色
        :param data: 模板消息数据

        :return: 返回的 JSON 数据包
        """
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
        """
        获取客服聊天记录
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=获取客服聊天记录

        :param start_time: 查询开始时间，UNIX 时间戳
        :param end_time: 查询结束时间，UNIX 时间戳，每次查询不能跨日查询
        :param page_index: 查询第几页，从 1 开始
        :param page_size: 每页大小，每页最多拉取 1000 条
        :param user_id: 普通用户的标识，对当前公众号唯一

        :return: 返回的 JSON 数据包
        """
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
