from __future__ import absolute_import, unicode_literals
from .messages import MESSAGE_TYPES
from .events import EVENT_TYPES
from ..messages import UnknownMessage


def parse_message(message):
    message_type = message['MsgType'].lower()
    if message_type == 'event':
        event_type = message['Event'].lower()
        message_class = EVENT_TYPES.get(event_type, UnknownMessage)
    else:
        message_class = MESSAGE_TYPES.get(message_type, UnknownMessage)
    return message_class(message)
