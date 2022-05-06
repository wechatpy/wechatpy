# -*- coding: utf-8 -*-

import hashlib
import time
import datetime
from operator import itemgetter
from urllib.parse import quote

from optionaldict import optionaldict
from wechatpy.utils import to_binary
from wechatpy.client.api.base import BaseWeChatAPI


class WeChatCustomService(BaseWeChatAPI):
    API_BASE_URL = "https://api.weixin.qq.com/customservice/"

    def add_account(self, account, nickname, password):
        """
        添加客服账号
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Service_Center_messages.html#%E6%B7%BB%E5%8A%A0%E5%AE%A2%E6%9C%8D%E5%B8%90%E5%8F%B7

        :param account: 完整客服账号，格式为：账号前缀@公众号微信号
        :param nickname: 客服昵称，最长6个汉字或12个英文字符
        :param password: 客服账号登录密码
        :return: 返回的 JSON 数据包
        """
        password = to_binary(password)
        password = hashlib.md5(password).hexdigest()
        return self._post(
            "kfaccount/add",
            data={"kf_account": account, "nickname": nickname, "password": password},
        )

    def update_account(self, account, nickname, password):
        """
        修改客服账号
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Service_Center_messages.html#%E4%BF%AE%E6%94%B9%E5%AE%A2%E6%9C%8D%E5%B8%90%E5%8F%B7

        :param account: 完整客服账号，格式为：账号前缀@公众号微信号
        :param nickname: 客服昵称，最长6个汉字或12个英文字符
        :param password: 客服账号登录密码
        :return: 返回的 JSON 数据包
        """
        password = to_binary(password)
        password = hashlib.md5(password).hexdigest()
        return self._post(
            "kfaccount/update",
            data={"kf_account": account, "nickname": nickname, "password": password},
        )

    def delete_account(self, account):
        """
        删除客服账号
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Service_Center_messages.html#%E5%88%A0%E9%99%A4%E5%AE%A2%E6%9C%8D%E5%B8%90%E5%8F%B7

        :param account: 完整客服账号，格式为：账号前缀@公众号微信号
        :return: 返回的 JSON 数据包
        """
        params_data = [
            f"access_token={quote(self.access_token)}",
            f"kf_account={quote(to_binary(account), safe=b'/@')}",
        ]
        params = "&".join(params_data)
        return self._get("kfaccount/del", params=params)

    def get_accounts(self):
        """
        获取所有客服账号
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Service_Center_messages.html#%E8%8E%B7%E5%8F%96%E6%89%80%E6%9C%89%E5%AE%A2%E6%9C%8D%E8%B4%A6%E5%8F%B7

        :return: 客服账号列表
        """
        res = self._get("getkflist", result_processor=itemgetter("kf_list"))
        return res

    def upload_headimg(self, account, media_file):
        """
        设置客服帐号的头像
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Service_Center_messages.html#%E8%AE%BE%E7%BD%AE%E5%AE%A2%E6%9C%8D%E5%B8%90%E5%8F%B7%E7%9A%84%E5%A4%B4%E5%83%8F

        :param account: 完整客服帐号，格式为：帐号前缀@公众号微信号
        :param media_file: 要上传的头像文件，一个 File-Object
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "kfaccount/uploadheadimg",
            params={"kf_account": account},
            files={"media": media_file},
        )

    def get_online_accounts(self):
        """
        获取在线客服接待信息
        详情请参考
        http://mp.weixin.qq.com/wiki/9/6fff6f191ef92c126b043ada035cc935.html

        :return: 客服接待信息列表
        """
        res = self._get(
            "getonlinekflist",
            result_processor=itemgetter("kf_online_list"),
        )
        return res

    def create_session(self, openid, account, text=None):
        """
        多客服创建会话
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Customer_Service/Session_control.html

        :param openid: 客户 openid
        :param account: 完整客服帐号，格式为：帐号前缀@公众号微信号
        :param text: 附加信息，可选
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(openid=openid, kf_account=account, text=text)
        return self._post("kfsession/create", data=data)

    def close_session(self, openid, account, text=None):
        """
        多客服关闭会话
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Customer_Service/Session_control.html

        :param openid: 客户 openid
        :param account: 完整客服帐号，格式为：帐号前缀@公众号微信号
        :param text: 附加信息，可选
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(openid=openid, kf_account=account, text=text)
        return self._post("kfsession/close", data=data)

    def get_session(self, openid):
        """
        获取客户的会话状态，如果不存在，则 kf_account 为空
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Customer_Service/Session_control.html

        :param openid: 粉丝的 openid
        :return: 返回的 JSON 数据包
        """
        return self._get(
            "kfsession/getsession",
            params={"openid": openid},
        )

    def get_session_list(self, account):
        """
        获取客服的会话列表
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Customer_Service/Session_control.html

        :param account: 完整客服帐号，格式为：帐号前缀@公众号微信号
        :return: 客服的会话列表
        """
        res = self._get(
            "kfsession/getsessionlist",
            params={"kf_account": account},
            result_processor=itemgetter("sessionlist"),
        )
        return res

    def get_wait_case(self):
        """
        获取未接入会话列表
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Customer_Service/Session_control.html

        :return: 返回的 JSON 数据包
        """
        return self._get("kfsession/getwaitcase")

    def get_records(self, start_time, end_time, msgid=1, number=10000):
        """
        获取客服聊天记录
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Customer_Service/Obtain_chat_transcript.html

        :param start_time: 查询开始时间，UNIX 时间戳
        :param end_time: 查询结束时间，UNIX 时间戳，每次查询不能跨日查询
        :param msgid: 消息id顺序从小到大，从1开始
        :param number: 每次获取条数，最多10000条

        :return: 返回的 JSON 数据包
        """
        if isinstance(start_time, datetime.datetime):
            start_time = time.mktime(start_time.timetuple())
        if isinstance(end_time, datetime.datetime):
            end_time = time.mktime(end_time.timetuple())
        record_data = {
            "starttime": int(start_time),
            "endtime": int(end_time),
            "msgid": msgid,
            "number": number,
        }
        res = self._post(
            "msgrecord/getmsglist",
            data=record_data,
        )
        return res
