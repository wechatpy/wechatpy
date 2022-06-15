# -*- coding: utf-8 -*-
"""
    wechatpy.events
    ~~~~~~~~~~~~~~~~

    This module contains all the events WeChat callback uses.

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
from typing import Dict, List

from wechatpy.fields import (
    Base64DecodeField,
    BaseField,
    DateTimeField,
    FloatField,
    IntegerField,
    StringField,
)
from wechatpy.messages import BaseMessage

EVENT_TYPES = {}


class BaseEvent(BaseMessage):
    """Base class for all events"""

    type = "event"
    event = ""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # 注册子类
        if cls.event:
            EVENT_TYPES[cls.event] = cls


class SubscribeEvent(BaseEvent):
    """
    用户关注事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_event_pushes.html
    """

    event = "subscribe"
    key = StringField("EventKey", "")


class UnsubscribeEvent(BaseEvent):
    """
    用户取消关注事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_event_pushes.html
    """

    event = "unsubscribe"


class SubscribeScanEvent(BaseEvent):
    """
    用户扫描二维码关注事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_event_pushes.html
    """

    event = "subscribe_scan"
    scene_id = StringField("EventKey")
    ticket = StringField("Ticket")


class ScanEvent(BaseEvent):
    """
    用户扫描二维码事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_event_pushes.html
    """

    event = "scan"
    scene_id = StringField("EventKey")
    ticket = StringField("Ticket")


class LocationEvent(BaseEvent):
    """
    上报地理位置事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_event_pushes.html
    """

    event = "location"
    latitude = FloatField("Latitude", 0.0)
    longitude = FloatField("Longitude", 0.0)
    precision = FloatField("Precision", 0.0)


class ClickEvent(BaseEvent):
    """
    点击菜单拉取消息事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_event_pushes.html
    """

    event = "click"
    key = StringField("EventKey")


class ViewEvent(BaseEvent):
    """
    点击菜单跳转链接事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_event_pushes.html
    """

    event = "view"
    url = StringField("EventKey")


class MassSendJobFinishEvent(BaseEvent):
    """
    群发消息任务完成事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Batch_Sends_and_Originality_Checks.html#7
    """

    id = IntegerField("MsgID", 0)
    event = "masssendjobfinish"
    status = StringField("Status")
    total_count = IntegerField("TotalCount", 0)
    filter_count = IntegerField("FilterCount", 0)
    sent_count = IntegerField("SentCount", 0)
    error_count = IntegerField("ErrorCount", 0)


class TemplateSendJobFinishEvent(BaseEvent):
    """
    模板消息任务完成事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html#6
    """

    id = IntegerField("MsgID")
    event = "templatesendjobfinish"
    status = StringField("Status")


class SubscribeMsgPopupEvent(BaseEvent):
    """
    用户操作订阅通知弹窗事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Subscription_Messages/api.html
    """

    event = "subscribe_msg_popup_event"
    subscribes_info = BaseField("SubscribeMsgPopupEvent", {})

    @property
    def subscribes(self) -> List[Dict]:
        """
        返回值参考:
        [
          {
            "TemplateId": "VRR0UEO9VJOLs0MHlU0OilqX6MVFDwH3_3gz3Oc0NIc",
            "SubscribeStatusString": "accept",
            "PopupScene": 2
          },
          {
            "TemplateId": "9nLIlbOQZC5Y89AZteFEux3WCXRRRG5Wfzkpssu4bLI",
            "SubscribeStatusString": "reject",
            "PopupScene": 2
          },
        ]
        """
        subscribes = self.subscribes_info["List"]
        if not isinstance(subscribes, list):
            subscribes = [subscribes]
        return subscribes


class SubscribeMsgChangeEvent(BaseEvent):
    """
    用户管理订阅通知事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Subscription_Messages/api.html
    """

    event = "subscribe_msg_change_event"
    subscribes_info = BaseField("SubscribeMsgChangeEvent", {})

    @property
    def subscribes(self) -> List[Dict]:
        """
        返回值参考:
        [
          {
            "TemplateId": "VRR0UEO9VJOLs0MHlU0OilqX6MVFDwH3_3gz3Oc0NIc",
            "SubscribeStatusString": "accept",
          },
          {
            "TemplateId": "9nLIlbOQZC5Y89AZteFEux3WCXRRRG5Wfzkpssu4bLI",
            "SubscribeStatusString": "reject",
          },
        ]
        """
        subscribes = self.subscribes_info["List"]
        if not isinstance(subscribes, list):
            subscribes = [subscribes]
        return subscribes


class SubscribeMsgSentEvent(BaseEvent):
    """
    发送订阅通知事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Subscription_Messages/api.html
    """

    event = "subscribe_msg_sent_event"
    subscribes_info = BaseField("SubscribeMsgSentEvent", {})

    @property
    def subscribes(self) -> List[Dict]:
        """
        返回值参考:
        [
          {
            "TemplateId": "VRR0UEO9VJOLs0MHlU0OilqX6MVFDwH3_3gz3Oc0NIc",
            "MsgID": "1700827132819554304",
            "ErrorCode": "0",
            "ErrorStatus": "success",
          },
        ]
        """
        subscribes = self.subscribes_info["List"]
        if not isinstance(subscribes, list):
            subscribes = [subscribes]
        return subscribes


class BaseScanCodeEvent(BaseEvent):
    key = StringField("EventKey")
    scan_code_info = BaseField("ScanCodeInfo", {})

    @property
    def scan_type(self):
        return self.scan_code_info["ScanType"]

    @property
    def scan_result(self):
        return self.scan_code_info["ScanResult"]


class ScanCodePushEvent(BaseScanCodeEvent):
    """
    扫码推事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Custom_Menus/Custom_Menu_Push_Events.html
    """

    event = "scancode_push"


class ScanCodeWaitMsgEvent(BaseScanCodeEvent):
    """
    扫码推事件且弹出“消息接收中”提示框的事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Custom_Menus/Custom_Menu_Push_Events.html
    """

    event = "scancode_waitmsg"


class BasePictureEvent(BaseEvent):
    key = StringField("EventKey")
    pictures_info = BaseField("SendPicsInfo", {})

    @property
    def count(self):
        return int(self.pictures_info["Count"])

    @property
    def pictures(self):
        if self.pictures_info["PicList"]:
            items = self.pictures_info["PicList"]["item"]
            if self.count > 1:
                return items
            return [items]
        return []


class PicSysPhotoEvent(BasePictureEvent):
    """
    弹出系统拍照发图的事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Custom_Menus/Custom_Menu_Push_Events.html
    """

    event = "pic_sysphoto"


class PicPhotoOrAlbumEvent(BasePictureEvent):
    """
    弹出拍照或者相册发图的事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Custom_Menus/Custom_Menu_Push_Events.html
    """

    event = "pic_photo_or_album"


class PicWeChatEvent(BasePictureEvent):
    """
    弹出微信相册发图器的事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Custom_Menus/Custom_Menu_Push_Events.html
    """

    event = "pic_weixin"


class LocationSelectEvent(BaseEvent):
    """
    弹出地理位置选择器的事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Custom_Menus/Custom_Menu_Push_Events.html
    """

    event = "location_select"
    key = StringField("EventKey")
    location_info = BaseField("SendLocationInfo", {})

    @property
    def location_x(self):
        return self.location_info["Location_X"]

    @property
    def location_y(self):
        return self.location_info["Location_Y"]

    @property
    def location(self):
        return self.location_x, self.location_y

    @property
    def scale(self):
        return self.location_info["Scale"]

    @property
    def label(self):
        return self.location_info["Label"]

    @property
    def poiname(self):
        return self.location_info["Poiname"]


class CardPassCheckEvent(BaseEvent):
    """
    卡券审核事件推送

    https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Coupons_Vouchers_and_Cards_Event_Push_Messages.html#1
    """

    event = "card_pass_check"
    card_id = StringField("CardId")


class CardNotPassCheckEvent(BaseEvent):
    event = "card_not_pass_check"
    card_id = StringField("CardId")
    refuse_reason = StringField("RefuseReason")


class UserGetCardEvent(BaseEvent):
    """
    领取事件推送

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Coupons_Vouchers_and_Cards_Event_Push_Messages.html#2
    """

    event = "user_get_card"
    card_id = StringField("CardId")
    is_given_by_friend = IntegerField("IsGiveByFriend")
    friend = StringField("FriendUserName")
    code = StringField("UserCardCode")
    old_code = StringField("OldUserCardCode")
    outer_id = StringField("OuterId")
    outer_str = StringField("OuterStr")
    is_restore_member_card = IntegerField("IsRestoreMemberCard")
    is_recommend_by_friend = IntegerField("IsRecommendByFriend")
    union_id = StringField("UnionId")


class UserGiftingCardEvent(BaseEvent):
    """
    转赠事件推送

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Coupons_Vouchers_and_Cards_Event_Push_Messages.html#3
    """

    event = "user_gifting_card"
    card_id = StringField("CardId")
    code = StringField("UserCardCode")
    is_return_back = IntegerField("IsReturnBack")
    friend = StringField("FriendUserName")
    is_chat_room = IntegerField("IsChatRoom")


class UserDeleteCardEvent(BaseEvent):
    """
    卡券删除事件推送

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Coupons_Vouchers_and_Cards_Event_Push_Messages.html#4
    """

    event = "user_del_card"
    card_id = StringField("CardId")
    code = StringField("UserCardCode")


class UserConsumeCardEvent(BaseEvent):
    """
    卡券核销事件推送

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Coupons_Vouchers_and_Cards_Event_Push_Messages.html#5
    """

    event = "user_consume_card"
    card_id = StringField("CardId")
    code = StringField("UserCardCode")
    consume_source = StringField("ConsumeSource")
    location_name = StringField("LocationName")
    staff = StringField("StaffOpenId")
    verify_code = StringField("VerifyCode")
    remark_amount = StringField("RemarkAmount")
    outer_str = StringField("OuterStr")


class UserPayFromPayCell(BaseEvent):
    """
    卡券买单事件推送

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Coupons_Vouchers_and_Cards_Event_Push_Messages.html#6
    """

    event = "user_pay_from_pay_cell"
    card_id = StringField("CardId")
    code = StringField("UserCardCode")
    trans_id = StringField("TransId")
    location_id = IntegerField("LocationId")
    fee = IntegerField("Fee")
    original_fee = IntegerField("OriginalFee")


class UserViewCard(BaseEvent):
    """
    进入会员卡事件推送

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Coupons_Vouchers_and_Cards_Event_Push_Messages.html#7
    """

    event = "user_view_card"
    card_id = StringField("CardId")
    code = StringField("UserCardCode")
    outer_str = StringField("OuterStr")


class UserEnterSessionFromCardEvent(BaseEvent):
    """
    从卡券进入公众号会话事件推送

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Coupons_Vouchers_and_Cards_Event_Push_Messages.html#8
    """

    event = "user_enter_session_from_card"
    card_id = StringField("CardId")
    code = StringField("UserCardCode")


class UpdateMemberCard(BaseEvent):
    """
    会员卡内容更新事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Coupons_Vouchers_and_Cards_Event_Push_Messages.html#9
    """

    event = "update_member_card"
    card_id = StringField("CardId")
    code = StringField("UserCardCode")
    modify_bonus = IntegerField("ModifyBonus")
    modify_balance = IntegerField("ModifyBalance")


class CardSkuRemindEvent(BaseEvent):
    """
    卡券库存报警事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Coupons_Vouchers_and_Cards_Event_Push_Messages.html#10
    """

    event = "card_sku_remind"
    card_id = StringField("CardId")
    detail = StringField("Detail")


class CardPayOrderEvent(BaseEvent):
    """
    券点流水详情事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Coupons_Vouchers_and_Cards_Event_Push_Messages.html#11
    """

    event = "card_pay_order"
    order_id = IntegerField("OrderId")
    status = StringField("Status")
    create_order_time = IntegerField("CreateOrderTime")
    pay_finish_time = IntegerField("PayFinishTime")
    description = StringField("Desc")
    free_coin_count = IntegerField("FreeCoinCount")
    pay_coin_count = IntegerField("PayCoinCount")
    refund_free_coin_count = IntegerField("RefundFreeCoinCount")
    refund_pay_coin_count = IntegerField("RefundPayCoinCount")
    order_type = StringField("OrderType")
    memo = StringField("Memo")
    receipt_info = StringField("ReceiptInfo")


class SubmitMembercardUserInfo(BaseEvent):
    """
    会员卡激活事件推送

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Cards_and_Offer/Coupons_Vouchers_and_Cards_Event_Push_Messages.html#12
    """

    event = "submit_membercard_user_info"
    card_id = StringField("CardId")
    card_code = StringField("UserCardCode")


class MerchantOrderEvent(BaseEvent):
    event = "merchant_order"
    order_id = StringField("OrderId")
    order_status = IntegerField("OrderStatus")
    product_id = StringField("ProductId")
    sku_info = StringField("SkuInfo")


class KfCreateSessionEvent(BaseEvent):
    event = "kf_create_session"
    account = StringField("KfAccount")


class KfCloseSessionEvent(BaseEvent):
    event = "kf_close_session"
    account = StringField("KfAccount")


class KfSwitchSessionEvent(BaseEvent):
    event = "kf_switch_session"
    from_account = StringField("FromKfAccount")
    to_account = StringField("ToKfAccount")


class DeviceTextEvent(BaseEvent):
    event = "device_text"
    device_type = StringField("DeviceType")
    device_id = StringField("DeviceID")
    session_id = StringField("SessionID")
    content = Base64DecodeField("Content")
    open_id = StringField("OpenID")


class DeviceBindEvent(BaseEvent):
    event = "device_bind"
    device_type = StringField("DeviceType")
    device_id = StringField("DeviceID")
    session_id = StringField("SessionID")
    content = Base64DecodeField("Content")
    open_id = StringField("OpenID")


class DeviceUnbindEvent(BaseEvent):
    event = "device_unbind"
    device_type = StringField("DeviceType")
    device_id = StringField("DeviceID")
    session_id = StringField("SessionID")
    content = Base64DecodeField("Content")
    open_id = StringField("OpenID")


class DeviceSubscribeStatusEvent(BaseEvent):
    event = "device_subscribe_status"
    device_type = StringField("DeviceType")
    device_id = StringField("DeviceID")
    open_id = StringField("OpenID")
    op_type = IntegerField("OpType")


class DeviceUnsubscribeStatusEvent(BaseEvent):
    event = "device_unsubscribe_status"
    device_type = StringField("DeviceType")
    device_id = StringField("DeviceID")
    open_id = StringField("OpenID")
    op_type = IntegerField("OpType")


class ShakearoundUserShakeEvent(BaseEvent):
    event = "shakearoundusershake"
    _chosen_beacon = BaseField("ChosenBeacon", {})
    _around_beacons = BaseField("AroundBeacons", {})

    @property
    def chosen_beacon(self):
        beacon = self._chosen_beacon
        if not beacon:
            return {}
        return {
            "uuid": beacon["Uuid"],
            "major": beacon["Major"],
            "minor": beacon["Minor"],
            "distance": float(beacon["Distance"]),
        }

    @property
    def around_beacons(self):
        beacons = self._around_beacons
        if not beacons:
            return []

        ret = []
        for beacon in beacons["AroundBeacon"]:
            ret.append(
                {
                    "uuid": beacon["Uuid"],
                    "major": beacon["Major"],
                    "minor": beacon["Minor"],
                    "distance": float(beacon["Distance"]),
                }
            )
        return ret


class PoiCheckNotifyEvent(BaseEvent):
    event = "poi_check_notify"
    poi_id = StringField("PoiId")
    uniq_id = StringField("UniqId")
    result = StringField("Result")
    message = StringField("Msg")


class WiFiConnectedEvent(BaseEvent):
    event = "wificonnected"
    connect_time = IntegerField("ConnectTime")
    expire_time = IntegerField("ExpireTime")
    vendor_id = StringField("VendorId")
    shop_id = StringField("PlaceId")
    bssid = StringField("DeviceNo")


# ============================================================================
# 微信认证事件推送
# ============================================================================
class QualificationVerifySuccessEvent(BaseEvent):
    """
    资质认证成功事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Account_Management/Wechat_Accreditation_Event_Push.html
    """

    event = "qualification_verify_success"
    expired_time = DateTimeField("ExpiredTime")


class QualificationVerifyFailEvent(BaseEvent):
    """
    资质认证失败事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Account_Management/Wechat_Accreditation_Event_Push.html
    """

    event = "qualification_verify_fail"
    fail_time = DateTimeField("FailTime")
    fail_reason = StringField("FailReason")


class NamingVerifySuccessEvent(BaseEvent):
    """
    名称认证成功事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Account_Management/Wechat_Accreditation_Event_Push.html
    """

    event = "naming_verify_success"
    expired_time = DateTimeField("ExpiredTime")


class NamingVerifyFailEvent(BaseEvent):
    """
    名称认证失败事件

    客户端不打勾，但仍有接口权限。详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Account_Management/Wechat_Accreditation_Event_Push.html
    """

    event = "naming_verify_fail"
    fail_time = DateTimeField("FailTime")
    fail_reason = StringField("FailReason")


class AnnualRenewEvent(BaseEvent):
    """
    年审通知事件

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Account_Management/Wechat_Accreditation_Event_Push.html
    """

    event = "annual_renew"
    expired_time = DateTimeField("ExpiredTime")


class VerifyExpiredEvent(BaseEvent):
    """
    认证过期失效通知

    详情请参阅
    https://developers.weixin.qq.com/doc/offiaccount/Account_Management/Wechat_Accreditation_Event_Push.html
    """

    event = "verify_expired"
    expired_time = DateTimeField("ExpiredTime")


class UserScanProductEvent(BaseEvent):
    """
    打开商品主页事件

    详情请参考
    https://mp.weixin.qq.com/wiki?id=mp1455872179
    """

    event = "user_scan_product"
    standard = StringField("KeyStandard")
    key = StringField("KeyStr")
    country = StringField("Country")
    province = StringField("Province")
    city = StringField("City")
    sex = IntegerField("Sex")
    scene = IntegerField("Scene")


class UserScanProductEnterSessionEvent(BaseEvent):
    """
    进入公众号事件

    详情请参考
    https://mp.weixin.qq.com/wiki?id=mp1455872179
    """

    event = "user_scan_product_enter_session"
    standard = StringField("KeyStandard")
    key = StringField("KeyStr")


class UserScanProductAsyncEvent(BaseEvent):
    """
    地理位置信息异步推送事件

    详情请参考
    https://mp.weixin.qq.com/wiki?id=mp1455872179
    """

    event = "user_scan_product_async"
    standard = StringField("KeyStandard")
    key = StringField("KeyStr")
    region_code = StringField("RegionCode")


class UserScanProductVerifyActionEvent(BaseEvent):
    """
    商品审核结果事件

    详情请参考
    https://mp.weixin.qq.com/wiki?id=mp1455872179
    """

    event = "user_scan_product_verify_action"
    standard = StringField("KeyStandard")
    key = StringField("KeyStr")
    result = StringField("Result")
    reason = StringField("ReasonMsg")


class SubscribeScanProductEvent(BaseEvent):
    """
    用户在商品主页中关注公众号事件

    详情请参考
    https://mp.weixin.qq.com/wiki?id=mp1455872179
    """

    event = "subscribe_scan_product"
    event_key = StringField("EventKey")

    @property
    def scene(self):
        return self.event_key.split("|", 1)[0]

    @property
    def standard(self):
        return self.event_key.split("|")[1]

    @property
    def key(self):
        return self.event_key.split("|")[2]


class UserAuthorizeInvoiceEvent(BaseEvent):
    """
    用户授权发票事件
    （会包含一个订单号，不成功就失败）

    详情请参考
    https://mp.weixin.qq.com/wiki?id=mp1497082828_r1cI2
    """

    event = "user_authorize_invoice"
    success_order_id = StringField("SuccOrderId")  # 授权成功的订单号
    fail_order_id = StringField("FailOrderId")  # 授权失败的订单号
    app_id = StringField("AppId")  # 用于接收事件推送的公众号的AppId
    auth_source = StringField("Source")  # 授权来源，web表示来自微信内H5，app标识来自app


class UpdateInvoiceStatusEvent(BaseEvent):
    """
    发票状态更新事件

    详情请参考
    https://mp.weixin.qq.com/wiki?id=mp1497082828_r1cI2
    """

    event = "update_invoice_status"
    status = StringField("Status")  # 发票报销状态
    card_id = StringField("CardId")  # 发票 Card ID
    code = StringField("Code")  # 发票 Code


class SubmitInvoiceTitleEvent(BaseEvent):
    """
    用户提交发票抬头事件

    详情请参考
    https://mp.weixin.qq.com/wiki?id=mp1496554912_vfWU0
    """

    event = "submit_invoice_title"
    title = StringField("title")  # 抬头
    phone = StringField("phone")  # 联系方式
    tax_no = StringField("tax_no")  # 税号
    addr = StringField("addr")  # 地址
    bank_type = StringField("bank_type")  # 银行类型
    bank_no = StringField("bank_no")  # 银行号码
    attach = StringField("attach")  # 附加字段
    title_type = StringField("title_type")  # 抬头类型，个人InvoiceUserTitlePersonType, 公司InvoiceUserTitleBusinessType


class UserEnterTempSessionEvent(BaseEvent):
    """
    小程序用户进入客服消息
    详情请参阅
    https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/customer-message/receive.html
    """

    event = "user_enter_tempsession"
    session_from = StringField("SessionFrom")


class ViewMiniProgramEvent(BaseEvent):
    """
    从菜单进入小程序事件
    """

    event = "view_miniprogram"
    page_path = StringField("EventKey")  # 小程序路径
    menu_id = StringField("MenuId")  # 菜单ID


class WxaMediaCheckEvent(BaseEvent):
    """
    异步检测结果通知事件
    详情请参考
    https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/sec-check/security.mediaCheckAsync.html
    """

    event = "wxa_media_check"
    is_risky = IntegerField("isrisky")  # 检测结果，0：暂未检测到风险，1：风险
    extra_info_json = StringField("extra_info_json")  # 附加信息，默认为空
    trace_id = StringField("trace_id")  # 任务 id
    status_code = IntegerField("status_code")  # 默认为：0，4294966288(-1008)为链接无法下载

    @property
    def is_valid(self):
        return self.is_risky == 0 and self.status_code == 0
