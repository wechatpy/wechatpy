# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict
from wechatpy.client.api.base import BaseWeChatAPI


class WeChatOA(BaseWeChatAPI):
    """
    OA管理

    https://work.weixin.qq.com/api/doc/90000/90135/90264
    """

    def get_template_detail(self, template_id):
        """
        查询审批模板的详情
        https://work.weixin.qq.com/api/doc/90000/90135/91982

        :param template_id: 模板Id
        :return:
        """
        data = {
            'template_id': template_id
        }
        return self._post(
            'oa/gettemplatedetail',
            data=data
        )

    def get_approval_info(self, start_time, end_time, cursor, size=100, filters=None):
        """
        批量获取审批单号
        https://work.weixin.qq.com/api/doc/90000/90135/91816

        :param start_time: 开始时间戳
        :param end_time: 结束时间戳，请求的参数endtime需要大于startime， 起始时间跨度不能超过31天；
        :param cursor: 分页查询游标，默认为0，后续使用返回的next_cursor进行分页拉取
        :param size: 一次请求拉取审批单数量，默认值为100，上限值为100
        :param filters: 请自行查看文档
        :return:
        """
        data = optionaldict({
            'starttime': str(start_time),
            'endtime': str(end_time),
            'cursor': cursor,
            'size': size,
            'filter': filters
        })

        return self._post(
            'oa/getapprovalinfo',
            data=data
        )

    def get_approval_detail(self, sp_no):
        """
        获取审批申请详情
        https://work.weixin.qq.com/api/doc/90000/90135/91983

        :param sp_no: 审批单编号
        :return:
        """
        data = {
            'sp_no': sp_no
        }
        return self._post(
            'oa/getapprovaldetail',
            data=data
        )

    def apply_event(self, creator_userid, template_id, use_template_approver, approver, apply_data, summary_list,
                    notifyer=None, notify_type=None):
        """
        提交审批申请，这个函数的参数比较复杂，具体请查看官方文档
        https://work.weixin.qq.com/api/doc/90000/90135/91853

        :param creator_userid: 申请人userid，此审批申请将以此员工身份提交，申请人需在应用可见范围内
        :param template_id: 模板id。可在“获取审批申请详情”、“审批状态变化回调通知”中获得，也可在审批模板的模板编辑页面链接中获得。暂不支持通过接口提交[打卡补卡][调班]模板审批单。
        :param use_template_approver: 审批人模式：0-通过接口指定审批人、抄送人（此时approver、notifyer等参数可用）; 1-使用此模板在管理后台设置的审批流程，支持条件审批。
        :param approver: 具体参数查看官方文档，审批流程信息，用于指定审批申请的审批流程，支持单人审批、多人会签、多人或签，可能有多个审批节点，仅use_template_approver为0时生效。
        :param apply_data: 具体参数查看官方文档，审批申请数据，可定义审批申请中各个控件的值，其中必填项必须有值，选填项可为空，数据结构同“获取审批申请详情”接口返回值中同名参数“apply_data”
        :param summary_list: 具体参数查看官方文档，摘要信息，用于显示在审批通知卡片、审批列表的摘要信息，最多3行
        :param notifyer: 抄送人节点userid列表，仅use_template_approver为0时生效。
        :param notify_type: 抄送方式：1-提单时抄送（默认值）； 2-单据通过后抄送；3-提单和单据通过后抄送。仅use_template_approver为0时生效。
        :return:
        """
        data = optionaldict({
            'creator_userid': creator_userid,
            'template_id': template_id,
            'use_template_approver': use_template_approver,
            'approver': approver,
            'notifyer': notifyer,
            'notify_type': notify_type,
            'apply_data': apply_data,
            'summary_list': summary_list
        })
        return self._post(
            'oa/applyevent',
            data=data
        )