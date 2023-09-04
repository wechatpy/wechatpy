#!/usr/bin/python3
# @Time    : 2023-09-03
# @Author  : Kevin Kong (kfx2007@163.com)

from wechatpy.client.api.base import BaseWeChatAPI

class WeChatCheckIn(BaseWeChatAPI):

    """
    考勤相关接口

    参考文档:
    https://developer.work.weixin.qq.com/document/path/90262
    """

    def get(self,data_type,start_time,end_time,user_ids):
        """
        获取打卡记录数据

        :param data_type: 打卡类型。1：上下班打卡；2：外出打卡；3：全部打卡
        :param start_time: 获取打卡记录的开始时间。Unix时间戳
        :param end_time: 获取打卡记录的结束时间。Unix时间戳
        :param user_ids: 	需要获取打卡记录的用户列表

        :return: 接口结果
        """

        data = {
            "opencheckindatatype": data_type,
            "starttime": start_time,
            "endtime": end_time,
            "useridlist": user_ids
        }

        return self._post("checkin/getcheckindata", data=data)
