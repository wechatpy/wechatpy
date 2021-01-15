# -*- coding: utf-8 -*-


from wechatpy.client.api.base import BaseWeChatAPI


class WeChatUser(BaseWeChatAPI):
    def get(self, user_id, lang="zh_CN"):
        """
        获取用户基本信息（包括UnionID机制）
        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140839

        :param user_id: 普通用户的标识，对当前公众号唯一
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            user = client.user.get('openid')

        """
        assert lang in (
            "zh_CN",
            "zh_TW",
            "en",
        ), "lang can only be one of \
            zh_CN, zh_TW, en language codes"
        return self._get("user/info", params={"openid": user_id, "lang": lang})

    def get_followers(self, first_user_id=None):
        """
        获取一页用户列表(当关注用户过多的情况下，这个接口只会返回一部分用户)

        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140840

        :param first_user_id: 可选。第一个拉取的 OPENID，不填默认从头开始拉取
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            followers = client.user.get_followers()

        """
        params = {}
        if first_user_id:
            params["next_openid"] = first_user_id
        return self._get("user/get", params=params)

    def iter_followers(self, first_user_id=None):
        """
        获取所有的用户openid列表

        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140840

        :return: 返回一个迭代器，可以用for进行循环，得到openid

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            for openid in client.user.iter_followers():
                print(openid)

        """
        while True:
            follower_data = self.get_followers(first_user_id)
            first_user_id = follower_data["next_openid"]
            # 微信有个bug(或者叫feature)，没有下一页，也返回next_openid这个字段
            # 所以要通过total_count和data的长度比较判断(比较麻烦，并且不稳定)
            # 或者获得结果前先判断data是否存在
            if "data" not in follower_data:
                return
            for openid in follower_data["data"]["openid"]:
                yield openid
            if not first_user_id:
                return

    def update_remark(self, user_id, remark):
        """
        设置用户备注名

        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140838

        :param user_id: 用户标识
        :param remark: 新的备注名，长度必须小于30字符
        :return: 返回的 JSON 数据包

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            client.user.update_remark('openid', 'Remark')

        """
        return self._post("user/info/updateremark", data={"openid": user_id, "remark": remark})

    def get_group_id(self, user_id):
        """
        获取用户所在分组 ID

        详情请参考
        http://mp.weixin.qq.com/wiki/0/56d992c605a97245eb7e617854b169fc.html

        :param user_id: 用户 ID
        :return: 用户所在分组 ID

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            group_id = client.user.get_group_id('openid')

        """
        res = self._post(
            "groups/getid",
            data={"openid": user_id},
            result_processor=lambda x: x["groupid"],
        )
        return res

    def get_batch(self, user_list):
        """
        批量获取用户基本信息
        开发者可通过该接口来批量获取用户基本信息。最多支持一次拉取100条。

        详情请参考
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140839

        :param user_list: user_list，支持“使用示例”中两种输入格式
        :return: 用户信息的 list

        使用示例::

            from wechatpy import WeChatClient

            client = WeChatClient('appid', 'secret')
            users = client.user.get_batch(['openid1', 'openid2'])
            users = client.user.get_batch([
              {'openid': 'openid1', 'lang': 'zh-CN'},
              {'openid': 'openid2', 'lang': 'en'},
            ])

        """
        if all((isinstance(x, str) for x in user_list)):
            user_list = [{"openid": oid} for oid in user_list]
        res = self._post(
            "user/info/batchget",
            data={"user_list": user_list},
            result_processor=lambda x: x["user_info_list"],
        )
        return res

    def change_openid(self, from_appid, openid_list):
        """微信公众号主体变更迁移用户 openid

        详情请参考
        http://kf.qq.com/faq/170221aUnmmU170221eUZJNf.html

        :param from_appid: 原公众号的 appid
        :param openid_list: 需要转换的openid，这些必须是旧账号目前关注的才行，否则会出错；一次最多100个
        :return: 转换后的 openid 信息列表
        """
        return self._post(
            "changeopenid",
            data={"from_appid": from_appid, "openid_list": openid_list},
            result_processor=lambda x: x["result_list"],
        )
