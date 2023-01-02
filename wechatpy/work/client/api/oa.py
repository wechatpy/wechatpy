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
            raise ValueError("the end time must be greater than the beginning time")

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
            raise ValueError("the end time must be greater than the beginning time")

        if not userid_list:
            raise ValueError("the userid_list can't be an empty list")

        data = {
            "opencheckindatatype": data_type,
            "starttime": start_time,
            "endtime": end_time,
            "useridlist": userid_list,
        }
        return self._post("checkin/getcheckindata", data=data)

    def get_checkin_daydata(self, start_time: int, end_time: int, userid_list: List[str]) -> dict:
        """
        获取打卡日报数据
        https://developer.work.weixin.qq.com/document/path/93374

        - 接口调用频率限制为100次/分钟

        :param start_time: 获取打卡记录的开始时间。Unix时间戳
        :param end_time: 获取打卡记录的结束时间。Unix时间戳
        :param userid_list: 获取日报的userid列表。可填充个数：1 ~ 100
        :return: 打卡数据
        """
        if end_time <= start_time:
            raise ValueError("the end time must be greater than the beginning time")

        if not userid_list:
            raise ValueError("the userid_list can't be an empty list")

        data = {
            "starttime": start_time,
            "endtime": end_time,
            "useridlist": userid_list,
        }
        return self._post("checkin/getcheckin_daydata", data=data)

    def get_checkin_monthdata(self, start_time: int, end_time: int, userid_list: List[str]) -> dict:
        """
        获取打卡月报数据
        https://developer.work.weixin.qq.com/document/path/93374

        - 接口调用频率限制为100次/分钟

        :param start_time: 获取打卡记录的开始时间。Unix时间戳
        :param end_time: 获取打卡记录的结束时间。Unix时间戳
        :param userid_list: 获取月报的userid列表。可填充个数：1 ~ 100
        :return: 打卡数据
        """
        if end_time <= start_time:
            raise ValueError("the end time must be greater than the beginning time")

        if not userid_list:
            raise ValueError("the userid_list can't be an empty list")

        data = {
            "starttime": start_time,
            "endtime": end_time,
            "useridlist": userid_list,
        }
        return self._post("checkin/getcheckin_monthdata", data=data)

    def get_corp_checkin_option(self):
        """
        获取企业所有打卡规则
        https://developer.work.weixin.qq.com/document/path/93384
        """
        return self._post("checkin/getcorpcheckinoption")

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

    def get_checkin_schedu_list(self, start_time: int, end_time: int, userid_list: List[str]) -> dict:
        """
        获取打卡人员排班信息
        https://developer.work.weixin.qq.com/document/path/93380

        :param start_time: 获取排班信息的开始时间。Unix时间戳
        :param end_time: 获取排班信息的结束时间。Unix时间戳（与 start_time 跨度不超过一个月）
        :param userid_list: 需要获取排班信息的用户列表（不超过100个）
        :return: 排班信息
        """
        if end_time <= start_time:
            raise ValueError("the end time must be greater than the beginning time")

        if end_time - start_time > 31 * 86400:
            raise ValueError("the difference between the start_time and the end_time cannot be more than one month")

        if not userid_list:
            raise ValueError("the userid_list can't be an empty list")

        data = {
            "starttime": start_time,
            "endtime": end_time,
            "useridlist": userid_list,
        }
        return self._post("checkin/getcheckinschedulist", data=data)

    def set_checkin_schedu_list(self, group_id: int, items: list, yearmonth: int) -> dict:
        """
        为打卡人员排班
        https://developer.work.weixin.qq.com/document/path/93385

        :param group_id: 打卡规则的规则 id，可通过“获取打卡规则”、“获取打卡数据”、“获取打卡人员排班信息”等相关接口获取
        :param items: 排班表信息，字典结构，包含 userid，day，schedule_id 三个字段
                    - userid: 打卡人员userid
                    - day: 要设置的天日期，取值在1-31之间。联合 yearmonth 组成唯一日期 比如20201205
                    - schedule_id: 对应 groupid 规则下的班次 id，通过预先拉取规则信息获取，0 代表休息
        :param yearmonth: 排班表月份，格式为年月，如202011
        """
        data = {
            "groupid": group_id,
            "items": items,
            "yearmonth": yearmonth,
        }
        return self._post("checkin/setcheckinschedulist", data=data)

    def add_checkin_userface(self, user_id: str, user_face: str) -> dict:
        """
        录入打卡人员人脸信息
        https://developer.work.weixin.qq.com/document/path/93378

        :param user_id: 需要录入的用户id
        :param user_face: 需要录入的人脸图片数据，需要将图片数据base64处理后填入，对已录入的人脸会进行更新处理
        """
        data = {
            "userid": user_id,
            "userface": user_face,
        }
        return self._post("checkin/addcheckinuserface", data=data)

    def get_hardware_checkin_data(
        self, start_time: int, end_time: int, userid_list: List[str], filter_type: int = 1
    ) -> dict:
        """
        获取设备打卡数据
        https://developer.work.weixin.qq.com/document/path/94126

        :param filter_type: 过滤类型，1 表示按打卡时间过滤，2 表示按设备上传打卡记录的时间过滤，默认值是 1
        :param start_time: Unix时间戳，当 filter_type 为 1 时，表示打卡的开始时间；当 filter_type 为 2 时，表示设备上传记录的开始时间
        :param end_time: Unix时间戳，当 filter_type 为 1 时，表示打卡的结束时间；当 filter_type 为 2 时，表示设备上传记录的结束时间
        :param userid_list: 需要获取打卡记录的用户列表（不超过100个）

        - 获取记录时间跨度不超过一个月
        - 用户列表不超过100个。若用户超过100个，请分批获取
        - 获取的是通过考勤设备打卡的原始记录，不包含企业微信app手机打卡的记录
        - userid无效时，忽略该参数，不报错
        """
        if end_time <= start_time:
            raise ValueError("the end time must be greater than the beginning time")

        if end_time - start_time > 31 * 86400:
            raise ValueError("the difference between the start_time and the end_time cannot be more than one month")

        if not userid_list:
            raise ValueError("the userid_list can't be an empty list")

        if filter_type not in {1, 2}:
            raise ValueError("Unsupported filter_type. Valid filter_type are 1 or 2")

        data = {
            "filter_type": filter_type,
            "starttime": start_time,
            "endtime": end_time,
            "useridlist": userid_list,
        }
        return self._post("hardware/get_hardware_checkin_data", data=data)

    def get_open_approval_data(self, third_no: str) -> dict:
        """
        查询自建应用审批单当前状态
        https://work.weixin.qq.com/api/doc/90000/90135/90269

        :param third_no: 开发者发起申请时定义的审批单号
        :return: 审批单的当前审批状态
        """
        data = {"thirdNo": third_no}
        return self._post("corp/getopenapprovaldata", data=data)

    def get_journal_record_list(self, start_time: int, end_time: int, cursor: int, limit: int, filters=None) -> dict:
        """
        批量获取汇报记录单号
        https://developer.work.weixin.qq.com/document/path/93393

        :param start_time: 开始时间
        :param end_time: 结束时间,开始时间和结束时间间隔不能超过一个月
        :param cursor: 游标首次请求传0，非首次请求携带上一次请求返回的next_cursor
        :param limit: 拉取条数
        :param filters: 过滤条件
        """
        if end_time <= start_time:
            raise ValueError("the end time must be greater than the beginning time")

        if end_time - start_time > 31 * 86400:
            raise ValueError("the difference between the start_time and the end_time cannot be more than one month")

        data = {
            "starttime": start_time,
            "endtime": end_time,
            "cursor": cursor,
            "limit": limit,
        }
        if filters:
            data["filters"] = filters
        return self._post("oa/journal/get_record_list", data=data)

    def get_journal_record_detail(self, journal_uuid: str) -> dict:
        """
        获取汇报记录详情
        https://developer.work.weixin.qq.com/document/path/93394

        :param journal_uuid: 汇报记录单号
        """
        return self._post("oa/journal/get_record_detail", data={"journaluuid": journal_uuid})

    def get_journal_stat_list(self, start_time: int, end_time: int, template_id: str) -> dict:
        """
        获取汇报统计数据
        https://developer.work.weixin.qq.com/document/path/93395

        :param start_time: 开始时间
        :param end_time: 结束时间，时间区间最大长度为一年
        :param template_id: 汇报表单id
        """
        data = {"template_id": template_id, "starttime": start_time, "endtime": end_time}
        return self._post("oa/journal/get_stat_list", data=data)

    def add_meetingroom(
        self,
        name: str,
        capacity: int,
        city: str = None,
        building: str = None,
        floor: str = None,
        equipment: list = None,
        latitude: str = None,
        longitude: str = None,
    ):
        """
        添加会议室
        https://developer.work.weixin.qq.com/document/path/93619

        - 如果需要为会议室设置位置信息，则必须同时填写城市（city），楼宇（building）和楼层(floor)三个参数。

        :param name: 会议室名称，最多30个字符
        :param capacity: 会议室所能容纳的人数
        :param city: 会议室所在城市
        :param building: 会议室所在楼宇
        :param floor: 会议室所在楼层
        :param equipment: 会议室支持的设备列表,参数详细含义见附录
        :param latitude: 会议室所在建筑纬度,可通过腾讯地图坐标拾取器获取
        :param longitude: 会议室所在建筑经度,可通过腾讯地图坐标拾取器获取
        """
        data = {
            "name": name,
            "capacity": capacity,
        }
        if all([city, building, floor]):
            data["city"] = city
            data["building"] = building
            data["floor"] = floor
        if equipment:
            data["equipment"] = equipment
        if latitude and longitude:
            data["coordinate"] = {"latitude": latitude, "longitude": longitude}
        return self._post("oa/meetingroom/add", data=data)

    def get_meetingroom_list(
        self,
        city: str = None,
        building: str = None,
        floor: str = None,
        equipment: list = None,
    ):
        """
        查询会议室
        https://developer.work.weixin.qq.com/document/path/93619

        - 如果需要为会议室设置位置信息，则必须同时填写城市（city），楼宇（building）和楼层(floor)三个参数。
        """
        data = {"city": city, "building": building, "floor": floor, "equipment": equipment}
        data = {k: v for k, v in data.items() if v is not None}
        return self._post("oa/meetingroom/list", data=data)

    def edit_meetingroom(
        self,
        meetingroom_id: int,
        name: str,
        capacity: int,
        city: str = None,
        building: str = None,
        floor: str = None,
        equipment: list = None,
        latitude: str = None,
        longitude: str = None,
    ):
        """
        编辑会议室
        https://developer.work.weixin.qq.com/document/path/93619

        - 如果需要为会议室设置位置信息，则必须同时填写城市（city），楼宇（building）和楼层(floor)三个参数。

        :param meetingroom_id: 会议室的id
        :param name: 会议室名称，最多30个字符
        :param capacity: 会议室所能容纳的人数
        :param city: 会议室所在城市
        :param building: 会议室所在楼宇
        :param floor: 会议室所在楼层
        :param equipment: 会议室支持的设备列表,参数详细含义见附录
        :param latitude: 会议室所在建筑纬度,可通过腾讯地图坐标拾取器获取
        :param longitude: 会议室所在建筑经度,可通过腾讯地图坐标拾取器获取
        """
        data = {
            "meetingroom_id": meetingroom_id,
            "name": name,
            "capacity": capacity,
        }
        if all([city, building, floor]):
            data["city"] = city
            data["building"] = building
            data["floor"] = floor
        if equipment:
            data["equipment"] = equipment
        if latitude and longitude:
            data["coordinate"] = {"latitude": latitude, "longitude": longitude}
        return self._post("oa/meetingroom/edit", data=data)

    def delete_meetingroom(self, meetingroom_id: int) -> dict:
        """
        删除会议室
        https://developer.work.weixin.qq.com/document/path/93619
        """
        return self._post("oa/meetingroom/del", data={"meetingroom_id": meetingroom_id})

    def get_meetingroom_booking_info(
        self,
        meetingroom_id: int = None,
        start_time: int = None,
        end_time: int = None,
        city: str = None,
        building: str = None,
        floor: str = None,
    ) -> dict:
        """
        查询会议室的预定信息
        https://developer.work.weixin.qq.com/document/path/93619

        - 如果需要根据位置信息查询，则需要保证其上一级的位置信息已填写，即如需使用楼宇进行过滤，则必须同时填写城市字段。

        :param meetingroom_id: 会议室id
        :param start_time: 查询预定的起始时间，默认为当前时间
        :param end_time: 查询预定的结束时间， 默认为明日0时
        :param city: 会议室所在城市
        :param building: 会议室所在楼宇
        :param floor: 会议室所在楼层
        """
        data = {
            "meetingroom_id": meetingroom_id,
            "start_time": start_time,
            "end_time": end_time,
            "city": city,
            "building": building,
            "floor": floor,
        }
        data = {k: v for k, v in data.items() if v is not None}
        return self._post("oa/meetingroom/get_booking_info", data=data)

    def book_meetingroom(
        self,
        meetingroom_id: int,
        start_time: int,
        end_time: int,
        booker: str,
        subject: str = None,
        attendees: list = None,
    ) -> dict:
        """
        预定会议室
        https://developer.work.weixin.qq.com/document/path/93619

        :param meetingroom_id: 会议室id
        :param start_time: 预定开始时间
        :param end_time: 预定结束时间
        :param booker: 预定人的userid
        :param subject: 会议主题
        :param attendees: 参与人的userid列表
        """
        data = {
            "meetingroom_id": meetingroom_id,
            "start_time": start_time,
            "end_time": end_time,
            "booker": booker,
        }
        if subject:
            data["subject"] = subject
        if attendees:
            data["attendees"] = attendees
        return self._post("oa/meetingroom/book", data=data)

    def cancle_meetingroom_book(self, meeting_id: str, keep_schedule=None) -> dict:
        """
        取消预定会议室
        https://developer.work.weixin.qq.com/document/path/93619

        :param meeting_id: 会议的id
        :param keep_schedule: 是否保留日程，0-同步删除 1-保留
        """
        data = {"meeting_id": meeting_id}
        if keep_schedule is not None:
            data["keep_schedule"] = keep_schedule
        return self._post("oa/meetingroom/cancel_book", data=data)

    def get_booking_info_by_meeting_id(self, meetingroom_id: int, meeting_id: str) -> dict:
        """
        根据会议ID查询会议室的预定信息
        https://developer.work.weixin.qq.com/document/path/93619

        :param meetingroom_id: 会议室id
        :param meeting_id: 会议的id
        """
        data = {
            "meetingroom_id": meetingroom_id,
            "meeting_id": meeting_id,
        }
        return self._post("oa/meetingroom/get_booking_info_by_meeting_id", data=data)
