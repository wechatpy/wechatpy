快速上手
=============

微信回调被动响应接入
-------------------------

验证请求有效性
~~~~~~~~~~~~~~~~~~~~~~

假设你已经从微信服务器推送的请求参数中获取了 ``signature``, ``timestamp`` 和 ``nonce`` 参数，以及回调 ``token``

.. code-block:: python

    from wechatpy.utils import check_signature
    from wechatpy.exceptions import InvalidSignatureException

    try:
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        # 处理异常情况或忽略

解析 XML 消息
~~~~~~~~~~~~~~~~~~~~

假设你已经从微信服务器推送的请求中获取了该 XML 消息正文并存储在变量 ``xml`` 中

对于明文模式，

.. code-block:: python

    from wechatpy import parse_message

    msg = parse_message(xml)

对于加密模式，假设你的 token 变量名为 ``token`` ，AES key 变量名为 ``encoding_aes_key``, App Id 变量名为 ``appid``,
并且你已经从请求参数中提取了 ``msg_signature``, ``timestamp``, ``nonce`` 参数。将加密过的 XML 解密：

.. code-block:: python

    from wechatpy import parse_message
    from wechatpy.crypto import WeChatCrypto
    from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException

    crypto = WeChatCrypto(token, encoding_aes_key, appid)
    try:
        decrypted_xml = crypto.decrypt_message(
            xml,
            msg_signature,
            timestamp,
            nonce
        )
    except (InvalidAppIdException, InvalidSignatureException):
        # 处理异常或忽略
        pass

    msg = parse_message(decrypted_xml)

对于解析后的消息类型等信息请参考 :ref:`推送消息 <messages>` 和 :ref:`推送事件 <events>` 文档。

回复消息
~~~~~~~~~~~~~~

TODO

微信主动调用接口使用
-------------------------

TODO
