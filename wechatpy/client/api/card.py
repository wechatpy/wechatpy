# -*- coding: utf-8 -*-
from operator import itemgetter


from wechatpy.client.api.base import BaseWeChatAPI


class WeChatCard(BaseWeChatAPI):

    API_BASE_URL = "https://api.weixin.qq.com/"

    def create(self, card_data):
        """
        创建卡券

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Create_a_Coupon_Voucher_or_Card.html#8

        :param card_data: 卡券信息
        :return: 创建的卡券 ID
        """
        result = self._post("card/create", data=card_data, result_processor=itemgetter("card_id"))
        return result

    def batch_add_locations(self, location_data):
        """
        ⚠️已废弃
        批量导入门店信息

        :param location_data: 门店信息
        :return: 门店 ID 列表，插入失败的门店元素值为 -1
        """
        result = self._post(
            "card/location/batchadd",
            data=location_data,
            result_processor=itemgetter("location_id_list"),
        )
        return result

    def batch_get_locations(self, offset=0, count=0):
        """
        ⚠️已废弃
        批量获取门店信息
        """
        return self._post("card/location/batchget", data={"offset": offset, "count": count})

    def get_colors(self):
        """
        获得卡券的最新颜色列表，用于创建卡券
        目前微信提供包括十四种色值供开发者使用。

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Create_a_Coupon_Voucher_or_Card.html#7

        :return: 颜色列表
        """
        return [
            "Color010",  # "#63b359"
            "Color020",  # "#2c9f67"
            "Color030",  # "#509fc9"
            "Color040",  # "#5885cf"
            "Color050",  # "#9062c0"
            "Color060",  # "#d09a45"
            "Color070",  # "#e4b138"
            "Color080",  # "#ee903c"
            "Color081",  # "#f08500"
            "Color082",  # "#a9d92d"
            "Color090",  # "#dd6549"
            "Color100",  # "#cc463d"
            "Color101",  # "#cf3e36"
            "Color102",  # "#5E6671"
        ]

    def create_qrcode(self, qrcode_data):
        """
        创建卡券二维码

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Distributing_Coupons_Vouchers_and_Cards.html#0

        :param qrcode_data: 二维码信息
        :return: 二维码 ticket，可使用 :func:show_qrcode 换取二维码文件
        """
        result = self._post(
            "card/qrcode/create",
            data=qrcode_data,
            result_processor=itemgetter("ticket"),
        )
        return result

    def create_landingpage(self, buffer_data):
        """
        创建货架

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Distributing_Coupons_Vouchers_and_Cards.html#3

        """
        result = self._post("card/landingpage/create", data=buffer_data)
        return result

    def get_html(self, card_id):
        """
        图文消息群发卡券

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Distributing_Coupons_Vouchers_and_Cards.html#6
        """
        result = self._post(
            "card/mpnews/gethtml",
            data={"card_id": card_id},
            result_processor=itemgetter("content"),
        )
        return result

    def consume_code(self, code, card_id=None):
        """
        消耗 code

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Redeeming_a_coupon_voucher_or_card.html#0
        """
        card_data = {"code": code}
        if card_id:
            card_data["card_id"] = card_id
        return self._post("card/code/consume", data=card_data)

    def decrypt_code(self, encrypt_code):
        """
        解码加密的 code

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Redeeming_a_coupon_voucher_or_card.html#0
        """
        result = self._post(
            "card/code/decrypt",
            data={"encrypt_code": encrypt_code},
            result_processor=itemgetter("code"),
        )
        return result

    def delete(self, card_id):
        """
        删除卡券

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Managing_Coupons_Vouchers_and_Cards.html#7
        """
        return self._post("card/delete", data={"card_id": card_id})

    def get_code(self, code, card_id=None, check_consume=True):
        """
        查询 code 信息

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Managing_Coupons_Vouchers_and_Cards.html#0
        """
        card_data = {"code": code}
        if card_id:
            card_data["card_id"] = card_id
        if not check_consume:
            card_data["check_consume"] = check_consume
        return self._post("card/code/get", data=card_data)

    def get_card_list(self, openid, card_id=None):
        """
        用于获取用户卡包里的，属于该appid下的卡券。

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Managing_Coupons_Vouchers_and_Cards.html#1
        """
        card_data = {"openid": openid}
        if card_id:
            card_data["card_id"] = card_id
        return self._post("card/user/getcardlist", data=card_data)

    def batch_get(self, offset=0, count=50, status_list=None):
        """
        批量查询卡券信息

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Managing_Coupons_Vouchers_and_Cards.html#3

        :param offset: 查询卡列表的起始偏移量，从0开始，即offset: 5是指从从列表里的第六个开始读取。
        :param count: 需要查询的卡片的数量（数量最大50）
        :param status_list: 支持开发者拉出指定状态的卡券列表
        """
        if count > 50:
            raise ValueError("count cannot be greater than 50")
        card_data = {"offset": offset, "count": count}
        if status_list:
            card_data["status_list"] = status_list
        return self._post("card/batchget", data=card_data)

    def get(self, card_id):
        """
        查询卡券详情

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Managing_Coupons_Vouchers_and_Cards.html#2
        """
        result = self._post("card/get", data={"card_id": card_id}, result_processor=itemgetter("card"))
        return result

    def update_code(self, card_id, old_code, new_code):
        """
        更新卡券 code

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Managing_Coupons_Vouchers_and_Cards.html#6

        :param card_id: 卡券ID。自定义 Code 码卡券为必填
        :param old_code: 需变更的 Code 码
        :param new_code: 变更后的有效 Code 码
        """
        return self._post(
            "card/code/update",
            data={"card_id": card_id, "code": old_code, "new_code": new_code},
        )

    def invalid_code(self, code, card_id=None):
        """
        设置卡券失效

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Managing_Coupons_Vouchers_and_Cards.html#8
        """
        card_data = {"code": code}
        if card_id:
            card_data["card_id"] = card_id
        return self._post("card/code/unavailable", data=card_data)

    def update(self, card_data):
        """
        更新卡券信息

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Managing_Coupons_Vouchers_and_Cards.html#4
        """
        return self._post("card/update", data=card_data)

    def set_paycell(self, card_id, is_open):
        """
        设置买单接口

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Create_a_Coupon_Voucher_or_Card.html#12
        """
        return self._post("card/paycell/set", data={"card_id": card_id, "is_open": is_open})

    def set_test_whitelist(self, openids=None, usernames=None):
        """
        设置卡券测试用户白名单

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Distributing_Coupons_Vouchers_and_Cards.html#12
        """
        openids = openids or []
        usernames = usernames or []
        return self._post("card/testwhitelist/set", data={"openid": openids, "username": usernames})

    def activate_membercard(self, membership_number, code, **kwargs):
        """
        激活会员卡 - 接口激活方式

        详情请参见
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Membership_Cards/Create_a_membership_card.html#14

        参数示例：
        {
            "init_bonus": 100,
            "init_bonus_record":"旧积分同步",
            "init_balance": 200,
            "membership_number": "AAA00000001",
            "code": "12312313",
            "card_id": "xxxx_card_id",
            "background_pic_url": "https://mmbiz.qlogo.cn/mmbiz/0?wx_fmt=jpeg",
            "init_custom_field_value1": "xxxxx",
            "init_custom_field_value2": "xxxxx",
            "init_custom_field_value3": "xxxxx"
        }

        返回示例：
        {"errcode":0,   "errmsg":"ok"}

        :param membership_number: 必填，会员卡编号，由开发者填入，作为序列号显示在用户的卡包里。可与Code码保持等值
        :param code: 必填，领取会员卡用户获得的code
        :return: 参见返回示例
        """
        kwargs["membership_number"] = membership_number
        kwargs["code"] = code
        return self._post("card/membercard/activate", data=kwargs)

    def update_membercard(self, code, card_id, **kwargs):
        """
        更新会员信息

        详情请参见
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Membership_Cards/Create_a_membership_card.html#18

        注意事项：
        1.开发者可以同时传入add_bonus和bonus解决由于同步失败带来的幂等性问题。同时传入add_bonus和bonus时
            add_bonus作为积分变动消息中的变量值，而bonus作为卡面上的总积分额度显示。余额变动同理。
        2.开发者可以传入is_notify_bonus控制特殊的积分对账变动不发送消息，余额变动同理。

        参数示例：
        {
            "code": "179011264953",
            "card_id": "p1Pj9jr90_SQRaVqYI239Ka1erkI",
            "background_pic_url": "https://mmbiz.qlogo.cn/mmbiz/0?wx_fmt=jpeg",
            "record_bonus": "消费30元，获得3积分",
            "bonus": 3000,
            "add_bonus": 30,
            "balance": 3000,
            "add_balance": -30,
            "record_balance": "购买焦糖玛琪朵一杯，扣除金额30元。",
            "custom_field_value1": "xxxxx"，
            "custom_field_value2": "xxxxx"，
            "notify_optional": {
                "is_notify_bonus": true,
                "is_notify_balance": true,
                "is_notify_custom_field1":true
            }
        }

        返回示例：
        {
            "errcode": 0,
            "errmsg": "ok",
            "result_bonus": 100,
            "result_balance": 200,
            "openid": "oFS7Fjl0WsZ9AMZqrI80nbIq8xrA"
        }

        :param code: 必填，卡券Code码
        :param card_id: 必填，卡券ID
        :param kwargs: 其他非必填字段，包含则更新对应字段。详情参见微信文档 “7 更新会员信息” 部分
        :return: 参见返回示例
        """
        kwargs.update(
            {
                "code": code,
                "card_id": card_id,
            }
        )
        return self._post("card/membercard/updateuser", data=kwargs)

    def get_membercard_user_info(self, card_id, code):
        """
        查询会员卡的会员信息

        详情请参见
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Membership_Cards/Create_a_membership_card.html#16

        :param card_id: 查询会员卡的 Card ID
        :param code: 所查询用户领取到的 code 值
        :return: 会员信息，包括激活资料、积分信息以及余额等信息
        """
        return self._post(
            "card/membercard/userinfo/get",
            data={
                "card_id": card_id,
                "code": code,
            },
        )

    def add_pay_giftcard(self, base_info, extra_info, is_membercard):
        """
        新增支付后投放卡券的规则，支持支付后领卡，支付后赠券

        详情请参见
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Membership_Cards/Manage_Member_Card.html#4

        :param base_info: 营销规则结构体
        :type base_info: dict
        :param extra_info: 支付规则结构体
        :type extra_info: dict
        :param is_membercard: 本次规则是否是领卡。（领卡传入 True, 赠券传入 False）
        :type is_membercard: bool
        :return: 规则 ID, 设置成功的列表，以及设置失败的列表
        """
        if is_membercard:
            rule_key = "member_rule"
            rule_type = "RULE_TYPE_PAY_MEMBER_CARD"
        else:
            rule_key = "single_pay"
            rule_type = "RULE_TYPE_SINGLE_PAY"
        return self._post(
            "card/paygiftcard/add",
            data={
                "rule_info": {
                    "type": rule_type,
                    "base_info": base_info,
                    rule_key: extra_info,
                }
            },
        )

    def del_pay_giftcard(self, rule_id):
        """
        删除支付后投放卡券的规则

        详情请参见
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Membership_Cards/Manage_Member_Card.html#4

        :param rule_id: 支付即会员的规则 ID
        """
        return self._post(
            "card/paygiftcard/delete",
            data={
                "rule_id": rule_id,
            },
        )

    def get_pay_giftcard(self, rule_id):
        """
        查询支付后投放卡券的规则

        详情请参见
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Membership_Cards/Manage_Member_Card.html#4

        :param rule_id: 支付即会员的规则 ID
        :return: 支付后投放卡券的规则
        :rtype: dict
        """
        return self._post(
            "card/paygiftcard/getbyid",
            data={
                "rule_id": rule_id,
            },
            result_processor=itemgetter("rule_info"),
        )

    def batch_get_pay_giftcard(self, effective=True, offset=0, count=10):
        """
        批量查询支付后投放卡券的规则

        详情请参见
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Membership_Cards/Manage_Member_Card.html#4

        :param effective: 是否仅查询生效的规则
        :type effective: bool
        :param offset: 起始偏移量
        :type offset: int
        :param count: 查询的数量
        :type count: int
        :return: 支付后投放卡券规则的总数，以及查询到的列表
        """
        return self._post(
            "card/paygiftcard/batchget",
            data={
                "type": "RULE_TYPE_PAY_MEMBER_CARD",
                "effective": effective,
                "offset": offset,
                "count": count,
            },
        )

    def update_movie_ticket(
        self,
        code,
        ticket_class,
        show_time,
        duration,
        screening_room,
        seat_number,
        card_id=None,
    ):
        """
        更新电影票

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Special_ticket.html#7
        """
        ticket = {
            "code": code,
            "ticket_class": ticket_class,
            "show_time": show_time,
            "duration": duration,
            "screening_room": screening_room,
            "seat_number": seat_number,
        }
        if card_id:
            ticket["card_id"] = card_id
        return self._post("card/movieticket/updateuser", data=ticket)

    def checkin_boardingpass(
        self,
        code,
        passenger_name,
        seat_class,
        etkt_bnr,
        seat="",
        gate="",
        boarding_time=None,
        is_cancel=False,
        qrcode_data=None,
        card_id=None,
    ):
        """
        飞机票接口

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Special_ticket.html#3
        """
        data = {
            "code": code,
            "passenger_name": passenger_name,
            "class": seat_class,
            "etkt_bnr": etkt_bnr,
            "seat": seat,
            "gate": gate,
            "is_cancel": is_cancel,
        }
        if boarding_time:
            data["boarding_time"] = boarding_time
        if qrcode_data:
            data["qrcode_data"] = qrcode_data
        if card_id:
            data["card_id"] = card_id
        return self._post("card/boardingpass/checkin", data=data)

    def update_luckymoney_balance(self, code, balance, card_id=None):
        """
        ⚠️已废弃
        更新红包余额
        """
        card_data = {"code": code, "balance": balance}
        if card_id:
            card_data["card_id"] = card_id
        return self._post("card/luckymoney/updateuserbalance", data=card_data)

    def get_redirect_url(self, url, encrypt_code, card_id):
        """
        获取卡券跳转外链
        """
        from wechatpy.utils import WeChatSigner

        code = self.decrypt_code(encrypt_code)

        signer = WeChatSigner()
        signer.add_data(self.secret)
        signer.add_data(code)
        signer.add_data(card_id)
        signature = signer.signature

        return f"{url}?encrypt_code={encrypt_code}&card_id={card_id}&signature={signature}"

    def deposit_code(self, card_id, codes):
        """
        导入code
        """
        card_data = {"card_id": card_id, "code": codes}
        return self._post("card/code/deposit", data=card_data)

    def get_deposit_count(self, card_id):
        """
        查询导入code数目
        """
        card_data = {
            "card_id": card_id,
        }
        return self._post("card/code/getdepositcount", data=card_data)

    def check_code(self, card_id, codes):
        """
        核查code
        """
        card_data = {"card_id": card_id, "code": codes}
        return self._post("card/code/checkcode", data=card_data)

    def modify_stock(self, card_id, n):
        """
        修改库存
        """
        if n == 0:
            return
        card_data = {
            "card_id": card_id,
        }
        if n > 0:
            card_data["increase_stock_value"] = n
        elif n < 0:
            card_data["reduce_stock_value"] = -n
        return self._post("card/modifystock", data=card_data)

    def get_activate_url(self, card_id, outer_str=None):
        """
        获取开卡插件 Url, 内含调用开卡插件所需的参数
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1499332673_Unm7V

        :param card_id: 会员卡的card_id
        :param outer_str: 渠道值，用于统计本次领取的渠道参数
        :return: 内含调用开卡插件所需的参数的 Url
        """
        return self._post(
            "card/membercard/activate/geturl",
            data={
                "card_id": card_id,
                "outer_str": outer_str,
            },
            result_processor=lambda x: x["url"],
        )

    def get_activate_info(self, activate_ticket):
        """
        获取用户开卡时提交的信息

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Membership_Cards/Create_a_membership_card.html#16

        :param activate_ticket: 跳转型开卡组件开卡后回调中的激活票据，可以用来获取用户开卡资料
        :return: 用户开卡时填写的字段值
        """
        return self._post(
            "card/membercard/activatetempinfo/get",
            data={
                "activate_ticket": activate_ticket,
            },
            result_processor=itemgetter("info"),
        )

    def set_activate_user_form(self, card_id, **kwargs):
        """
        设置开卡字段接口

        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Membership_Cards/Create_a_membership_card.html#16

        "6 激活会员卡" -> "6.2 一键激活" -> "步骤二：设置开卡字段接口"

        参数示例：
        {
            "card_id": "pbLatjnrwUUdZI641gKdTMJzHGfc",
            "service_statement": {
                "name": "会员守则",
                "url": "https://www.qq.com"
            },
            "bind_old_card": {
                "name": "老会员绑定",
                "url": "https://www.qq.com"
            },
            "required_form": {
                "can_modify"：false,
                "rich_field_list": [
                    {
                        "type": "FORM_FIELD_RADIO",
                        "name": "兴趣",
                        "values": [
                            "钢琴",
                            "舞蹈",
                            "足球"
                        ]
                    },
                    {
                        "type": "FORM_FIELD_SELECT",
                        "name": "喜好",
                        "values": [
                            "郭敬明",
                            "韩寒",
                            "南派三叔"
                        ]
                    },
                    {
                        "type": "FORM_FIELD_CHECK_BOX",
                        "name": "职业",
                        "values": [
                            "赛车手",
                            "旅行家"
                        ]
                    }
                ],
                "common_field_id_list": [
                    "USER_FORM_INFO_FLAG_MOBILE"
                ]
            },
            "optional_form": {
                "can_modify"：false,
                "common_field_id_list": [
                    "USER_FORM_INFO_FLAG_LOCATION",
                    "USER_FORM_INFO_FLAG_BIRTHDAY"
                ],
                "custom_field_list": [
                    "喜欢的电影"
                ]
            }
        }
        common_field_id_list 值见常量 `wechatpy.constants.UserFormInfoFlag`

        :param card_id: 卡券ID
        :param kwargs: 其他非必填参数，见微信文档
        """
        kwargs["card_id"] = card_id
        return self._post("card/membercard/activateuserform/set", data=kwargs)
