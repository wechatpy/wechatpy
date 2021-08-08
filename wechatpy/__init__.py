# -*- coding: utf-8 -*-
import logging

from wechatpy.client import WeChatClient  # NOQA
from wechatpy.component import ComponentOAuth, WeChatComponent  # NOQA
from wechatpy.exceptions import (
    WeChatClientException,
    WeChatException,
    WeChatOAuthException,
    WeChatPayException,
)  # NOQA
from wechatpy.oauth import WeChatOAuth  # NOQA
from wechatpy.parser import parse_message  # NOQA
from wechatpy.pay import WeChatPay  # NOQA
from wechatpy.replies import create_reply  # NOQA

__version__ = "2.0.0.alpha11"
__author__ = "messense"

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
