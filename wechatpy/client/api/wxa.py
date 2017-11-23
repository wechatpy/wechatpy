# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatWxa(BaseWeChatAPI):
    API_BASE_URL = 'https://api.weixin.qq.com/'

    def create_qrcode(self, path, width=430):
        """
        创建小程序二维码（接口C：适用于需要的码数量较少的业务场景）
        详情请参考
        https://mp.weixin.qq.com/debug/wxadoc/dev/api/qrcode.html
        """
        return self._post(
            'cgi-bin/wxaapp/createwxaqrcode',
            data={
                'path': path,
                'width': width
            }
        )

    def get_wxa_code(self, path, width=430, auto_color=False, line_color={"r": "0", "g": "0", "b": "0"}):
        """
        创建小程序码（接口A: 适用于需要的码数量较少的业务场景）
        详情请参考
        https://mp.weixin.qq.com/debug/wxadoc/dev/api/qrcode.html
        """
        return self._post(
            'wxa/getwxacode',
            data={
                'path': path,
                'width': width,
                'auto_color': auto_color,
                'line_color': line_color,
            }
        )

    def get_wxa_code_unlimited(self, scene, width=430, auto_color=False, line_color={"r": "0", "g": "0", "b": "0"}):
        """
        创建小程序码（接口B：适用于需要的码数量极多，或仅临时使用的业务场景）
        详情请参考
        https://mp.weixin.qq.com/debug/wxadoc/dev/api/qrcode.html
        """
        return self._post(
            'wxa/getwxacodeunlimit',
            data={
                'scene': scene,
                'width': width,
                'auto_color': auto_color,
                'line_color': line_color,
            }
        )

    def send_template_message(self, user_id, template_id, data, form_id, page=None, color=None, emphasis_keyword=None):
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
        return self._post(
            'cgi-bin/message/wxopen/template/send',
            data=tpl_data
        )

    def modify_domain(self, action, request_domain=(), wsrequest_domain=(), upload_domain=(), download_domain=()):
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
            'wxa/modify_domain',
            data={
                'action': action,
                'requestdomain': request_domain,
                'wsrequestdomain': wsrequest_domain,
                'uploaddomain': upload_domain,
                'downloaddomain': download_domain,
            }
        )

    def bind_tester(self, wechat_id):
        """
        绑定微信用户成为小程序体验者
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140588_nVUgx

        :param wechat_id: 微信号
        """
        return self._post(
            'wxa/bind_tester',
            data={
                'wechatid': wechat_id,
            }
        )

    def unbind_tester(self, wechat_id):
        """
        解除绑定小程序的体验者
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140588_nVUgx

        :param wechat_id: 微信号
        """
        return self._post(
            'wxa/unbind_tester',
            data={
                'wechatid': wechat_id,
            }
        )

    def commit(self, template_id, ext_json, version, description):
        """
        为授权的小程序账号上传小程序代码
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :param template_id: 代码库中的代码模版 ID
        :param ext_json: 第三方自定义的配置
        :param version: 代码版本号，开发者可自定义
        :param description: 代码描述，开发者可自定义
        """
        return self._post(
            'wxa/commit',
            data={
                'template_id': template_id,
                'ext_json': ext_json,
                'user_version': version,
                'user_desc': description,
            },
        )

    def get_qrcode(self):
        """
        获取体验小程序的体验二维码
        返回 Response 类型，header 中带有 Content-Type 与 Content-disposition 类型
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :rtype: requests.Response
        """
        return self._get('wxa/get_qrcode')

    def get_category(self):
        """
        获取授权小程序账号的可选类目
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :rtype: list[dict]
        """
        return self._get(
            'wxa/get_category',
            result_processor=lambda x: x['category_list'],
        )

    def get_page(self):
        """
        获取小程序的第三方提交代码的页面配置
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :rtype: list
        """
        return self._get(
            'wxa/get_page',
            result_processor=lambda x: x['page_list'],
        )

    def submit_audit(self, item_list):
        """
        将第三方提交的代码包提交审核
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :param item_list: 提交审核项的一个列表（至少填写1项，至多填写5项）
        :type item_list: list[dict]
        :return: 审核编号
        :rtype: int
        """
        return self._post(
            'wxa/submit_audit',
            data={
                'item_list': item_list,
            },
            result_processor=lambda x: x['auditid'],
        )

    def get_audit_status(self, auditid):
        """
        查询某个指定版本的审核状态
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :param auditid: 审核编号
        :type auditid: int
        :return: 一个包含 status, reason 的 dict。status 0为审核成功，1为审核失败，2为审核中。
        """
        return self._post(
            'wxa/get_auditstatus',
            data={
                'auditid': auditid,
            },
        )

    def get_latest_audit_status(self):
        """
        查询最近一次提交的审核状态
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :return: 一个包含 status, reason, auditid 的 dict。status 0为审核成功，1为审核失败，2为审核中。
        """
        return self._get(
            'wxa/get_latest_auditstatus'
        )

    def release(self):
        """
        发布已通过审核的小程序
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4
        """
        return self._post(
            'wxa/release',
            data={},
        )

    def change_visit_status(self, close=False):
        """
        修改小程序线上代码的可见状态
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1489140610_Uavc4

        :param close: close 为 True 时会关闭小程序线上代码的可见状态。
        :type close: bool
        """
        return self._post(
            'wxa/change_visitstatus',
            data={
                'action': 'close' if close else 'open',
            },
        )

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
        return self._post(
            'cgi-bin/wxopen/template/library/list',
            data={
                'offset': offset,
                'count': count,
            },
        )

    def get_library_template(self, template_short_id):
        """
        获取小程序模板库里，某个模板的详细信息
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1500465446_j4CgR

        :param template_short_id: 模板标题ID
        :rtype: dict
        """
        return self._post(
            'cgi-bin/wxopen/template/library/get',
            data={
                'id': template_short_id,
            },
        )

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
            'cgi-bin/wxopen/template/list',
            data={
                'offset': offset,
                'count': count,
            },
            result_processor=lambda x: x['list'],
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
            'cgi-bin/wxopen/template/add',
            data={
                'id': template_short_id,
                'keyword_id_list': keyword_id_list,
            },
            result_processor=lambda x: x['template_id'],
        )

    def del_template(self, template_id):
        """
        删除本账号内某个模板
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1500465446_j4CgR

        :param template_id: 模板ID
        """
        return self._post(
            'cgi-bin/wxopen/template/del',
            data={
                'template_id': template_id,
            },
        )

    def create_open(self, appid):
        """
        创建开放平台账号，并绑定公众号/小程序
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1498704199_1bcax

        :param appid: 授权公众号或小程序的 appid
        :return: 开放平台的 appid
        """
        return self._post(
            'cgi-bin/open/create',
            data={
                'appid': appid,
            },
            result_processor=lambda x: x['open_appid'],
        )

    def get_open(self, appid):
        """
        获取公众号/小程序所绑定的开放平台账号
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1498704199_1bcax

        :param appid: 授权公众号或小程序的 appid
        :return: 开放平台的 appid
        """
        return self._post(
            'cgi-bin/open/get',
            data={
                'appid': appid,
            },
            result_processor=lambda x: x['open_appid'],
        )

    def bind_open(self, appid, open_appid):
        """
        将公众号/小程序绑定到开放平台帐号下
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1498704199_1bcax

        :param appid: 授权公众号或小程序的 appid
        :param open_appid: 开放平台帐号 appid
        """
        return self._post(
            'cgi-bin/open/bind',
            data={
                'appid': appid,
                'open_appid': open_appid,
            }
        )

    def unbind_open(self, appid, open_appid):
        """
        将公众号/小程序绑定到开放平台帐号下
        详情请参考
        https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&id=open1498704199_1bcax

        :param appid: 授权公众号或小程序的 appid
        :param open_appid: 开放平台帐号 appid
        """
        return self._post(
            'cgi-bin/open/unbind',
            data={
                'appid': appid,
                'open_appid': open_appid,
            }
        )
