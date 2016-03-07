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

假设被动响应收到的消息解析后保存在变量 ``msg`` 中

回复文本消息
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from wechatpy.replies import TextReply

    reply = TextReply(content='text reply', message=msg)
    # 或者
    reply = TextReply(message=msg)
    reply.content = 'text reply'
    # 转换成 XML
    xml = reply.render()

快速回复文本消息：

.. code-block:: python

    from wechatpy.replies import create_reply

    reply = create_reply('text reply', message=msg)
    # 转换成 XML
    xml = reply.render()

回复图片消息
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from wechatpy.replies import ImageReply

    reply = ImageReply(message=msg)
    reply.media_id = 'image media id'
    # 转换成 XML
    xml = reply.render()

回复语音消息
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from wechatpy.replies import VoiceReply

    reply = VoiceReply(message=msg)
    reply.media_id = 'voice media id'
    # 转换成 XML
    xml = reply.render()

回复图文消息
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from wechatpy.replies import ArticlesReply

    reply = ArticlesReply(message=msg, articles=[
        {
            'title': u'标题1',
            'description': u'描述1',
            'url': u'http://www.qq.com',
        },
        {
            'title': u'标题2',
            'description': u'描述2',
            'url': u'http://www.qq.com',
            'image': 'http://img.qq.com/1.png',
        },
    ])
    # 继续添加
    reply.add_article({
        'title': u'标题3',
        'description': u'描述3',
        'url': u'http://www.qq.com',
    })
    # 转换成 XML
    xml = reply.render()

更多回复类型请参考 :ref:`回复 <replies>` 文档。

加密模式回复处理
^^^^^^^^^^^^^^^^^^^^^^

对于加密模式，在将回复转换成 XML 后，还需要将其加密后返回给微信服务器。

假设你的 token 变量名为 ``token`` ，AES key 变量名为 ``encoding_aes_key``, App Id 变量名为 ``appid``,
并且你已经从请求参数中提取了 ``timestamp``, ``nonce`` 参数。将 ``xml`` 加密：

.. code-block:: python

    from wechatpy.crypto import WeChatCrypto

    crypto = WeChatCrypto(token, encoding_aes_key, appid)
    encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)

基于 Flask Web 框架的简单的加密模式示例可参考 https://github.com/jxtech/wechatpy/tree/master/examples/echo-encrypted

基于 Flask Web 框架的自适应加密和明文模式示例可参考 https://github.com/jxtech/wechatpy/tree/master/examples/echo

微信主动调用接口使用
-------------------------

TODO
