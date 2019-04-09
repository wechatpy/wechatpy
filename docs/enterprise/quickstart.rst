企业微信快速上手
===========================================
基于企业微信的开发一般分为如下两种

* 回调模式
    * 用户通过公众号产生的一系列消息（例如普通文本消息、扫码事件消息、微信支付成功事件消息）
    * 开发者需要根据不同的消息，做出对应的响应
    * 此模式下，可以理解为微信服务器作为开发者服务器的客户端对开发者服务器发送 HTTP 请求（一般情况下为 POST）
* 主动调用
    * 开发者可以通过企业微信提供的 API 做出一系列操作，例如向用户主动推送消息

微信回调模式接入
-------------------------

验证请求有效性
~~~~~~~~~~~~~~~~~~~~~~

微信企业号只有微信订阅号的 **安全模式** ，所以对于回调模式下的请求都是经过 AES 加密过的。

.. code-block:: python

    from wechatpy.enterprise.crypto import WeChatCrypto
    from wechatpy.exceptions import InvalidSignatureException

    crypto = WeChatCrypto(TOKEN, EncodingAESKey, CorpId)
    try:
        echo_str = crypto.check_signature(
            signature,
            timestamp,
            nonce,
            echo_str
        )
    except InvalidSignatureException:
        raise  # 处理异常情况

解析 XML 消息
~~~~~~~~~~~~~~~~~~~~~~
微信服务器发送来的消息在 HTTP 请求的 body 中，将微信服务器当做浏览器客户端，所以微信的 XML 消息正文在 ``Flask`` 中是 ``request.data``，在 ``Tornado`` 中是 ``self.request.body``。

假设开发者将 XML 消息正文储存在变量 ``raw_message`` 中

.. code-block:: python

    from wechatpy.enterprise.crypto import WeChatCrypto
    from wechatpy.exceptions import InvalidSignatureException
    from wechatpy.enterprise.exceptions import InvalidCorpIdException
    from wechatpy.enterprise import parse_message

    crypto = WeChatCrypto(TOKEN, EncodingAESKey, CorpId)

    try:
        decrypted_xml = crypto.decrypt_message(
            raw_message,
            signature,
            timestamp,
            nonce
        )
    except (InvalidSignatureException, InvalidCorpIdException):
        raise  # 处理异常情况
    else:
        msg = parse_message(decrypted_xml)

对于解析后的消息可以参考 :ref:`推送消息 <messages>` 和 :ref:`推送事件 <events>` 文档，基本与订阅号一致。

回复消息
~~~~~~~~~~~~~~~~~~~~~~
企业号回复的消息也是经过 AES 加密过的，具体的回复消息也与订阅号基本一致。

.. code-block:: python

    from wechatpy.enterprise import parse_message, create_reply
    from wechatpy.enterprise.crypto import WeChatCrypto

    crypto = WeChatCrypto(TOKEN, EncodingAESKey, CorpId)

    xml = create_reply(msg.content, msg).render()
    encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)

基于 Flask 框架的示例可参考 https://github.com/jxtech/wechatpy/tree/master/examples/echo-enterprise

微信主动调用模式接入
-------------------------
对于主动调用 wechatpy 提供了主动调用模式的操作类 ``wechatpy.enterprise.WeChatClient``

.. code-block:: python

    from wechatpy.enterprise import WeChatClient
    wechat_client = WeChatClient(
        CorpId,
        secret
    )

AccessToken
~~~~~~~~~~~~~~~~~~~~~~
wechatpy 对于微信的 **AccessToken** 会在内部自动处理，一般情况下开发者不需要手动去操作，如果开发者需要访问 **AccessToken**，可以通过 `wechat_client.access_token <http://docs.wechatpy.org/zh_CN/master/enterprise/client.html#wechatpy.enterprise.client.WeChatClient.access_token>`_ 获取到。

Storage
..................
wechatpy 支持多种 **AccessToken** 的持久化储存，目前支持 memcached，memory，redis，shove

Redis 示例:

.. code-block:: python

    from wechatpy.enterprise import WeChatClient
    from wechatpy.session.redisstorage import RedisStorage
    from redis import Redis

    redis_client = Redis.from_url('redis://127.0.0.1:6379/0')
    session_interface = RedisStorage(
        redis_client,
        prefix="wechatpy"
    )

    wechat_client = WeChatClient(
        CorpId,
        secret,
        session=session_interface
    )

Shove 示例:

.. code-block:: python

    from wechatpy.session.shovestorage import ShoveStorage
  
memcached 示例:

.. code-block:: python

    from wechatpy.session.memcachedstorage import MemcachedStorage
  
memory 示例:

.. code-block:: python

    from wechatpy.session.memorystorage import MemoryStorage

自定义 Storage
!!!!!!!!!!!!!!
对于 wechatpy 不支持的 Storage，也可以自定义 Storage，要使用 Storage，首先要实现自定义的 Storage，自定义的 Storage 需要实现 ``get`` 、 ``set`` 和 ``delete``，具体示例如下

.. code-block:: python

    from wechatpy.session import SessionStorage

    class CustomStorage(SessionStorage):

        def __init__(self, *args, **kwargs):
            pass

        def get(self, key, default=None):
            pass

        def set(self, key, value, ttl=None):
            pass

        def delete(self, key):
            pass

    wechat_client = WeChatClient(
        CorpId,
        secret,
        session=CustomStorage()
    )
