from __future__ import absolute_import, unicode_literals

import logging

from wechatpy.parser import parse_message  # NOQA
from wechatpy.replies import create_reply  # NOQA
from wechatpy.client import WeChatClient  # NOQA
from wechatpy.exceptions import WeChatException  # NOQA
from wechatpy.exceptions import WeChatClientException  # NOQA
from wechatpy.oauth import WeChatOAuth  # NOQA
from wechatpy.exceptions import WeChatOAuthException  # NOQA
from wechatpy.pay import WeChatPay  # NOQA
from wechatpy.exceptions import WeChatPayException  # NOQA
from wechatpy.component import WeChatComponent  # NOQA


__version__ = '1.5.4'
__author__ = 'messense'

# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
