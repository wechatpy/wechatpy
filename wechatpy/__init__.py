from __future__ import absolute_import, unicode_literals
try:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)
except ImportError:
    from pkg_resources import declare_namespace
    declare_namespace(__name__)

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


__version__ = '1.2.8'
__author__ = 'messense'
