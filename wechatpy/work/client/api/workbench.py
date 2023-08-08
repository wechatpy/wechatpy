#!/usr/bin/python3
# @Time    : 2023-08-08
# @Author  : Kevin Kong (kfx2007@163.com)

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatWorkBench(BaseWeChatAPI):

    """
    工作台相关接口

    参考文档:
    https://developer.work.weixin.qq.com/document/path/92535
    """

    def set_template(self, type, agentid, keydata=None, image=None, list=None, webview=None, replace_user_data=False):
        """
        设置应用在工作台展示的模版

        :params type: 模版类型，目前支持的自定义类型包括 "keydata"、 "image"、 "list"、 "webview" 。若设置的type为 "normal",则相当于从自定义模式切换为普通宫格或者列表展示模式
        :params agentid: 应用id,
        :params keydata: 若type指定为 "keydata"，且需要设置企业级别默认数据，则需要设置关键数据型模版数据,数据结构参考"关键数据型"
        :params image: 若type指定为 "image"，且需要设置企业级别默认数据，则需要设置图片型模版数据,数据结构参考“图片型
        :params list: 若type指定为 "list"，且需要设置企业级别默认数据，则需要设置列表型模版数据,数据结构参考“列表型”
        :params webview: 若type指定为 "webview"，且需要设置企业级别默认数据，则需要设置webview型模版数据,数据结构参考“webview型”
        :params replace_user_data: 是否覆盖用户工作台的数据。设置为true的时候，会覆盖企业所有用户当前设置的数据。若设置为false,则不会覆盖用户当前设置的所有数据。默认为false
        :return :接口结果
        """

        data = {
            "type": type,
            "agentid": agentid,
            "keydata": keydata,
            "image": image,
            "list": list,
            "webview": webview,
            "replace_user_data": replace_user_data,
        }

        return self._post("agent/set_workbench_template", data=data)

    def get_template(self, agentid):
        """
        获取应用在工作台展示的模版

        :params agentid: 应用id
        :return: 接口调用结果
        """

        data = {"agentid": agentid}

        return self._post("agent/get_workbench_template", data=data)

    def set_user_data(self, agentid, userid, type, keydata=None, image=None, list=None, webview=None):
        """
        设置应用在用户工作台展示的数据

        :params agentid: 应用id,
        :params type: 模版类型，目前支持的自定义类型包括 "keydata"、 "image"、 "list"、 "webview"
        :params keydata: 若type指定为 "keydata"，且需要设置企业级别默认数据，则需要设置关键数据型模版数据,数据结构参考"关键数据型"
        :params image: 若type指定为 "image"，且需要设置企业级别默认数据，则需要设置图片型模版数据,数据结构参考“图片型
        :params list: 若type指定为 "list"，且需要设置企业级别默认数据，则需要设置列表型模版数据,数据结构参考“列表型”
        :params webview: 若type指定为 "webview"，且需要设置企业级别默认数据，则需要设置webview型模版数据,数据结构参考“webview型”
        :return: 接口调用结果
        """

        data = {
            "agentid": agentid,
            "userid": userid,
            "type": type,
            "keydata": keydata,
            "image": image,
            "list": list,
            "webview": webview,
        }

        return self._post("agent/set_workbench_data", data=data)
