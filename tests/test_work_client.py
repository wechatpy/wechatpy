# -*- coding: utf-8 -*-
import io
import json
import os
import unittest

from httmock import HTTMock, response, urlmatch

from wechatpy.exceptions import WeChatClientException
from wechatpy.work import WeChatClient

_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_FIXTURE_PATH = os.path.join(_TESTS_PATH, "fixtures", "work")


@urlmatch(netloc=r"(.*\.)?qyapi\.weixin\.qq\.com$")
def wechat_api_mock(url, request):
    path = url.path.replace("/cgi-bin/", "").replace("/", "_")
    res_file = os.path.join(_FIXTURE_PATH, f"{path}.json")
    content = {
        "errcode": 99999,
        "errmsg": f"can not find fixture {res_file}",
    }
    headers = {"Content-Type": "application/json"}
    try:
        with open(res_file, "rb") as f:
            content = json.loads(f.read().decode("utf-8"))
    except (IOError, ValueError) as e:
        content["errmsg"] = f"Loads fixture {res_file} failed, error: {e}"
    return response(200, content, headers, request=request)


class WeChatClientTestCase(unittest.TestCase):
    corp_id = "123456"
    secret = "123456"

    def setUp(self):
        self.client = WeChatClient(self.corp_id, self.secret)

    def test_init_client_with_access_token(self):
        client = WeChatClient(self.corp_id, self.secret, access_token="abcdef")
        self.assertTrue(client)

    def test_fetch_access_token(self):
        with HTTMock(wechat_api_mock):
            token = self.client.fetch_access_token()
            self.assertEqual("1234567890", token["access_token"])
            self.assertEqual(7200, token["expires_in"])
            self.assertEqual("1234567890", self.client.access_token)

    def test_get_wechat_ips(self):
        with HTTMock(wechat_api_mock):
            res = self.client.misc.get_wechat_ips()
            self.assertEqual(["127.0.0.1"], res)

    def test_department_create(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.create("Test")
            self.assertEqual(2, res["id"])

    def test_department_update(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.update(2, "Test 1")
            self.assertEqual(0, res["errcode"])

    def test_department_delete(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.delete(2)
            self.assertEqual(0, res["errcode"])

    def test_department_get(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.get()
            self.assertEqual(2, len(res))

    def test_department_get_users(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.get_users(2)
            self.assertEqual(1, len(res))

    def test_department_get_users_detail(self):
        with HTTMock(wechat_api_mock):
            res = self.client.department.get_users(2, simple=False)
            self.assertEqual(1, len(res))

    def test_department_map_users(self):
        with HTTMock(wechat_api_mock):
            users = self.client.department.get_map_users(2, key="email")
            self.assertEqual(users, {"zhangthree@wechat.com": "zhangthree-userid"})

            users = self.client.department.get_map_users(key="mobile")
            self.assertEqual(users, {"15723333333": "zhangthree-userid"})

    def test_tag_create(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.create("test")
            self.assertEqual("1", res["tagid"])

    def test_tag_create_with_invalid_tag_id(self):
        with HTTMock(wechat_api_mock):
            self.assertRaises(ValueError, self.client.tag.create, tag_id=-1, name="xxx")

    def test_tag_create_with_invalid_tag_name(self):
        with HTTMock(wechat_api_mock):
            self.assertRaises(ValueError, self.client.tag.create, name="x" * 33)

    def test_tag_update(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.update(1, "test")
            self.assertEqual(0, res["errcode"])

    def test_tag_delete(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.delete(1)
            self.assertEqual(0, res["errcode"])

    def test_tag_get_users(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.get_users(1)
            self.assertEqual(1, len(res["userlist"]))
            self.assertEqual(1, len(res["partylist"]))

    def test_tag_add_users(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.add_users(1, [1, 2, 3])
            self.assertEqual(0, res["errcode"])

    def test_tag_add_users_with_depts(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.add_users(1, department_ids=[1, 2, 3])
            self.assertEqual(0, res["errcode"])

    def test_tag_add_users_with_empty_user_and_dept(self):
        with HTTMock(wechat_api_mock):
            self.assertRaises(
                ValueError,
                self.client.tag.add_users,
                tag_id=1,
            )

    def test_tag_add_users_with_too_more_users_or_depts(self):
        with HTTMock(wechat_api_mock):
            user_ids = [str(i) for i in range(1001)]
            department_ids = list(range(101))
            self.assertRaises(ValueError, self.client.tag.add_users, tag_id=1, user_ids=user_ids)
            self.assertRaises(ValueError, self.client.tag.add_users, tag_id=1, department_ids=department_ids)

    def test_tag_delete_users(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.delete_users(1, [1, 2, 3])
            self.assertEqual(0, res["errcode"])

    def test_tag_delete_users_with_delete_depts(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.delete_users(1, department_ids=[1, 2, 3])
            self.assertEqual(0, res["errcode"])

    def test_tag_delete_users_with_empty_users_and_depts(self):
        with HTTMock(wechat_api_mock):
            self.assertRaises(ValueError, self.client.tag.delete_users, tag_id=1)

    def test_tag_delete_users_with_too_more_user_or_dept(self):
        with HTTMock(wechat_api_mock):
            user_ids = [str(i) for i in range(1001)]
            department_ids = list(range(101))
            self.assertRaises(ValueError, self.client.tag.delete_users, tag_id=1, user_ids=user_ids)
            self.assertRaises(ValueError, self.client.tag.delete_users, tag_id=1, department_ids=department_ids)

    def test_tag_list(self):
        with HTTMock(wechat_api_mock):
            res = self.client.tag.list()
            self.assertEqual(2, len(res))

    def test_batch_sync_user(self):
        with HTTMock(wechat_api_mock):
            res = self.client.batch.sync_user("http://example.com", "123456", "123456", "12345678")
            self.assertEqual(0, res["errcode"])

    def test_batch_replace_user(self):
        with HTTMock(wechat_api_mock):
            res = self.client.batch.replace_user("http://example.com", "123456", "123456", "12345678")
            self.assertEqual(0, res["errcode"])

    def test_batch_replace_party(self):
        with HTTMock(wechat_api_mock):
            res = self.client.batch.replace_party("http://example.com", "123456", "123456", "12345678")
            self.assertEqual(0, res["errcode"])

    def test_batch_get_result(self):
        with HTTMock(wechat_api_mock):
            res = self.client.batch.get_result("123456")
            self.assertEqual(0, res["errcode"])
            self.assertEqual(1, res["status"])

    def test_jsapi_get_ticket(self):
        with HTTMock(wechat_api_mock):
            result = self.client.jsapi.get_ticket()
            self.assertEqual(
                "bxLdikRXVbTPdHSM05e5u5sUoXNKd8-41ZO3MhKoyN5OfkWITDGgnr2fwJ0m9E8NYzWKVZvdVtaUgWvsdshFKA",  # NOQA
                result["ticket"],
            )
            self.assertEqual(7200, result["expires_in"])

    def test_jsapi_get_jsapi_signature(self):
        noncestr = "Wm3WZYTPz0wzccnW"
        ticket = "sM4AOVdWfPE4DxkXGEs8VMCPGGVi4C3VM0P37wVUCFvkVAy_90u5h9nbSlYy3-Sl-HhTdfl2fzFy1AOcHKP7qg"  # NOQA
        timestamp = 1414587457
        url = "http://mp.weixin.qq.com?params=value"
        signature = self.client.jsapi.get_jsapi_signature(noncestr, ticket, timestamp, url)
        self.assertEqual("0f9de62fce790f9a083d5c99e95740ceb90c27ed", signature)

    def test_user_convert_to_openid(self):
        with HTTMock(wechat_api_mock):
            res = self.client.user.convert_to_openid("zhangsan")
            self.assertEqual("oDOGms-6yCnGrRovBj2yHij5JL6E", res["openid"])
            self.assertEqual("wxf874e15f78cc84a7", res["appid"])

    def test_user_convert_to_user_id(self):
        with HTTMock(wechat_api_mock):
            user_id = self.client.user.convert_to_user_id("oDOGms-6yCnGrRovBj2yHij5JL6E")
            self.assertEqual("zhangsan", user_id)

    def test_user_get_active_stat(self):
        with HTTMock(wechat_api_mock):
            active_stat = self.client.user.get_active_stat("2020-03-27")
            self.assertEqual(active_stat, 100)

    def test_user_join_qrcode(self):
        with HTTMock(wechat_api_mock):
            qrcode_url = self.client.user.get_join_qrcode()
            self.assertIsNotNone(qrcode_url)

    def test_upload_media(self):
        media_file = io.StringIO("nothing")
        with HTTMock(wechat_api_mock):
            media = self.client.media.upload("image", media_file)
            self.assertEqual("image", media["type"])
            self.assertEqual("12345678", media["media_id"])

    def test_reraise_requests_exception(self):
        @urlmatch(netloc=r"(.*\.)?qyapi\.weixin\.qq\.com$")
        def _wechat_api_mock(url, request):
            return {"status_code": 404, "content": "404 not found"}

        try:
            with HTTMock(_wechat_api_mock):
                self.client.user.convert_to_openid("zhangsan")
        except WeChatClientException as e:
            self.assertEqual(404, e.response.status_code)

    def test_service_get_provider_token(self):
        with HTTMock(wechat_api_mock):
            res = self.client.service.get_provider_token("provider_secret")

        self.assertEqual(7200, res["expires_in"])
        self.assertEqual("enLSZ5xxxxxxJRL", res["provider_access_token"])

    def test_service_get_login_info(self):
        with HTTMock(wechat_api_mock):
            res = self.client.service.get_login_info("enLSZ5xxxxxxJRL", "auth_code")

        self.assertTrue(res["is_sys"])
        self.assertTrue(res["is_inner"])

    def test_external_contact_get_follow_user_list(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.get_follow_user_list()
            self.assertEqual(0, res["errcode"])

    def test_external_contact_list(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.list("userid")
            self.assertEqual(0, res["errcode"])

    def test_external_contact_get(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.get("external_userid")
            self.assertEqual(0, res["errcode"])

    def test_external_contact_add_contact_way(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.add_contact_way(
                1,
                1,
                1,
                "remark",
                True,
                "state",
                ["UserID1", "UserID2"],
                ["PartyID1", "PartyID2"],
            )
            self.assertEqual(0, res["errcode"])

    def test_external_contact_get_contact_way(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.get_contact_way("42b34949e138eb6e027c123cba77fad7")
            self.assertEqual(0, res["errcode"])

    def test_external_contact_update_contact_way(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.update_contact_way(
                "42b34949e138eb6e027c123cba77fad7",
                "渠道客户",
                True,
                1,
                "teststate",
                ["UserID1", "UserID2", "UserID3"],
                ["PartyID1", "PartyID2"],
            )
            self.assertEqual(0, res["errcode"])

    def test_external_contact_del_contact_way(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.del_contact_way("42b34949e138eb6e027c123cba77fad7")
            self.assertEqual(0, res["errcode"])

    def test_external_contact_add_msg_template(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.add_msg_template(
                {
                    "external_userid": ["woAJ2GCAAAXtWyujaWJHDDGi0mACas1w", "wmqfasd1e1927831291723123109r712"],
                    "sender": "zhangsan",
                    "text": {"content": "文本消息内容"},
                    "image": {"media_id": "MEDIA_ID"},
                }
            )
            self.assertEqual(0, res["errcode"])

    def test_external_contact_get_group_msg_result(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.get_group_msg_result("msgGCAAAXtWyujaWJHDDGi0mACas1w")
            self.assertEqual(0, res["errcode"])

    def test_external_contact_get_user_behavior_data(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.get_user_behavior_data(["zhangsan", "lisi"], 1536508800, 1536940800)
            self.assertEqual(0, res["errcode"])

    def test_external_contact_send_welcome_msg(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.send_welcome_msg(
                {
                    "welcome_code": "CALLBACK_CODE",
                    "text": {"content": "文本消息内容"},
                    "image": {"media_id": "MEDIA_ID"},
                    "link": {
                        "title": "消息标题",
                        "picurl": "https://example.pic.com/path",
                        "desc": "消息描述",
                        "url": "https://example.link.com/path",
                    },
                    "miniprogram": {
                        "title": "消息标题",
                        "pic_media_id": "MEDIA_ID",
                        "appid": "wx8bd80126147df384",
                        "page": "/path/index",
                    },
                }
            )
            self.assertEqual(0, res["errcode"])

    def test_external_contact_get_unassigned_list(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.get_unassigned_list(0, 100)
            self.assertEqual(0, res["errcode"])

    def test_external_contact_transfer(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.transfer("woAJ2GCAAAXtWyujaWJHDDGi0mACH71w", "zhangsan", "lisi")
            self.assertEqual(0, res["errcode"])

    def test_external_contact_get_group_chat_list(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.get_group_chat_list(
                limit=10,
                status_filter=0,
                owner_filter={"userid_list": ["abel"]},
                cursor="r9FqSqsI8fgNbHLHE5QoCP50UIg2cFQbfma3l2QsmwI",
            )
            self.assertEqual(0, res["errcode"])

    def test_external_contact_get_group_chat_info(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.get_group_chat_info(chat_id="wrOgQhDgAAMYQiS5ol9G7gK9JVAAAA")
            self.assertEqual(0, res["errcode"])

    def test_external_contact_add_group_welcome_template(self):
        with HTTMock(wechat_api_mock):
            template = {
                "text": {"content": "亲爱的%NICKNAME%用户，你好"},
                "image": {
                    "media_id": "MEDIA_ID",
                    "pic_url": "http://p.qpic.cn/pic_wework/3474110808/7a6344sdadfwehe42060/0",
                },
                "link": {
                    "title": "消息标题",
                    "picurl": "https://example.pic.com/path",
                    "desc": "消息描述",
                    "url": "https://example.link.com/path",
                },
                "miniprogram": {
                    "title": "消息标题",
                    "pic_media_id": "MEDIA_ID",
                    "appid": "wx8bd80126147dfAAA",
                    "page": "/path/index",
                },
            }
            res = self.client.external_contact.add_group_welcome_template(
                template=template,
                agentid=1000014,
            )
            self.assertEqual(0, res["errcode"])

    def test_external_contact_update_group_welcome_template(self):
        with HTTMock(wechat_api_mock):
            template = {
                "text": {"content": "文本消息内容"},
                "image": {
                    "media_id": "MEDIA_ID",
                    "pic_url": "http://p.qpic.cn/pic_wework/3474110808/7a6344sdadfwehe42060/0",
                },
                "link": {
                    "title": "消息标题",
                    "picurl": "https://example.pic.com/path",
                    "desc": "消息描述",
                    "url": "https://example.link.com/path",
                },
                "miniprogram": {
                    "title": "消息标题",
                    "pic_media_id": "MEDIA_ID",
                    "appid": "wx8bd80126147df384",
                    "page": "/path/index",
                },
            }
            res = self.client.external_contact.update_group_welcome_template(
                template=template,
                template_id="msgXXXXXXX",
                agentid=1000014,
            )
            self.assertEqual(0, res["errcode"])

    def test_external_contact_get_group_welcome_template(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.get_group_welcome_template(template_id="msgXXXXXXX")
            self.assertEqual(0, res["errcode"])

    def test_external_contact_del_group_welcome_template(self):
        with HTTMock(wechat_api_mock):
            res = self.client.external_contact.del_group_welcome_template(template_id="msgXXXXXXX", agentid=1000014)
            self.assertEqual(0, res["errcode"])

    def test_oa_get_dial_record(self):
        with HTTMock(wechat_api_mock):
            res = self.client.oa.get_dial_record(start_time=1536508800, end_time=1536940800, offset=0, limit=100)
            self.assertIsInstance(res, dict, msg="the returned result should be dict type")
            self.assertEqual(0, res["errcode"])

    def test_os_get_dial_record_with_invalid_timestamp(self):
        with HTTMock(wechat_api_mock):
            self.assertRaises(
                ValueError,
                self.client.oa.get_dial_record,
                start_time=1536940800,
                end_time=1536508800,
                offset=0,
                limit=100,
            )

    def test_oa_get_checkin_data(self):
        with HTTMock(wechat_api_mock):
            res = self.client.oa.get_checkin_data(
                data_type=3, start_time=1492617600, end_time=1492790400, userid_list=["james", "paul"]
            )
            self.assertIsInstance(res, dict, msg="the returned result should be dict type")
            self.assertEqual(0, res["errcode"])

    def test_oa_get_checkin_data_with_invalid_datatype(self):
        with HTTMock(wechat_api_mock):
            self.assertRaises(
                ValueError,
                self.client.oa.get_checkin_data,
                data_type=5,
                start_time=1492617600,
                end_time=1492790400,
                userid_list=["james", "paul"],
            )

    def test_oa_get_checkin_data_with_invalid_timestamp(self):
        with HTTMock(wechat_api_mock):
            self.assertRaises(
                ValueError,
                self.client.oa.get_checkin_data,
                data_type=5,
                start_time=1492790400,
                end_time=1492617600,
                userid_list=["james", "paul"],
            )

    def test_oa_get_checkin_option(self):
        with HTTMock(wechat_api_mock):
            res = self.client.oa.get_checkin_option(datetime=1511971200, userid_list=["james", "paul"])
            self.assertIsInstance(res, dict, msg="the returned result should be dict type")
            self.assertEqual(0, res["errcode"])

    def test_oa_get_open_approval_data(self):
        with HTTMock(wechat_api_mock):
            res = self.client.oa.get_open_approval_data(third_no="201806010001")
            self.assertIsInstance(res, dict, msg="the returned result should be dict type")
            self.assertEqual(0, res["errcode"])

    def test_invoice_get_info(self):
        with HTTMock(wechat_api_mock):
            res = self.client.invoice.get_info(card_id="CARDID", encrypt_code="ENCRYPTCODE")
            self.assertEqual(0, res["errcode"])

    def test_invoice_get_info_batch(self):
        with HTTMock(wechat_api_mock):
            item_list = [
                {"card_id": "CARDID1", "encrypt_code": "ENCRYPTCODE1"},
                {"card_id": "CARDID2", "encrypt_code": "ENCRYPTCODE2"},
            ]
            res = self.client.invoice.get_info_batch(item_list)
            self.assertEqual(0, res["errcode"])

    def test_invoice_get_info_batch_with_empty_item_list(self):
        with HTTMock(wechat_api_mock):
            self.assertRaises(ValueError, self.client.invoice.get_info_batch, item_list=[])

    def test_invoice_update_status(self):
        with HTTMock(wechat_api_mock):
            card_id = "CARDID"
            encrypt_code = "ENCRYPTCODE"
            reimburse_status = "INVOICE_REIMBURSE_INIT"
            res = self.client.invoice.update_status(card_id, encrypt_code, reimburse_status)
            self.assertEqual(0, res["errcode"])

    def test_invoice_update_status_with_empty_status(self):
        with HTTMock(wechat_api_mock):
            self.assertRaises(
                ValueError,
                self.client.invoice.update_status,
                card_id="CARDID",
                encrypt_code="ENCRYPTCODE",
                reimburse_status="",
            )

    def test_invoice_update_status_with_invalid_status(self):
        with HTTMock(wechat_api_mock):
            self.assertRaises(
                ValueError,
                self.client.invoice.update_status,
                card_id="CARDID",
                encrypt_code="ENCRYPTCODE",
                reimburse_status="INVALID_STATUS",
            )

    def test_invoice_update_status_batch(self):
        with HTTMock(wechat_api_mock):
            openid = "OPENID"
            reimburse_status = "INVOICE_REIMBURSE_INIT"
            invoice_list = [
                {"card_id": "cardid_1", "encrypt_code": "encrypt_code_1"},
                {"card_id": "cardid_2", "encrypt_code": "encrypt_code_2"},
            ]
            res = self.client.invoice.update_status_batch(openid, reimburse_status, invoice_list)
            self.assertEqual(0, res["errcode"])

    def test_invoice_update_status_batch_with_invalid_status(self):
        with HTTMock(wechat_api_mock):
            openid = "OPENID"
            reimburse_status = ""
            invoice_list = [
                {"card_id": "cardid_1", "encrypt_code": "encrypt_code_1"},
                {"card_id": "cardid_2", "encrypt_code": "encrypt_code_2"},
            ]
            self.assertRaises(
                ValueError,
                self.client.invoice.update_status_batch,
                openid=openid,
                reimburse_status=reimburse_status,
                invoice_list=invoice_list,
            )

    def test_invoice_update_status_batch_with_empty_invoice_list(self):
        with HTTMock(wechat_api_mock):
            openid = "OPENID"
            reimburse_status = "INVOICE_REIMBURSE_INIT"
            invoice_list = []
            self.assertRaises(
                ValueError,
                self.client.invoice.update_status_batch,
                openid=openid,
                reimburse_status=reimburse_status,
                invoice_list=invoice_list,
            )
