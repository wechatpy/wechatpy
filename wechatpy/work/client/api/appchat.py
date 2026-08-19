# -*- coding: utf-8 -*-


from optionaldict import optionaldict

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatAppChat(BaseWeChatAPI):
    """发送消息到群聊会话
    https://work.weixin.qq.com/api/doc#90000/90135/90244
    """

    def create(self, chat_id=None, name=None, owner=None, user_list=None):
        """
        创建群聊会话

        详情请参考
        https://work.weixin.qq.com/api/doc#90000/90135/90245

        限制说明：
        只允许企业自建应用调用，且应用的可见范围必须是根部门；
        群成员人数不可超过管理端配置的“群成员人数上限”，且最大不可超过500人；
        每企业创建群数不可超过1000/天；

        :param chat_id: 群聊的唯一标志，不能与已有的群重复；字符串类型，最长32个字符。只允许字符0-9及字母a-zA-Z。如果不填，系统会随机生成群id
        :param name: 群聊名，最多50个utf8字符，超过将截断
        :param owner: 指定群主的id。如果不指定，系统会随机从userlist中选一人作为群主
        :param user_list: 会话成员列表，成员用userid来标识。至少2人，至多500人
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(
            chatid=chat_id,
            name=name,
            owner=owner,
            userlist=user_list,
        )
        return self._post("appchat/create", data=data)

    def get(self, chat_id):
        """
        获取群聊会话

        详情请参考
        https://work.weixin.qq.com/api/doc#90000/90135/90247

        :param chat_id: 群聊id
        :return: 会话信息
        """
        res = self._get("appchat/get", params={"chatid": chat_id})
        return res["chat_info"]

    def update(self, chat_id, name=None, owner=None, add_user_list=None, del_user_list=None):
        """
        修改群聊会话

        详情请参考
        https://work.weixin.qq.com/api/doc#90000/90135/90246

        :param chat_id: 群聊id
        :param name: 新的群聊名。若不需更新，请忽略此参数。最多50个utf8字符，超过将截断
        :param owner: 新群主的id。若不需更新，请忽略此参数
        :param add_user_list: 会话新增成员列表，成员用userid来标识
        :param del_user_list: 会话退出成员列表，成员用userid来标识
        :return: 返回的 JSON 数据包
        """
        data = optionaldict(
            chatid=chat_id,
            name=name,
            owner=owner,
            add_user_list=add_user_list,
            del_user_list=del_user_list,
        )
        return self._post("appchat/update", data=data)

    def send(self, chat_id, msg_type, **kwargs):
        """
        应用推送消息

        详情请参考：https://work.weixin.qq.com/api/doc#90000/90135/90248
        :param chat_id: 群聊id
        :param msg_type: 消息类型，可以为text/image/voice/video/file/textcard/news/mpnews/markdown
        :param kwargs: 具体消息类型的扩展参数
        :return:
        """
        data = {"chatid": chat_id, "safe": kwargs.get("safe") or 0}
        data.update(self._build_msg_content(msg_type, **kwargs))

        return self._post("appchat/send", data=data)

    def send_text(self, chat_id, content, safe=0):
        """
        发送文本消息

        详情请参考：https://work.weixin.qq.com/api/doc#90000/90135/90248/文本消息/

        :param chat_id: 群聊id
        :param content: 消息内容
        :param safe: 表示是否是保密消息，0表示否，1表示是，默认0
        :return:
        """
        return self.send(chat_id, "text", safe=safe, content=content)

    def _build_msg_content(self, msgtype="text", **kwargs):
        """
        构造消息内容

        :param content: 消息内容，最长不超过2048个字节
        :param msgtype: 消息类型，可以为text/image/voice/video/file/textcard/news/mpnews/markdown
        :param kwargs: 具体消息类型的扩展参数
        :return:
        """
        data = {"msgtype": msgtype}
        if msgtype == "text":
            data[msgtype] = {"content": kwargs.get("content")}
        elif msgtype == "image" or msgtype == "voice" or msgtype == "file":
            data[msgtype] = {"media_id": kwargs.get("media_id")}
        elif msgtype == "video":
            data[msgtype] = {
                "media_id": kwargs.get("media_id"),
                "title": kwargs.get("title"),
                "description": kwargs.get("description"),
            }
        elif msgtype == "textcard":
            data[msgtype] = {
                "title": kwargs.get("title"),
                "description": kwargs.get("description"),
                "url": kwargs.get("url"),
                "btntxt": kwargs.get("btntxt"),
            }
        elif msgtype == "news":
            # {
            #         "articles" :
            #         [
            #             {
            #                 "title" : "中秋节礼品领取",
            #                 "description" : "今年中秋节公司有豪礼相送",
            #                 "url":"https://zhidao.baidu.com/question/2073647112026042748.html",
            #                 "picurl":"http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
            #              }
            #         ]
            #     }
            data[msgtype] = kwargs
        elif msgtype == "mpnews":
            # {
            #         "articles":[
            #             {
            #                 "title": "地球一小时",
            #                 "thumb_media_id": "biz_get(image)",
            #                 "author": "Author",
            #                 "content_source_url": "https://work.weixin.qq.com",
            #                 "content": "3月24日20:30-21:30 \n办公区将关闭照明一小时，请各部门同事相互转告",
            #                 "digest": "3月24日20:30-21:30 \n办公区将关闭照明一小时"
            #             }
            #          ]
            #     }
            data[msgtype] = kwargs
        elif msgtype == "markdown":
            #  {
            #         "content": "您的会议室已经预定，稍后会同步到`邮箱`
            #                 >**事项详情**
            #                 >事　项：<font color=\"info\">开会</font>
            #                 >组织者：@miglioguan
            #                 >参与者：@miglioguan、@kunliu、@jamdeezhou、@kanexiong、@kisonwang
            #                 >
            #                 >会议室：<font color=\"info\">广州TIT 1楼 301</font>
            #                 >日　期：<font color=\"warning\">2018年5月18日</font>
            #                 >时　间：<font color=\"comment\">上午9:00-11:00</font>
            #                 >
            #                 >请准时参加会议。
            #                 >
            #                 >如需修改会议信息，请点击：[修改会议信息](https://work.weixin.qq.com)"
            #    }
            data[msgtype] = kwargs
        else:
            raise TypeError(f"不能识别的msgtype: {msgtype}")
        return data
