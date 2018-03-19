from __future__ import absolute_import, unicode_literals

import logging

from wechatpy.client import WeChatClient  # NOQA
from wechatpy.component import ComponentOAuth, WeChatComponent  # NOQA
from wechatpy.exceptions import WeChatClientException, WeChatException, WeChatOAuthException, WeChatPayException  # NOQA
from wechatpy.oauth import WeChatOAuth  # NOQA
from wechatpy.parser import parse_message  # NOQA
from wechatpy.pay import WeChatPay  # NOQA
from wechatpy.replies import create_reply  # NOQA

__version__ = '1.6.1'
__author__ = 'messense'

# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
