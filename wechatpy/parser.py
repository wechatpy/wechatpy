# -*- coding: utf-8 -*-
"""
    wechatpy.parser
    ~~~~~~~~~~~~~~~~
    This module provides functions for parsing WeChat messages

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
import xmltodict

from wechatpy.messages import MESSAGE_TYPES, UnknownMessage
from wechatpy.events import EVENT_TYPES
from wechatpy.utils import to_text


def parse_message(xml):
    """
    解析微信服务器推送的 XML 消息

    :param xml: XML 消息
    :return: 解析成功返回对应的消息或事件，否则返回 ``UnknownMessage``
    """
    if not xml:
        return
    message = xmltodict.parse(to_text(xml))["xml"]
    message_type = message["MsgType"].lower()
    event_type = None
    if message_type == "event" or message_type.startswith("device_"):
        if "Event" in message:
            event_type = message["Event"].lower()
        # special event type for device_event
        if event_type is None and message_type.startswith("device_"):
            event_type = message_type
        elif message_type.startswith("device_"):
            event_type = f"device_{event_type}"

        if event_type == "subscribe" and message.get("EventKey"):
            event_key = message["EventKey"]
            if event_key.startswith(("scanbarcode|", "scanimage|")):
                event_type = "subscribe_scan_product"
                message["Event"] = event_type
            elif event_key.startswith("qrscene_"):
                # Scan to subscribe with scene id event
                event_type = "subscribe_scan"
                message["Event"] = event_type
                message["EventKey"] = event_key[len("qrscene_") :]
        message_class = EVENT_TYPES.get(event_type, UnknownMessage)
    else:
        message_class = MESSAGE_TYPES.get(message_type, UnknownMessage)
    return message_class(message)
