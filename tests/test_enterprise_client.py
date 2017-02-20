# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import six
import unittest

from httmock import urlmatch, HTTMock, response

from wechatpy.enterprise import WeChatClient
from wechatpy.exceptions import WeChatClientException
from wechatpy.utils import json


_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_FIXTURE_PATH = os.path.join(_TESTS_PATH, 'fixtures', 'enterprise')


@urlmatch(netloc=r'(.*\.)?qyapi\.weixin\.qq\.com$')
def wechat_api_mock(url, request):
    path = url.path.replace('/cgi-bin/', '').replace('/', '_')
    res_file = os.path.join(_FIXTURE_PATH, '%s.json' % path)
    content = {
        'errcode': 99999,
        'errmsg': 'can not find fixture %s' % res_file,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        with open(res_file, 'rb') as f:
            content = json.loads(f.read().decode('utf-8'))
    except (IOError, ValueError) as e:
        content['errmsg'] = 'Loads fixture {0} failed, error: {1}'.format(
            res_file,
            e
        )
    return response(200, content, headers, request=request)


class WeChatClientTestCase(unittest.TestCase):
    corp_id = '123456'
    secret = '123456'

    def setUp(self):
        self.client = WeChatClient(self.corp_id, self.secret)

    def test_fetch_access_token(self):
        with HTTMock(wechat_api_mock):
            token = self.client.fetch_access_token()
            self.assertEqual('1234567890', token['access_token'])
            self.assertEqual(7200, token['expires_in'])
            self.assertEqual('1234567890', self.client.access_token)

    def test_get_wechat_ips(self):
        with HTTMock(wechat_api_mock):
            res = self.client.misc.get_wechat_ips()
            self.assertEqual(['127.0.0.1'], res)

    def test_department_create(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.create('Test')
            self.assertEqual(2, res['id'])

    def test_department_update(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.update(2, 'Test 1')
            self.assertEqual(0, res['errcode'])

    def test_department_delete(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.delete(2)
            self.assertEqual(0, res['errcode'])

    def test_department_get(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.get()
            self.assertEqual(2, len(res))

    def test_department_get_users(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.get_users(2)
            self.assertEqual(1, len(res))

    def test_tag_create(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.create('test')
            self.assertEqual('1', res['tagid'])

    def test_tag_update(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.update(1, 'test')
            self.assertEqual(0, res['errcode'])

    def test_tag_delete(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.delete(1)
            self.assertEqual(0, res['errcode'])

    def test_tag_get_users(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.get_users(1)
            self.assertEqual(1, len(res['userlist']))
            self.assertEqual(1, len(res['partylist']))

    def test_tag_add_users(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.add_users(1, [1, 2, 3])
            self.assertEqual(0, res['errcode'])

    def test_tag_delete_users(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.delete_users(1, [1, 2, 3])
            self.assertEqual(0, res['errcode'])

    def test_tag_list(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.list()
            self.assertEqual(2, len(res))

    def test_batch_invite_user(self):
        with HTTMock(wechat_api_mock):
            res = self.client.batch.invite_user(
                'http://example.com',
                '123456',
                '123456',
                '123|456',
                [123, 456],
                (12, 34),
                ''
            )
            self.assertEqual(0, res['errcode'])

    def test_batch_sync_user(self):
        with HTTMock(wechat_api_mock):
            res = self.client.batch.sync_user(
                'http://example.com',
                '123456',
                '123456',
                '12345678'
            )
            self.assertEqual(0, res['errcode'])

    def test_batch_replace_user(self):
        with HTTMock(wechat_api_mock):
            res = self.client.batch.replace_user(
                'http://example.com',
                '123456',
                '123456',
                '12345678'
            )
            self.assertEqual(0, res['errcode'])

    def test_batch_replace_party(self):
        with HTTMock(wechat_api_mock):
            res = self.client.batch.replace_party(
                'http://example.com',
                '123456',
                '123456',
                '12345678'
            )
            self.assertEqual(0, res['errcode'])

    def test_batch_get_result(self):
        with HTTMock(wechat_api_mock):
            res = self.client.batch.get_result('123456')
            self.assertEqual(0, res['errcode'])
            self.assertEqual(1, res['status'])

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

    def test_user_convert_to_openid(self):
        with HTTMock(wechat_api_mock):
            res = self.client.user.convert_to_openid('zhangsan')
            self.assertEqual('oDOGms-6yCnGrRovBj2yHij5JL6E', res['openid'])
            self.assertEqual('wxf874e15f78cc84a7', res['appid'])

    def test_user_convert_to_user_id(self):
        with HTTMock(wechat_api_mock):
            user_id = self.client.user.convert_to_user_id(
                'oDOGms-6yCnGrRovBj2yHij5JL6E'
            )
            self.assertEqual('zhangsan', user_id)

    def test_upload_media(self):
        media_file = six.StringIO('nothing')
        with HTTMock(wechat_api_mock):
            media = self.client.media.upload('image', media_file)
            self.assertEqual('image', media['type'])
            self.assertEqual('12345678', media['media_id'])

    def test_material_get_count(self):
        with HTTMock(wechat_api_mock):
            res = self.client.material.get_count(1)
            self.assertEqual(37, res['total_count'])
            self.assertEqual(3, res['video_count'])
            self.assertEqual(10, res['voice_count'])
            self.assertEqual(12, res['image_count'])
            self.assertEqual(3, res['file_count'])
            self.assertEqual(6, res['mpnews_count'])

    def test_material_batchget_mpnews(self):
        with HTTMock(wechat_api_mock):
            res = self.client.material.batchget(1, 'mpnews')
            self.assertEqual('mpnews', res['type'])
            self.assertEqual(20, res['total_count'])
            self.assertEqual(3, res['item_count'])
            self.assertEqual(
                '2-G6nrLmr5EC3MMb_-zK1dDdzmd0p7cNliYu',
                res['itemlist'][0]['media_id']
            )

    def test_material_delete(self):
        media_id = '2-G6nrLmr5EC3MMb_-zK1dDdzmd0p7cNliYu'
        with HTTMock(wechat_api_mock):
            res = self.client.material.delete(1, media_id)
            self.assertEqual('deleted', res['errmsg'])

    def test_material_get_mpnews(self):
        media_id = '2-G6nrLmr5EC3MMb_-zK1dDdzmd0p7cNliYu'
        with HTTMock(wechat_api_mock):
            res = self.client.material.get_articles(1, media_id)
            self.assertEqual('mpnews', res['type'])
            self.assertEqual(
                '2-G6nrLmr5EC3MMb_-zK1dDdzmd0' +
                'p7cNliYu9V5w7o8K0HuucGBZCzw4HmLa5C',
                res['mpnews']['articles'][0]['thumb_media_id']
            )
            self.assertEqual(
                '2-G6nrLmr5EC3MMb_-zK1dDdzmd0' +
                'p7cNliYu9V5w7oovsUPf3wG4t9N3tE',
                res['mpnews']['articles'][1]['thumb_media_id']
            )

    def test_reraise_requests_exception(self):
        @urlmatch(netloc=r'(.*\.)?qyapi\.weixin\.qq\.com$')
        def _wechat_api_mock(url, request):
            return {'status_code': 404, 'content': '404 not found'}

        try:
            with HTTMock(_wechat_api_mock):
                self.client.material.get_count(1)
        except WeChatClientException as e:
            self.assertEqual(404, e.response.status_code)

    def test_shakearound_get_shake_info(self):
        with HTTMock(wechat_api_mock):
            res = self.client.shakearound.get_shake_info('123456')
            self.assertEqual(14000, res['page_id'])
            self.assertEqual('zhangsan', res['userid'])

    def test_service_get_provider_token(self):
        with HTTMock(wechat_api_mock):
            res = self.client.service.get_provider_token('provider_secret')

        self.assertEqual(7200, res['expires_in'])
        self.assertEqual('enLSZ5xxxxxxJRL', res['provider_access_token'])

    def test_service_get_login_info(self):
        with HTTMock(wechat_api_mock):
            res = self.client.service.get_login_info(
                'enLSZ5xxxxxxJRL',
                'auth_code'
            )

        self.assertTrue(res['is_sys'])
        self.assertTrue(res['is_inner'])

    def test_chat_create(self):
        with HTTMock(wechat_api_mock):
            res = self.client.chat.create(
                '1', 'chat', 'zhangsan', ['zhangsan', 'lisi', 'wangwu']
            )

        self.assertEqual(0, res['errcode'])

    def test_chat_get(self):
        with HTTMock(wechat_api_mock):
            chat = self.client.chat.get('235364212115767297')

        self.assertEqual('235364212115767297', chat['chatid'])
        self.assertEqual('zhangsan', chat['owner'])

    def test_chat_update(self):
        with HTTMock(wechat_api_mock):
            res = self.client.chat.update(
                '235364212115767297',
                'lisi',
                '企业应用中心',
                'zhangsan',
                ['zhaoli'],
                ['zhangsan']
            )

        self.assertEqual(0, res['errcode'])

    def test_chat_quit(self):
        with HTTMock(wechat_api_mock):
            res = self.client.chat.quit('235364212115767297', 'lisi')

        self.assertEqual(0, res['errcode'])

    def test_chat_clear_notify(self):
        with HTTMock(wechat_api_mock):
            res = self.client.chat.clear_notify('zhangsan', 'single', 'lisi')

        self.assertEqual(0, res['errcode'])

    def test_chat_set_mute(self):
        mute_list = [
            {'userid': 'zhangsan', 'status': 0},
            {'userid': 'lisi', 'status': 1},
        ]
        with HTTMock(wechat_api_mock):
            res = self.client.chat.set_mute(mute_list)

        self.assertEqual(0, res['errcode'])
        self.assertEqual(['zhangsan'], res['invaliduser'])

    def test_chat_send_text(self):
        with HTTMock(wechat_api_mock):
            res = self.client.chat.send_text(
                'zhangsan', 'single', 'lisi', 'hello'
            )

        self.assertEqual(0, res['errcode'])

    def test_chat_send_image(self):
        with HTTMock(wechat_api_mock):
            res = self.client.chat.send_image(
                'zhangsan', 'single', 'lisi', 'media_id'
            )

        self.assertEqual(0, res['errcode'])

    def test_chat_send_file(self):
        with HTTMock(wechat_api_mock):
            res = self.client.chat.send_file(
                'zhangsan', 'single', 'lisi', 'media_id'
            )

        self.assertEqual(0, res['errcode'])
