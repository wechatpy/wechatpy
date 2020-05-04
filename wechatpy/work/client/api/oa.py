# -*- coding: utf-8 -*-


from optionaldict import optionaldict
from wechatpy.client.api.base import BaseWeChatAPI
from typing import List, Optional


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
        data = {"template_id": template_id}
        return self._post("oa/gettemplatedetail", data=data)

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
        data = optionaldict(
            {"starttime": str(start_time), "endtime": str(end_time), "cursor": cursor, "size": size, "filter": filters}
        )

        return self._post("oa/getapprovalinfo", data=data)

    def get_approval_detail(self, sp_no):
        """
        获取审批申请详情
        https://work.weixin.qq.com/api/doc/90000/90135/91983

        :param sp_no: 审批单编号
        :return:
        """
        data = {"sp_no": sp_no}
        return self._post("oa/getapprovaldetail", data=data)

    def apply_event(
        self,
        creator_userid,
        template_id,
        use_template_approver,
        approver,
        apply_data,
        summary_list,
        notifyer=None,
        notify_type=None,
    ):
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
        data = optionaldict(
            {
                "creator_userid": creator_userid,
                "template_id": template_id,
                "use_template_approver": use_template_approver,
                "approver": approver,
                "notifyer": notifyer,
                "notify_type": notify_type,
                "apply_data": apply_data,
                "summary_list": summary_list,
            }
        )
        return self._post("oa/applyevent", data=data)

    def get_dial_record(
        self, start_time: Optional[int] = None, end_time: Optional[int] = None, offset: int = 0, limit: int = 100
    ) -> dict:
        """
        获取公费电话拨打记录
        https://work.weixin.qq.com/api/doc/90000/90135/90267

        企业可通过此接口，按时间范围拉取成功接通的公费电话拨打记录。

        请注意，查询的时间范围为[start_time,end_time]，即前后均为闭区间。在两个参数都
        指定了的情况下，结束时间不得小于开始时间，开始时间也不得早于当前时间，否则会返回
        600018错误码(无效的起止时间)。

        受限于网络传输，起止时间的最大跨度为30天，如超过30天，则以结束时间为基准向前取
        30天进行查询。

        如果未指定起止时间，则默认查询最近30天范围内数据。

        :param start_time: 查询的起始时间戳
        :param end_time: 查询的结束时间戳
        :param offset: 分页查询的偏移量
        :param limit: 分页查询的每页大小,默认为100条，如该参数大于100则按100处理
        :return: 公费电话拨打记录
        """
        if start_time and end_time and end_time <= start_time:
            raise ValueError("the end time must be greater than the begining time")

        data = {"start_time": start_time, "end_time": end_time, "offset": offset, "limit": limit}
        return self._post("dial/get_dial_record", data=data)

    def get_checkin_data(self, data_type: int, start_time: int, end_time: int, userid_list: List[str]) -> dict:
        """
        获取打卡数据
        https://work.weixin.qq.com/api/doc/90000/90135/90262

        - 获取记录时间跨度不超过30天
        - 用户列表不超过100个。若用户超过100个，请分批获取
        - 有打卡记录即可获取打卡数据，与当前”打卡应用”是否开启无关

        :param data_type: 打卡类型。1：上下班打卡；2：外出打卡；3：全部打卡
        :param start_time: 获取打卡记录的开始时间。Unix时间戳
        :param end_time: 获取打卡记录的结束时间。Unix时间戳
        :param userid_list: 需要获取打卡记录的用户列表
        :return: 打卡数据
        """
        checkin_data_type = {1: "上下班打卡", 2: "外出打卡", 3: "全部打卡"}
        if data_type not in checkin_data_type:
            raise ValueError(f"data_type must be in {list(checkin_data_type.keys())}")

        if end_time <= start_time:
            raise ValueError("the end time must be greater than the begining time")

        if not userid_list:
            raise ValueError("the userid_list can't be an empty list")

        data = {
            "opencheckindatatype": data_type,
            "starttime": start_time,
            "endtime": end_time,
            "useridlist": userid_list,
        }
        return self._post("checkin/getcheckindata", data=data)

    def get_checkin_option(self, datetime: int, userid_list: List[str]) -> dict:
        """
        获取打卡规则
        https://work.weixin.qq.com/api/doc/90000/90135/90263

        - 用户列表不超过100个，若用户超过100个，请分批获取。
        - 用户在不同日期的规则不一定相同，请按天获取。

        :param datetime: 需要获取规则的日期当天0点的Unix时间戳
        :param userid_list: 需要获取打卡规则的用户列表
        :return: 打卡规则
        """
        if not userid_list:
            raise ValueError("the userid_list can't be an empty list")

        data = {"datetime": datetime, "useridlist": userid_list}
        return self._post("checkin/getcheckinoption", data=data)

    def get_open_approval_data(self, third_no: str) -> dict:
        """
        查询自建应用审批单当前状态
        https://work.weixin.qq.com/api/doc/90000/90135/90269

        :param third_no: 开发者发起申请时定义的审批单号
        :return: 审批单的当前审批状态
        """
        data = {"thirdNo": third_no}
        return self._post("corp/getopenapprovaldata", data=data)
