# -*- coding: utf-8 -*-


from wechatpy.client.api.base import BaseWeChatAPI


class WeChatInvoice(BaseWeChatAPI):
    API_BASE_URL = "https://api.weixin.qq.com/card/invoice/"

    def get_url(self):
        """
        获取自身开票平台专用的授权链接
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496561481_1TyO7

        :return:该开票平台专用的授权链接
        """
        return self._post(
            "seturl",
            data={},
            result_processor=lambda x: x["invoice_url"],
        )

    def create_card(self, base_info, payee, invoice_type, detail=None):
        """
        创建发票卡券模板
        注意这里的对象和会员卡有类似之处，但是含义有不同。创建发票卡券模板是创建发票卡券的基础。
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496561481_1TyO7

        :param base_info:发票卡券模板基础信息
        :type base_info: dict
        :param payee: 收款方（开票方）全称，显示在发票详情内。建议一个收款方对应一个发票卡券模板
        :param invoice_type: 发票类型描述
        :param detail: 备注详情
        :return: 发票卡券模板的编号，用于后续该商户发票生成后，作为必填参数在调用插卡接口时传入
        """
        return self._post(
            "platform/createcard",
            data={
                "invoice_info": {
                    "base_info": base_info,
                    "payee": payee,
                    "type": invoice_type,
                    "detail": detail,
                },
            },
            result_processor=lambda x: x["card_id"],
        )

    def get_auth_url(
        self,
        s_pappid,
        order_id,
        money,
        timestamp,
        source,
        ticket,
        auth_type,
        redirect_url=None,
    ):
        """
        获取授权页链接
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1497082828_r1cI2

        :param s_pappid: 开票平台在微信的标识号，商户需要找开票平台提供
        :param order_id: 订单id，在商户内单笔开票请求的唯一识别号
        :param money: 订单金额，以分为单位
        :type money: int
        :param timestamp: Unix 时间戳
        :type timestamp: int
        :param source: 开票来源。app: App开票, web: 微信H5开票, wap: 普通网页开票
        :param ticket: 根据获取授权ticket接口取得
        :param auth_type: 授权类型。0: 开票授权，1: 填写字段开票授权，2: 领票授权
        :type auth_type: int
        :param redirect_url: 授权成功后跳转页面。本字段只有在source为H5的时候需要填写。
        :return: 获取授权页链接
        """
        if source not in {"app", "web", "wap"}:
            raise ValueError('Unsupported source. Valid sources are "app", "web" or "wap"')
        if source == "web" and redirect_url is None:
            raise ValueError("redirect_url is required if source is web")
        if not (0 <= auth_type <= 2):
            raise ValueError("Unsupported auth type. Valid auth types are 0, 1 or 2")
        return self._post(
            "getauthurl",
            data={
                "s_pappid": s_pappid,
                "order_id": order_id,
                "money": money,
                "timestamp": timestamp,
                "source": source,
                "ticket": ticket,
                "type": auth_type,
                "redirect_url": redirect_url,
            },
            result_processor=lambda x: x["auth_url"],
        )

    def set_auth_field(self, user_field, biz_field):
        """
        设置授权页字段信息
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1497082828_r1cI2

        :param user_field: 授权页个人发票字段
        :type user_field: dict
        :param biz_field: 授权页单位发票字段
        :type biz_field: dict
        """
        return self._post(
            "setbizattr",
            params={
                "action": "set_auth_field",
            },
            data={
                "auth_field": {
                    "user_field": user_field,
                    "biz_field": biz_field,
                },
            },
        )

    def get_auth_field(self):
        """
        获取授权页字段信息
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1497082828_r1cI2

        :return: 授权页的字段设置
        :rtype: dict
        """
        return self._post(
            "setbizattr",
            params={
                "action": "get_auth_field",
            },
            data={},
        )

    def get_auth_data(self, s_pappid, order_id):
        """
        查询授权数据
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1497082828_r1cI2

        :param s_pappid: 开票平台在微信的标识号，商户需要找开票平台提供
        :param order_id: 订单id，在商户内单笔开票请求的唯一识别号
        :return: 用户的开票信息
        :rtype: dict
        """
        return self._post(
            "getauthdata",
            data={
                "s_pappid": s_pappid,
                "order_id": order_id,
            },
        )

    def reject_insert(self, s_pappid, order_id, reason, redirect_url=None):
        """
        拒绝用户的开发票请求
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1497082828_r1cI2

        :param s_pappid: 开票平台在微信的标识号，商户需要找开票平台提供
        :param order_id: 订单id，在商户内单笔开票请求的唯一识别号
        :param reason: 拒绝原因
        :param redirect_url: 跳转链接
        """
        return self._post(
            "rejectinsert",
            data={
                "s_pappid": s_pappid,
                "order_id": order_id,
                "reason": reason,
                "url": redirect_url,
            },
        )

    def insert(self, order_id, card_id, appid, card_ext):
        """
        制作发票卡券，并放入用户卡包
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1497082828_r1cI2

        :param order_id: 订单id，在商户内单笔开票请求的唯一识别号
        :param card_id: 发票卡券模板的编号
        :param appid: 商户 AppID
        :param card_ext: 发票具体内容
        :type card_ext: dict
        :return: 随机防重字符串，以及用户 Open ID
        """
        return self._post(
            "insert",
            data={
                "order_id": order_id,
                "card_id": card_id,
                "appid": appid,
                "card_ext": card_ext,
            },
        )

    def upload_pdf(self, pdf):
        """
        上传电子发票中的消费凭证 PDF
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1497082828_r1cI2

        :param pdf: 要上传的 PDF 文件，一个 File-object
        :return: 64位整数，在将发票卡券插入用户卡包时使用用于关联pdf和发票卡券。有效期为3天。
        """
        return self._post(
            "platform/setpdf",
            files={
                "pdf": pdf,
            },
            result_processor=lambda x: x["s_media_id"],
        )

    def get_pdf(self, s_media_id):
        """
        查询已上传的 PDF
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1497082828_r1cI2

        :param s_media_id: PDF 文件上传时的 s_media_id
        :return: PDF 文件的 URL，以及过期时间
        :rtype: dict
        """
        return self._post(
            "platform/getpdf",
            params={
                "action": "get_url",
            },
            data={
                "s_media_id": s_media_id,
            },
        )

    def update_status(self, card_id, code, reimburse_status):
        """
        更新发票卡券的状态
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1497082828_r1cI2

        :param card_id: 发票卡券模板的编号
        :param code: 发票卡券的编号
        :param reimburse_status: 发票报销状态
        """
        return self._post(
            "platform/updatestatus",
            data={
                "card_id": card_id,
                "code": code,
                "reimburse_status": reimburse_status,
            },
        )

    def set_contact(self, phone, time_out):
        """
        商户获取授权链接之前，需要先设置商户的联系方式
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Invoice/E_Invoice/Vendor_API_List.html#17

        :param phone: 联系电话
        :param time_out: 开票超时时间
        """
        return self._post(
            "setbizattr",
            params={
                "action": "set_contact",
            },
            data={
                "contact": {
                    "phone": phone,
                    "time_out": time_out,
                },
            },
        )

    def get_contact(self):
        """
        商户获取授权链接之前，需要先设置商户的联系方式
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Invoice/E_Invoice/Vendor_API_List.html#17

        """
        return self._post(
            "setbizattr",
            params={
                "action": "get_contact",
            },
            data={},
        )

    def set_pay_mch(self, mchid, s_pappid):
        """
        关联商户号与开票平台，设置支付后开票
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496561731_2Z55U

        :param mchid: 微信支付商户号
        :param s_pappid: 开票平台在微信的标识号，商户需要找开票平台提供
        """
        return self._post(
            "setbizattr",
            params={
                "action": "set_pay_mch",
            },
            data={
                "paymch_info": {
                    "mchid": mchid,
                    "s_pappid": s_pappid,
                },
            },
        )

    def get_pay_mch(self):
        """
        查询商户号与开票平台关联情况
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496561731_2Z55U

        :return: mchid 和 s_pappid
        :rtype: dict
        """
        return self._post(
            "setbizattr",
            params={
                "action": "get_pay_mch",
            },
            data={},
        )

    def get_reimburse(self, card_id, encrypt_code):
        """
        报销方查询发票信息
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496561749_f7T6D

        :param card_id: 发票卡券的 Card ID
        :param encrypt_code: 发票卡券的加密 Code
        :return: 电子发票的结构化信息
        :rtype: dict
        """
        return self._post(
            "reimburse/getinvoiceinfo",
            data={
                "card_id": card_id,
                "encrypt_code": encrypt_code,
            },
        )

    def update_reimburse(self, card_id, encrypt_code, reimburse_status):
        """
        报销方更新发票信息
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496561749_f7T6D

        :param card_id: 发票卡券的 Card ID
        :param encrypt_code: 发票卡券的加密 Code
        :param reimburse_status: 发票报销状态
        """
        return self._post(
            "reimburse/updateinvoicestatus",
            data={
                "card_id": card_id,
                "encrypt_code": encrypt_code,
                "reimburse_status": reimburse_status,
            },
        )

    def batch_update_reimburse(self, openid, reimburse_status, invoice_list):
        """
        报销方批量更新发票信息
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496561749_f7T6D

        :param openid: 用户的 Open ID
        :param reimburse_status: 发票报销状态
        :param invoice_list: 发票列表
        :type invoice_list: list[dict]
        """
        return self._post(
            "reimburse/updatestatusbatch",
            data={
                "openid": openid,
                "reimburse_status": reimburse_status,
                "invoice_list": invoice_list,
            },
        )

    def get_user_title_url(
        self,
        user_fill,
        title=None,
        phone=None,
        tax_no=None,
        addr=None,
        bank_type=None,
        bank_no=None,
        out_title_id=None,
    ):
        """
        获取添加发票链接
        获取链接，发送给用户。用户同意以后，发票抬头信息将会录入到用户微信中
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496554912_vfWU0

        :param user_fill: 企业设置抬头为0，用户自己填写抬头为1
        :type user_fill: bool
        :param title: 抬头，当 user_fill 为 False 时必填
        :param phone: 联系方式
        :param tax_no: 税号
        :param addr: 地址
        :param bank_type: 银行类型
        :param bank_no: 银行号码
        :param out_title_id: 开票码
        :return: 添加发票的链接
        """
        if user_fill and title is None:
            raise ValueError("title is required when user_fill is False")
        return self._post(
            "biz/getusertitleurl",
            data={
                "user_fill": int(user_fill),
                "title": title,
                "phone": phone,
                "tax_no": tax_no,
                "addr": addr,
                "bank_type": bank_type,
                "bank_no": bank_no,
                "out_title_id": out_title_id,
            },
            result_processor=lambda x: x["url"],
        )

    def get_select_title_url(self, attach=None):
        """
        获取商户专属开票链接
        商户调用接口，获取链接。用户扫码，可以选择抬头发给商户。可以将链接转成二维码，立在收银台。
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496554912_vfWU0

        :param attach: 附加字段，用户提交发票时会发送给商户
        :return: 商户专属开票链接
        """
        return self._post(
            "biz/getselecttitleurl",
            data={
                "attach": attach,
            },
            result_processor=lambda x: x["url"],
        )

    def scan_title(self, scan_text):
        """
        根据扫描码，获取用户发票抬头
        商户扫用户“我的—个人信息—我的发票抬头”里面的抬头二维码后，通过调用本接口，可以获取用户抬头信息
        详情请参考
        https://mp.weixin.qq.com/wiki?id=mp1496554912_vfWU0

        :param scan_text: 扫码后获取的文本
        :return: 用户的发票抬头数据
        :rtype: dict
        """
        return self._post(
            "scantitle",
            data={
                "scan_text": scan_text,
            },
        )
