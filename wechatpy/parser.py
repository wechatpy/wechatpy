# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from xml.etree import ElementTree
import six

from .messages import MESSAGE_TYPES, UnknownMessage
from .events import EVENT_TYPES


def parse_message(xml):
    if not xml:
        return
    to_text = six.text_type
    parser = ElementTree.fromstring(to_text(xml).encode('utf-8'))
    message = dict((child.tag, to_text(child.text)) for child in parser)
    message_type = message['MsgType'].lower()
    if message_type == 'event':
        event_type = message['Event'].lower()
        if event_type == 'subscribe' and 'EventKey' in message:
            # Scan to subscribe with scene id event
            event_type = 'subscribe_scan'
            message['EventKey'] = message['EventKey'].replace('qrscene_', '')
        message_class = EVENT_TYPES.get(event_type, UnknownMessage)
    else:
        message_class = MESSAGE_TYPES.get(message_type, UnknownMessage)
    return message_class(message)
