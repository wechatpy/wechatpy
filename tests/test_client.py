# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import unittest
from datetime import datetime

import six
from httmock import urlmatch, HTTMock, response

from wechatpy import WeChatClient
from wechatpy._compat import json


_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_FIXTURE_PATH = os.path.join(_TESTS_PATH, 'fixtures')


@urlmatch(netloc=r'(.*\.)?api\.weixin\.qq\.com$')
def wechat_api_mock(url, request):
    path = url.path.replace('/cgi-bin/', '').replace('/', '_')
    res_file = os.path.join(_FIXTURE_PATH, '%s.json' % path)
    content = {
        'errcode': 99999,
        'errmsg': 'can not find fixture'
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        with open(res_file) as f:
            content = json.loads(f.read())
    except (IOError, ValueError):
        pass
    return response(200, content, headers, request=request)


class WeChatClientTestCase(unittest.TestCase):

    app_id = '123456'
    secret = '123456'

    def setUp(self):
        self.client = WeChatClient(self.app_id, self.secret)

    def test_fetch_access_token(self):
        with HTTMock(wechat_api_mock):
            token = self.client.fetch_access_token()
            self.assertEqual('1234567890', token['access_token'])
            self.assertEqual(7200, token['expires_in'])
            self.assertEqual('1234567890', self.client.access_token)

    def test_upload_media(self):
        media_file = six.StringIO('nothing')
        with HTTMock(wechat_api_mock):
            media = self.client.media.upload('image', media_file)
            self.assertEqual('image', media['type'])
            self.assertEqual('12345678', media['media_id'])

    def test_create_group(self):
        with HTTMock(wechat_api_mock):
            group = self.client.group.create('test')
            self.assertEqual(1, group['group']['id'])
            self.assertEqual('test', group['group']['name'])

    def test_group_get(self):
        with HTTMock(wechat_api_mock):
            groups = self.client.group.get()
            self.assertEqual(5, len(groups))

    def test_group_getid(self):
        with HTTMock(wechat_api_mock):
            group = self.client.group.get('123456')
            self.assertEqual(102, group)

    def test_group_update(self):
        with HTTMock(wechat_api_mock):
            result = self.client.group.update(102, 'test')
            self.assertEqual(0, result['errcode'])

    def test_group_move_user(self):
        with HTTMock(wechat_api_mock):
            result = self.client.group.move_user('test', 102)
            self.assertEqual(0, result['errcode'])

    def test_send_text_message(self):
        with HTTMock(wechat_api_mock):
            result = self.client.message.send_text(1, 'test', account='test')
            self.assertEqual(0, result['errcode'])

    def test_send_image_message(self):
        with HTTMock(wechat_api_mock):
            result = self.client.message.send_image(1, '123456')
            self.assertEqual(0, result['errcode'])

    def test_send_voice_message(self):
        with HTTMock(wechat_api_mock):
            result = self.client.message.send_voice(1, '123456')
            self.assertEqual(0, result['errcode'])

    def test_send_video_message(self):
        with HTTMock(wechat_api_mock):
            result = self.client.message.send_video(
                1, '123456', 'test', 'test'
            )
            self.assertEqual(0, result['errcode'])

    def test_send_music_message(self):
        with HTTMock(wechat_api_mock):
            result = self.client.message.send_music(
                1, 'http://www.qq.com', 'http://www.qq.com',
                '123456', 'test', 'test'
            )
            self.assertEqual(0, result['errcode'])

    def test_send_articles_message(self):
        with HTTMock(wechat_api_mock):
            articles = [{
                'title': 'test',
                'description': 'test',
                'url': 'http://www.qq.com',
                'image': 'http://www.qq.com'
            }]
            result = self.client.message.send_articles(1, articles)
            self.assertEqual(0, result['errcode'])

    def test_create_menu(self):
        with HTTMock(wechat_api_mock):
            result = self.client.menu.create({
                'button': [
                    {
                        'type': 'click',
                        'name': 'test',
                        'key': 'test'
                    }
                ]
            })
            self.assertEqual(0, result['errcode'])

    def test_get_menu(self):
        with HTTMock(wechat_api_mock):
            menu = self.client.menu.get()
            self.assertTrue('menu' in menu)

    def test_delete_menu(self):
        with HTTMock(wechat_api_mock):
            result = self.client.menu.delete()
            self.assertEqual(0, result['errcode'])

    def test_update_menu(self):
        with HTTMock(wechat_api_mock):
            result = self.client.menu.update({
                'button': [
                    {
                        'type': 'click',
                        'name': 'test',
                        'key': 'test'
                    }
                ]
            })
            self.assertEqual(0, result['errcode'])

    def test_short_url(self):
        with HTTMock(wechat_api_mock):
            result = self.client.misc.short_url('http://www.qq.com')
            self.assertEqual('http://qq.com', result['short_url'])

    def test_get_wechat_ips(self):
        with HTTMock(wechat_api_mock):
            result = self.client.misc.get_wechat_ips()
            self.assertEqual(['127.0.0.1'], result)

    def test_get_user_info(self):
        with HTTMock(wechat_api_mock):
            openid = 'o6_bmjrPTlm6_2sgVt7hMZOPfL2M'
            user = self.client.user.get(openid)
            self.assertEqual('Band', user['nickname'])

    def test_get_followers(self):
        with HTTMock(wechat_api_mock):
            result = self.client.user.get_followers()
            self.assertEqual(2, result['total'])
            self.assertEqual(2, result['count'])

    def test_update_user_remark(self):
        with HTTMock(wechat_api_mock):
            openid = 'openid'
            remark = 'test'
            result = self.client.user.update_remark(openid, remark)
            self.assertEqual(0, result['errcode'])

    def test_create_qrcode(self):
        data = {
            'expire_seconds': 1800,
            'action_name': 'QR_SCENE',
            'action_info': {
                'scene': {'scene_id': 123}
            }
        }
        with HTTMock(wechat_api_mock):
            result = self.client.qrcode.create(data)
            self.assertEqual(1800, result['expire_seconds'])

    def test_get_qrcode_url_with_str_ticket(self):
        ticket = '123'
        url = self.client.qrcode.get_url(ticket)
        self.assertEqual(
            'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=123',
            url
        )

    def test_get_qrcode_url_with_dict_ticket(self):
        ticket = {
            'ticket': '123',
        }
        url = self.client.qrcode.get_url(ticket)
        self.assertEqual(
            'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=123',
            url
        )

    def test_customservice_add_account(self):
        with HTTMock(wechat_api_mock):
            result = self.client.customservice.add_account(
                'test1@test',
                'test1',
                'test1'
            )
            self.assertEqual(0, result['errcode'])

    def test_customservice_update_account(self):
        with HTTMock(wechat_api_mock):
            result = self.client.customservice.update_account(
                'test1@test',
                'test1',
                'test1'
            )
            self.assertEqual(0, result['errcode'])

    def test_customservice_delete_account(self):
        with HTTMock(wechat_api_mock):
            result = self.client.customservice.delete_account(
                'test1@test',
                'test1',
                'test1'
            )
            self.assertEqual(0, result['errcode'])

    def test_customservice_upload_headimg(self):
        media_file = six.StringIO('nothing')
        with HTTMock(wechat_api_mock):
            result = self.client.customservice.upload_headimg(
                'test1@test',
                media_file
            )
            self.assertEqual(0, result['errcode'])

    def test_customservice_get_accounts(self):
        with HTTMock(wechat_api_mock):
            result = self.client.customservice.get_accounts()
            self.assertEqual(2, len(result))

    def test_customservice_get_online_accounts(self):
        with HTTMock(wechat_api_mock):
            result = self.client.customservice.get_online_accounts()
            self.assertEqual(2, len(result))

    def test_customservice_create_session(self):
        with HTTMock(wechat_api_mock):
            result = self.client.customservice.create_session(
                'openid',
                'test1@test'
            )
            self.assertEqual(0, result['errcode'])

    def test_customservice_close_session(self):
        with HTTMock(wechat_api_mock):
            result = self.client.customservice.close_session(
                'openid',
                'test1@test'
            )
            self.assertEqual(0, result['errcode'])

    def test_customservice_get_session(self):
        with HTTMock(wechat_api_mock):
            result = self.client.customservice.get_session('openid')
            self.assertEqual('test1@test', result['kf_account'])

    def test_customservice_get_session_list(self):
        with HTTMock(wechat_api_mock):
            result = self.client.customservice.get_session_list('test1@test')
            self.assertEqual(2, len(result))

    def test_customservice_get_wait_case(self):
        with HTTMock(wechat_api_mock):
            result = self.client.customservice.get_wait_case()
            self.assertEqual(150, result['count'])

    def test_customservice_get_records(self):
        with HTTMock(wechat_api_mock):
            result = self.client.customservice.get_records(
                123456789,
                987654321,
                1
            )
            self.assertEqual(2, len(result))

    def test_datacube_get_user_summary(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_user_summary(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_user_cumulate(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_user_cumulate(
                datetime(2014, 12, 6),
                datetime(2014, 12, 7)
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_interface_summary(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_interface_summary(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_interface_summary_hour(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_interface_summary_hour(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_article_summary(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_article_summary(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_article_total(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_article_total(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_user_read(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_user_read(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_user_read_hour(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_user_read_hour(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_user_share(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_user_share(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(2, len(result))

    def test_datacube_get_user_share_hour(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_user_share_hour(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_upstream_msg(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_upstream_msg(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_upstream_msg_hour(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_upstream_msg_hour(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_upstream_msg_week(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_upstream_msg_week(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_upstream_msg_month(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_upstream_msg_month(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_upstream_msg_dist(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_upstream_msg_dist(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_upstream_msg_dist_week(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_upstream_msg_dist_week(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_datacube_get_upstream_msg_dist_month(self):
        with HTTMock(wechat_api_mock):
            result = self.client.datacube.get_upstream_msg_dist_month(
                '2014-12-06',
                '2014-12-07'
            )
            self.assertEqual(1, len(result))

    def test_jsapi_get_ticket(self):
        with HTTMock(wechat_api_mock):
            result = self.client.jsapi.get_ticket()
            self.assertEqual(
                'bxLdikRXVbTPdHSM05e5u5sUoXNKd8-41ZO3MhKoyN5OfkWITDGgnr2fwJ0m9E8NYzWKVZvdVtaUgWvsdshFKA',  # NOQA
                result['ticket']
            )
            self.assertEqual(7200, result['expires_in'])

    def test_jsapi_get_jsapi_signature(self):
        noncestr = 'Wm3WZYTPz0wzccnW'
        ticket = 'sM4AOVdWfPE4DxkXGEs8VMCPGGVi4C3VM0P37wVUCFvkVAy_90u5h9nbSlYy3-Sl-HhTdfl2fzFy1AOcHKP7qg'  # NOQA
        timestamp = 1414587457
        url = 'http://mp.weixin.qq.com?params=value'
        signature = self.client.jsapi.get_jsapi_signature(
            noncestr,
            ticket,
            timestamp,
            url
        )
        self.assertEqual(
            '0f9de62fce790f9a083d5c99e95740ceb90c27ed',
            signature
        )

    def test_menu_get_menu_info(self):
        with HTTMock(wechat_api_mock):
            menu_info = self.client.menu.get_menu_info()
            self.assertEqual(1, menu_info['is_menu_open'])

    def test_message_get_autoreply_info(self):
        with HTTMock(wechat_api_mock):
            autoreply = self.client.message.get_autoreply_info()
            self.assertEqual(1, autoreply['is_autoreply_open'])
