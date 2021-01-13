# -*- coding: utf-8 -*-


from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatExternalContactGroupChat(BaseWeChatAPI):
    """
    https://work.weixin.qq.com/api/doc#90000/90135/90221
    """

    def list(
            self, status_filter: int = 0, owner_userid_list: list = None, cursor: str = None, limit: int = 100
    ):
        """
        该接口用于获取配置过客户群管理的客户群列表。
        https://work.weixin.qq.com/api/doc/90000/90135/92120
        :return: 返回的 JSON 数据包
        :param status_filter: 客户群跟进状态过滤。[0 - 所有列表(即不过滤)
                                                1 - 离职待继承
                                                2 - 离职继承中
                                                3 - 离职继承完成

                                                默认为0]
        :param owner_userid_list: 根据群主id过滤。如果不填，表示获取应用可见范围内全部群主的数据（但是不建议这么用，如果可见范围人数超过1000人，为了防止数据包过大，会报错 81017）
        :param cursor: 用于分页查询的游标，字符串类型，由上一次调用返回，首次调用不填
        :param limit: 分页，预期请求的数据量，取值范围 1 ~ 1000， 默认100
        :return:
        """
        data = optionaldict(
            status_filter=status_filter,
            cursor=cursor,
            limit=limit,
        )
        if owner_userid_list:
            data['owner_filter'] = {"userid_list": owner_userid_list}
        return self._post("externalcontact/groupchat/list", data=data)

    def get(self, chat_id: str):
        """
        通过客户群ID，获取详情。包括群名、群成员列表、群成员入群时间、入群方式。（客户群是由具有客户群使用权限的成员创建的外部群）
        需注意的是，如果发生群信息变动，会立即收到群变更事件，但是部分信息是异步处理，可能需要等一段时间调此接口才能得到最新结果
        PS: 接口命名为get，调用却是POST，无语
        https://work.weixin.qq.com/api/doc/90000/90135/92122
        :param chat_id: 客户群ID
        :return: 返回的 JSON 数据包
        """
        return self._post("externalcontact/groupchat/get", data={"chat_id": chat_id})
