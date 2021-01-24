# -*- coding: utf-8 -*-


from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatWxa(BaseWeChatAPI):
    API_BASE_URL = "https://api.weixin.qq.com/"

    def create_qrcode(self, path, width=430):
        """
        创建小程序二维码（接口C：适用于需要的码数量较少的业务场景）
        详情请参考
        https://mp.weixin.qq.com/debug/wxadoc/dev/api/qrcode.html
        """
        return self._post("cgi-bin/wxaapp/createwxaqrcode", data={"path": path, "width": width})

    def get_wxa_code(
        self,
        path,
        width=430,
        auto_color=False,
        line_color=None,
        is_hyaline=False,
    ):
        """
        创建小程序码（接口A: 适用于需要的码数量较少的业务场景）
        详情请参考
        https://mp.weixin.qq.com/debug/wxadoc/dev/api/qrcode.html
        """
        if line_color is None:
            line_color = {"r": "0", "g": "0", "b": "0"}
        return self._post(
            "wxa/getwxacode",
            data={
                "path": path,
                "width": width,
                "auto_color": auto_color,
                "line_color": line_color,
                "is_hyaline": is_hyaline,
            },
        )

    def get_wxa_code_unlimited(
        self,
        scene,
        width=430,
        auto_color=False,
        line_color=None,
        page=None,
        is_hyaline=False,
    ):
        """
        创建小程序码（接口B：适用于需要的码数量极多，或仅临时使用的业务场景）
        详情请参考
        https://mp.weixin.qq.com/debug/wxadoc/dev/api/qrcode.html
        """
        if line_color is None:
            line_color = {"r": "0", "g": "0", "b": "0"}
        return self._post(
            "wxa/getwxacodeunlimit",
            data=optionaldict(
                scene=scene,
                page=page,
                width=width,
                auto_color=auto_color,
                line_color=line_color,
                is_hyaline=is_hyaline,
            ),
        )

    def send_template_message(
        self,
        user_id,
        template_id,
        data,
        form_id,
        page=None,
        color=None,
        emphasis_keyword=None,
    ):
        """
        发送模板消息
        详情请参考
        https://mp.weixin.qq.com/debug/wxadoc/dev/api/notice.html
        """
        tpl_data = optionaldict(
            touser=user_id,
            template_id=template_id,
            page=page,
            form_id=form_id,
            data=data,
            color=color,
            emphasis_keyword=emphasis_keyword,
        )
        return self._post("cgi-bin/message/wxopen/template/send", data=tpl_data)

    def send_subscribe_message(self, user_id, template_id, data, page=None):
        """
        发送订阅消息
        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/subscribe-message/subscribeMessage.send.html
        """
        subs_data = optionaldict(touser=user_id, template_id=template_id, page=page, data=data)
        return self._post("cgi-bin/message/subscribe/send", data=subs_data)

    def modify_domain(
        self,
        action,
        request_domain=(),
        wsrequest_domain=(),
        upload_domain=(),
        download_domain=(),
    ):
        """
        修改小程序服务器授权域名
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489138143_WPbOO

        :param action: 增删改查的操作类型，仅支持 'add', 'delete', 'set', 'get'
        :param request_domain: request 合法域名
        :param wsrequest_domain: socket 合法域名
        :param upload_domain: upload file 合法域名
        :param download_domain: download file 合法域名
        """
        return self._post(
            "wxa/modify_domain",
            data={
                "action": action,
                "requestdomain": request_domain,
                "wsrequestdomain": wsrequest_domain,
                "uploaddomain": upload_domain,
                "downloaddomain": download_domain,
            },
        )

    def bind_tester(self, wechat_id):
        """
        绑定微信用户成为小程序体验者
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140588_nVUgx

        :param wechat_id: 微信号
        """
        return self._post("wxa/bind_tester", data={"wechatid": wechat_id})

    def unbind_tester(self, wechat_id):
        """
        解除绑定小程序的体验者
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140588_nVUgx

        :param wechat_id: 微信号
        """
        return self._post("wxa/unbind_tester", data={"wechatid": wechat_id})

    def commit(self, template_id, ext_json, version, description):
        """
        为授权的小程序账号上传小程序代码
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :param template_id: 代码库中的代码模板 ID
        :param ext_json: 第三方自定义的配置
        :param version: 代码版本号，开发者可自定义
        :param description: 代码描述，开发者可自定义
        """
        return self._post(
            "wxa/commit",
            data={"template_id": template_id, "ext_json": ext_json, "user_version": version, "user_desc": description},
        )

    def get_qrcode(self):
        """
        获取体验小程序的体验二维码
        返回 Response 类型，header 中带有 Content-Type 与 Content-disposition 类型
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :rtype: requests.Response
        """
        return self._get("wxa/get_qrcode")

    def get_category(self):
        """
        获取授权小程序账号的可选类目
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :rtype: list[dict]
        """
        return self._get("wxa/get_category", result_processor=lambda x: x["category_list"])

    def get_page(self):
        """
        获取小程序的第三方提交代码的页面配置
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :rtype: list
        """
        return self._get("wxa/get_page", result_processor=lambda x: x["page_list"])

    def submit_audit(self, data):
        """
        将第三方提交的代码包提交审核
        详情请参考
        https://developers.weixin.qq.com/doc/oplatform/Third-party_Platforms/Mini_Programs/code/submit_audit.html
        """
        return self._post("wxa/submit_audit", data=data)

    def undo_code_audit(self):
        """
        调用本接口可以撤回当前的代码审核单
        注意： 单个帐号每天审核撤回次数最多不超过 1 次，一个月不超过 10 次。
        https://developers.weixin.qq.com/doc/oplatform/Third-party_Platforms/Mini_Programs/code/undocodeaudit.html
        """
        return self._get("wxa/undocodeaudit")

    def revert_code_release(self):
        """
        调用本接口可以将小程序的线上版本进行回退
        注意：
        1. 如果没有上一个线上版本，将无法回退
        2. 只能向上回退一个版本，即当前版本回退后，不能再调用版本回退接口
        https://developers.weixin.qq.com/doc/oplatform/Third-party_Platforms/Mini_Programs/code/revertcoderelease.html
        """
        return self._get("wxa/revertcoderelease")

    def get_audit_status(self, auditid):
        """
        查询某个指定版本的审核状态
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :param auditid: 审核编号
        :type auditid: int
        :return: 一个包含 status, reason 的 dict。status 0为审核成功，1为审核失败，2为审核中。
        """
        return self._post("wxa/get_auditstatus", data={"auditid": auditid})

    def get_latest_audit_status(self):
        """
        查询最近一次提交的审核状态
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :return: 一个包含 status, reason, auditid 的 dict。status 0为审核成功，1为审核失败，2为审核中。
        """
        return self._get("wxa/get_latest_auditstatus")

    def release(self):
        """
        发布已通过审核的小程序
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4
        """
        return self._post("wxa/release", data={})

    def change_visit_status(self, close=False):
        """
        修改小程序线上代码的可见状态
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :param close: close 为 True 时会关闭小程序线上代码的可见状态。
        :type close: bool
        """
        return self._post("wxa/change_visitstatus", data={"action": "close" if close else "open"})

    def list_library_templates(self, offset=0, count=20):
        """
        获取小程序模板库里，所有模板的ID与标题
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1500465446_j4CgR

        :param offset: 用于分页，表示起始量，最小值为0
        :type offset: int
        :param count: 用于分页，表示拉取数量，最大值为20
        :type count: int
        :return: 带有 total_count 与 list 的数据
        :rtype: dict
        """
        return self._post("cgi-bin/wxopen/template/library/list", data={"offset": offset, "count": count})

    def get_library_template(self, template_short_id):
        """
        获取小程序模板库里，某个模板的详细信息
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1500465446_j4CgR

        :param template_short_id: 模板标题ID
        :rtype: dict
        """
        return self._post("cgi-bin/wxopen/template/library/get", data={"id": template_short_id})

    def list_templates(self, offset=0, count=20):
        """
        获取本账号内所有模板
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1500465446_j4CgR

        :param offset: 用于分页，表示起始量，最小值为0
        :type offset: int
        :param count: 用于分页，表示拉取数量，最大值为20
        :type count: int
        :return: 模板列表
        :rtype: list[dict]
        """
        return self._post(
            "cgi-bin/wxopen/template/list",
            data={"offset": offset, "count": count},
            result_processor=lambda x: x["list"],
        )

    def add_template(self, template_short_id, keyword_id_list):
        """
        组合模板，并将其添加至账号下的模板列表里
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1500465446_j4CgR

        :param template_short_id: 模板标题ID
        :param keyword_id_list: 按照顺序排列的模板关键词列表，最多10个
        :type keyword_id_list: list[int]
        :return: 模板ID
        """
        return self._post(
            "cgi-bin/wxopen/template/add",
            data={"id": template_short_id, "keyword_id_list": keyword_id_list},
            result_processor=lambda x: x["template_id"],
        )

    def del_template(self, template_id):
        """
        删除本账号内某个模板
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1500465446_j4CgR

        :param template_id: 模板ID
        """
        return self._post("cgi-bin/wxopen/template/del", data={"template_id": template_id})

    def create_open(self, appid):
        """
        创建开放平台账号，并绑定公众号/小程序
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1498704199_1bcax

        :param appid: 授权公众号或小程序的 appid
        :return: 开放平台的 appid
        """
        return self._post("cgi-bin/open/create", data={"appid": appid}, result_processor=lambda x: x["open_appid"])

    def get_open(self, appid):
        """
        获取公众号/小程序所绑定的开放平台账号
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1498704199_1bcax

        :param appid: 授权公众号或小程序的 appid
        :return: 开放平台的 appid
        """
        return self._post("cgi-bin/open/get", data={"appid": appid}, result_processor=lambda x: x["open_appid"])

    def bind_open(self, appid, open_appid):
        """
        将公众号/小程序绑定到开放平台帐号下
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1498704199_1bcax

        :param appid: 授权公众号或小程序的 appid
        :param open_appid: 开放平台帐号 appid
        """
        return self._post("cgi-bin/open/bind", data={"appid": appid, "open_appid": open_appid})

    def unbind_open(self, appid, open_appid):
        """
        将公众号/小程序绑定到开放平台帐号下
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1498704199_1bcax

        :param appid: 授权公众号或小程序的 appid
        :param open_appid: 开放平台帐号 appid
        """
        return self._post("cgi-bin/open/unbind", data={"appid": appid, "open_appid": open_appid})

    def code_to_session(self, js_code):
        """
        登录凭证校验。通过 wx.login() 接口获得临时登录凭证 code 后传到开发者服务器调用此接口完成登录流程。更多使用方法详见 小程序登录
        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/api/code2Session.html

        :param js_code:
        :return:
        """
        return self._get(
            "sns/jscode2session",
            params={
                "appid": self.appid,
                "secret": self.secret,
                "js_code": js_code,
                "grant_type": "authorization_code",
            },
        )

    def check_image_security(self, media):
        """
        校验一张图片是否含有违法违规内容。
        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/sec-check/security.imgSecCheck.html

        :param media: 要检测的图片文件，格式支持PNG、JPEG、JPG、GIF，图片尺寸不超过 750px x 1334px
        :return:
        """
        return self._post("wxa/img_sec_check", files={"media": media})

    def check_media_async(self, media_url: str, media_type: int):
        """异步校验图片/音频是否含有违法违规内容。

        https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/sec-check/security.mediaCheckAsync.html

        应用场景举例：
        1. 语音风险识别：社交类用户发表的语音内容检测；
        2. 图片智能鉴黄：涉及拍照的工具类应用(如美拍，识图类应用)用户拍照上传检测；电商类商品上架图片检测；媒体类用户文章里的图片检测等；
        3. 敏感人脸识别：用户头像；媒体类用户文章里的图片检测；社交类用户上传的图片检测等。 频率限制：单个 appId 调用上限为 2000 次/分钟，200,000 次/天；文件大小限制：单个文件大小不超过10M


        :param media_url: 要检测的多媒体url
        :param media_type: 1:音频;2:图片
        :return: 返回的 JSON 数据包
        """
        return self._post("wxa/media_check_async", data={"media_url": media_url, "media_type": media_type})

    def check_text_security(self, content):
        """
        检查一段文本是否含有违法违规内容。
        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/sec-check/security.msgSecCheck.html

        :param content: 要检测的文本内容，长度不超过 500KB
        :return:
        """
        return self._post("wxa/msg_sec_check", data={"content": content})

    def speed_up_audit(self, auditid):
        """
        加急审核申请
        有加急次数的第三方可以通过该接口，对已经提审的小程序进行加急操作，加急后的小程序预计2-12小时内审完。
        https://developers.weixin.qq.com/doc/oplatform/Third-party_Platforms/Mini_Programs/code/speedup_audit.html
        """
        return self._post("wxa/speedupaudit", data={"auditid": auditid})

    def query_quota(self):
        """
        查询服务商的当月提审限额（quota）和加急次数
        服务商可以调用该接口，查询当月平台分配的提审限额和剩余可提审次数，以及当月分配的审核加急次数和剩余加急次数。（所有旗下小程序共用该额度）
        https://developers.weixin.qq.com/doc/oplatform/Third-party_Platforms/Mini_Programs/code/query_quota.html
        """
        return self._get("wxa/queryquota")

    def get_paid_unionid(self, openid, transaction_id=None, mch_id=None, out_trade_no=None):
        """
        用户支付完成后，获取该用户的 UnionId，无需用户授权。

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/user-info/auth.getPaidUnionId.html

        :param openid: 支付用户唯一标识
        :param transaction_id: 微信支付订单号，可选
        :param mch_id: 微信支付分配的商户号，和商户订单号配合使用，可选
        :param out_trade_no: 微信支付商户订单号，和商户号配合使用
        :return: 用户唯一标识 unionid
        """
        return self._get(
            "wxa/getpaidunionid",
            params={
                "openid": openid,
                "transaction_id": transaction_id,
                "mch_id": mch_id,
                "out_trade_no": out_trade_no,
            },
            result_processor=lambda x: x["unionid"],
        )

    def get_merchant_category(self) -> dict:
        """
        拉取门店小程序类目

        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Shop_Miniprogram_Interface.html#5
        """
        return self._get("wxa/get_merchant_category")

    def apply_merchant(self, data: dict) -> dict:
        """
        创建门店小程序
        创建门店小程序提交后需要公众号管理员确认通过后才可进行审核。如果主管理员24小时超时未确认，才能再次提交。
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Shop_Miniprogram_Interface.html#6

        :param data: 门店数据，具体请参考文档
        """
        return self._post("wxa/applywxastore", data=data)

    def get_merchant_audit_info(self) -> dict:
        """
        查询门店小程序审核结果
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Shop_Miniprogram_Interface.html#7
        """
        return self._get("wxa/get_merchant_audit_info")

    def modify_merchant(self, data: dict) -> dict:
        """
        修改门店小程序信息
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Shop_Miniprogram_Interface.html#8

        :param data: 具体请参考文档
        :return: 参考文档
        """
        return self._post("wxa/modify_merchant", data=data)

    def get_district(self) -> dict:
        """
        从腾讯地图拉取省市区信息
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Shop_Miniprogram_Interface.html#9
        :return: 参考文档
        """
        return self._get("wxa/get_district")

    def search_map_poi(self, data: dict) -> dict:
        """
        在腾讯地图中搜索门店
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Shop_Miniprogram_Interface.html#10

        :param data: 具体请参考文档
        :return: 参考文档
        """
        return self._post("wxa/search_map_poi", data=data)

    def create_map_poi(self, data: dict) -> dict:
        """
        在腾讯地图中创建门店
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Shop_Miniprogram_Interface.html#11

        :param data: 具体请参考文档
        :return: 参考文档
        """
        return self._post("wxa/create_map_poi", data=data)

    def add_store(self, data: dict) -> dict:
        """
        添加门店
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Shop_Miniprogram_Interface.html#12

        :param data: 具体请参考文档
        :return: 参考文档
        """
        return self._post("wxa/add_store", data=data)

    def update_store(self, data: dict) -> dict:
        """
        更新门店信息
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Shop_Miniprogram_Interface.html#13

        :param data: 具体请参考文档
        :return: 参考文档
        """
        return self._post("wxa/update_store", data=data)

    def get_store_info(self, poi_id: str) -> dict:
        """
        获取单个门店信息
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Shop_Miniprogram_Interface.html#14

        :param poi_id: 为门店小程序添加门店，审核成功后返回的门店id
        :return: 门店信息
        """
        return self._post("wxa/get_store_info", data={"poi_id": poi_id})

    def get_store_list(self, offset: int = 0, limit: int = 10) -> dict:
        """
        获取门店信息列表
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Shop_Miniprogram_Interface.html#15

        :param offset: 获取门店列表的初始偏移位置，从0开始计数
        :param limit: 获取门店个数
        :return: 参考文档
        """
        return self._post("wxa/get_store_list", data={"offset": offset, "limit": limit})

    def del_store(self, poi_id: str) -> dict:
        """
        删除门店
        https://developers.weixin.qq.com/doc/offiaccount/WeChat_Stores/WeChat_Shop_Miniprogram_Interface.html#16

        :param poi_id: 为门店小程序添加门店，审核成功后返回的门店id
        :return: 参考文档
        """
        return self._post("wxa/del_store", data={"poi_id": poi_id})
