# -*- coding: utf-8 -*-
"""
file: external_contact.py
author: Beck
created at: 2019-06-06
email: beck@ilife.co
"""
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatExternalContact(BaseWeChatAPI):
    """
    https://work.weixin.qq.com/api/doc#90000/90135/90221
    """
    def get_follow_user_list(self):
        """
        获取配置了客户联系功能的成员列表
        https://work.weixin.qq.com/api/doc#90000/90135/91554
        :return: 返回的 JSON 数据包
        """
        return self._get('externalcontact/get_follow_user_list')

    def list(self, userid):
        """
        获取外部联系人列表
        https://work.weixin.qq.com/api/doc#90000/90135/91555
        :param userid: 企业成员的userid
        :return: 返回的 JSON 数据包
        """
        return self._get('externalcontact/list', params={'userid': userid})

    def get(self, external_userid):
        """
        获取外部联系人详情
        https://work.weixin.qq.com/api/doc#90000/90135/91556
        :param external_userid: 外部联系人的userid，注意不是企业成员的帐号
        :return: 返回的 JSON 数据包
        """
        return self._get('externalcontact/get',
                         params={'external_userid': external_userid})

    def add_contact_way(self, type, scene, style=None,
                        remark=None, skip_verify=True, state=None,
                        user=None, party=None):
        """
        配置客户联系「联系我」方式
        https://work.weixin.qq.com/api/doc#90000/90135/91559

        :param type: 联系方式类型,1-单人, 2-多人
        :param scene: 场景，1-在小程序中联系，2-通过二维码联系
        :param style: 在小程序中联系时使用的控件样式，详见附表
        :param remark: 联系方式的备注信息，用于助记，不超过30个字符
        :param skip_verify: 外部客户添加时是否无需验证，默认为true
        :param state: 企业自定义的state参数，用于区分不同的添加渠道，在调用“获取外部联系人详情”时会返回该参数值
        :param user: 使用该联系方式的用户userID列表，在type为1时为必填，且只能有一个
        :param party: 使用该联系方式的部门id列表，只在type为2时有效
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(
            type=type,
            scene=scene,
            style=style,
            remark=remark,
            skip_verify=skip_verify,
            state=state,
            user=user,
            party=party
        )
        return self._post('externalcontact/add_contact_way', data=data)

    def get_contact_way(self, config_id):
        """
        获取企业已配置的「联系我」方式
        https://work.weixin.qq.com/api/doc#90000/90135/91559
        :param config_id: 联系方式的配置id, e.g.42b34949e138eb6e027c123cba77fad7
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(
            config_id=config_id
        )
        return self._post('externalcontact/get_contact_way', data=data)

    def update_contact_way(self, config_id, remark, skip_verify=True,
                           style=None, state=None, user=None,
                           party=None):
        """
        更新企业已配置的「联系我」方式
        https://work.weixin.qq.com/api/doc#90000/90135/91559

        :param config_id: 企业联系方式的配置id
        :param remark: 联系方式的备注信息，不超过30个字符，将覆盖之前的备注
        :param skip_verify: 外部客户添加时是否无需验证
        :param style: 样式，只针对“在小程序中联系”的配置生效
        :param state: 企业自定义的state参数，用于区分不同的添加渠道，在调用“获取外部联系人详情”时会返回该参数值
        :param user: 使用该联系方式的用户列表，将覆盖原有用户列表
        :param party: 使用该联系方式的部门列表，将覆盖原有部门列表，只在配置的type为2时有效
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(
            config_id=config_id,
            remark=remark,
            skip_verify=skip_verify,
            style=style,
            state=state,
            user=user,
            party=party
        )
        return self._post('externalcontact/update_contact_way', data=data)

    def del_contact_way(self, config_id):
        """
        删除企业已配置的「联系我」方式
        :param config_id: 企业联系方式的配置id
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(
            config_id=config_id
        )
        return self._post('externalcontact/del_contact_way', data=data)

    def add_msg_template(self, template):
        """
        添加企业群发消息模板
        https://work.weixin.qq.com/api/doc#90000/90135/91560

        {
          "external_userid":[
            "woAJ2GCAAAXtWyujaWJHDDGi0mACas1w",
            "wmqfasd1e1927831291723123109r712"
          ],
          "sender":"zhangsan",
          "text":{
            "content":"文本消息内容"
          },
          "image":{
            "media_id":"MEDIA_ID"
          },
          "link":{
            "title":"消息标题",
            "picurl":"https://example.pic.com/path",
            "desc":"消息描述",
            "url":"https://example.link.com/path"
          },
          "miniprogram":{
            "title":"消息标题",
            "pic_media_id":"MEDIA_ID",
            "appid":"wx8bd80126147df384",
            "page":"/path/index"
          }
        }
        external_userid	否	客户的外部联系人id列表，不可与sender同时为空，最多可传入1万个客户
        sender	否	发送企业群发消息的成员userid，不可与external_userid同时为空
        text.content	否	消息文本内容
        image.media_id	是	图片的media_id
        link.title	是	图文消息标题
        link.picurl	否	图文消息封面的url
        link.desc	否	图文消息的描述
        link.url	是	图文消息的链接
        miniprogram.title	是	小程序消息标题
        miniprogram.pic_media_id	是	小程序消息封面的mediaid，封面图建议尺寸为520*416
        miniprogram.appid	是	小程序appid，必须是关联到企业的小程序应用
        miniprogram.page	是	小程序page路径

        text、image、link和miniprogram四者不能同时为空；
        text与另外三者可以同时发送，此时将会以两条消息的形式触达客户
        image、link和miniprogram只能有一个，如果三者同时填，则按image、link、miniprogram的优先顺序取参，也就是说，如果image与link同时传值，则只有image生效。
        media_id可以通过素材管理接口获得。

        :param template: 见上方说明.
        :return: 返回的 JSON 数据包
        """
        return self._post('externalcontact/add_msg_template', data=template)

    def get_group_msg_result(self, msgid):
        """
        获取企业群发消息发送结果
        企业和第三方可通过该接口获取到添加企业群发消息模板生成消息的群发发送结果。
        https://work.weixin.qq.com/api/doc#90000/90135/91561

        :param msgid: 群发消息的id，通过添加企业群发消息模板接口返回
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(
            msgid=msgid
        )
        return self._post('externalcontact/get_group_msg_result', data=data)

    def get_user_behavior_data(self, userid,
                               start_time, end_time):
        """
        获取员工行为数据

        企业可通过此接口获取员工联系客户的行为数据，包括聊天数，发送消息数，消息回复比例和平均首次回复时长等维度。
        https://work.weixin.qq.com/api/doc#90000/90135/91580

        :param userid: 	userid列表
        :param start_time: 数据起始时间
        :param end_time: 数据结束时间
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(
            userid=userid,
            start_time=start_time,
            end_time=end_time
        )
        return self._post('externalcontact/get_user_behavior_data', data=data)

    def send_welcome_msg(self, template):
        """
        发送新客户欢迎语
        企业微信在向企业推送添加外部联系人事件时，会额外返回一个welcome_code，企业以此为凭据调用接口，即可通过成员向新添加的客户发送个性化的欢迎语。
        为了保证用户体验以及避免滥用，企业仅可在收到相关事件后20秒内调用，且只可调用一次。
        如果企业已经在管理端为相关成员配置了可用的欢迎语，则推送添加外部联系人事件时不会返回welcome_code。
        https://work.weixin.qq.com/api/doc#90000/90135/91688

        {
          "welcome_code":"CALLBACK_CODE",
          "text":{
            "content":"文本消息内容"
          },
          "image":{
            "media_id":"MEDIA_ID"
          },
          "link":{
            "title":"消息标题",
            "picurl":"https://example.pic.com/path",
            "desc":"消息描述",
            "url":"https://example.link.com/path"
          },
          "miniprogram":{
            "title":"消息标题",
            "pic_media_id":"MEDIA_ID",
            "appid":"wx8bd80126147df384",
            "page":"/path/index"
          }
        }
        welcome_code	是	通过添加外部联系人事件推送给企业的发送欢迎语的凭证，有效期为20秒
        text.content	否	消息文本内容
        image.media_id	是	图片的media_id
        link.title	是	图文消息标题
        link.picurl	否	图文消息封面的url
        link.desc	否	图文消息的描述
        link.url	是	图文消息的链接
        miniprogram.title	是	小程序消息标题
        miniprogram.pic_media_id	是	小程序消息封面的mediaid，封面图建议尺寸为520*416
        miniprogram.appid	是	小程序appid，必须是关联到企业的小程序应用
        miniprogram.page	是	小程序page路径

        text、image、link和miniprogram四者不能同时为空；
        text与另外三者可以同时发送，此时将会以两条消息的形式触达客户
        image、link和miniprogram只能有一个，如果三者同时填，则按image、link、miniprogram的优先顺序取参，也就是说，如果image与link同时传值，则只有image生效。
        media_id可以通过素材管理接口获得。
        :param template: 见上方说明.
        :return: 返回的 JSON 数据包
        """
        return self._post('externalcontact/send_welcome_msg', data=template)

    def get_unassigned_list(self, page_id, page_size):
        """
        获取离职成员的客户列表
        企业和第三方可通过此接口，获取所有离职成员的客户列表，并可进一步调用离职成员的外部联系人再分配接口将这些客户重新分配给其他企业成员。
        https://work.weixin.qq.com/api/doc#90000/90135/91563

        :param page_id: 分页查询，要查询页号，从0开始
        :param page_size: 每次返回的最大记录数，默认为1000，最大值为1000
        :return:
        """
        data = optionaldict(
            page_id=page_id,
            page_size=page_size
        )
        return self._post('externalcontact/get_unassigned_list', data=data)

    def transfer(self, external_userid, handover_userid,
                 takeover_userid):
        """
        离职成员的外部联系人再分配
        企业可通过此接口，将已离职成员的外部联系人分配给另一个成员接替联系。
        https://work.weixin.qq.com/api/doc#90000/90135/91564

        :param external_userid: 外部联系人的userid，注意不是企业成员的帐号
        :param handover_userid: 离职成员的userid
        :param takeover_userid: 接替成员的userid
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(
            external_userid=external_userid,
            handover_userid=handover_userid,
            takeover_userid=takeover_userid
        )
        return self._post('externalcontact/transfer', data=data)
