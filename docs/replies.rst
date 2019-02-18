.. _replies:

回复
======

公共属性
----------

每一种类型的回复都有如下属性：

======= ===============================
name    value
======= ===============================
type    回复类型
source  回复的来源用户，通常是发送回复的用户。
target  回复的目标用户
time    回复的发送时间
======= ===============================

每一种类型的回复都有一个 ``render`` 方法将回复转换成 XML 字符串:

.. code-block:: python

    from wechatpy.replies import TextReply

    reply = TextReply()
    reply.source = 'user1'
    reply.target = 'user2'
    reply.content = 'test'

    xml = reply.render()

你可以在构建 Reply 时传入一个合法的 Message 对象来自动生成 source 和 target:

.. code-block:: python

    reply = TextReply(content='test', message=message)


.. module:: wechatpy.replies

文本回复
------------------------

.. autoclass:: TextReply
   :members:
   :inherited-members:

======= ===============================
name    value
======= ===============================
type    text
content 回复正文
======= ===============================

图片回复
------------------------

.. autoclass:: ImageReply
   :members:
   :inherited-members:

========= ===============================
name      value
========= ===============================
type      image
media_id  通过上传多媒体文件，得到的 id
========= ===============================

语音回复
------------------------

.. autoclass:: VoiceReply
   :members:
   :inherited-members:

========= ===============================
name      value
========= ===============================
type      voice
media_id  通过上传多媒体文件，得到的 id
========= ===============================

视频回复
------------------------

.. autoclass:: VideoReply
   :members:
   :inherited-members:

============= ===============================
name          value
============= ===============================
type          video
media_id      通过上传多媒体文件，得到的 id
title         视频回复的标题
description   视频回复的描述
============= ===============================

音乐回复
-----------------------

.. autoclass:: MusicReply
   :members:
   :inherited-members:

================ =======================================
name             value
================ =======================================
type             music
thumb_media_id   缩略图的媒体 id，通过上传多媒体文件，得到的 id
title            音乐回复的标题
description      音乐回复的描述
music_url        音乐链接
hq_music_url     高质量音乐链接，WiFi 环境优先使用该链接播放音乐
================ =======================================

图文回复
-------------------------

.. autoclass:: ArticlesReply
   :members:
   :inherited-members:

============= ===============================
name          value
============= ===============================
type          news
============= ===============================

你需要给 ArticlesReply 添加 article 来增加图文，使用 ArticlesReply 的 add_article 方法或者设置 ArticlesReply 的 articles 属性。article 应当是 dict like 的对象（只要其能响应和 dict 一致的 get 方法即可），其应当包含如下属性(键值):

============= ===============================
name          value
============= ===============================
title         图文回复标题
description   图文回复描述
image         图片链接
url           点击图文消息跳转链接
============= ===============================

使用示例:

.. code-block:: python

    from wechatpy.replies import ArticlesReply
    from wechatpy.utils import ObjectDict

    reply = ArticlesReply(message=message)
    # simply use dict as article
    reply.add_article({
        'title': 'test',
        'description': 'test',
        'image': 'image url',
        'url': 'url'
    })
    # or you can use ObjectDict
    article = ObjectDict()
    article.title = 'test'
    article.description = 'test'
    article.image = 'image url'
    article.url = 'url'
    reply.add_article(article)


将消息转发到多客服
-----------------------------------------------

.. autoclass:: TransferCustomerServiceReply
   :members:
   :inherited-members:

============= ===============================
name          value
============= ===============================
type          transfer_customer_service
============= ===============================

回复空串
-----------------------------------------------

.. autoclass:: EmptyReply
   :members:

微信服务器不会对此作任何处理，并且不会发起重试,
可以使用客服消息接口进行异步回复。

快速构建回复
-------------

wechatpy 提供了一个便捷的 create_reply 函数用来快速构建回复 :

.. code-block:: python

    from wechatpy import create_reply

    empty_reply = create_reply('')

    text_reply = create_reply('text reply', message=message)

    articles = [
        {
            'title': 'test',
            'description': 'test',
            'image': 'image url',
            'url': 'url'
        },
        # add more ...
    ]

    articles_reply = create_reply(articles, message=message)

反序列化回复
-------------

wechatpy 提供一个deserialize_reply方法来反序列化xml回复为 ``wechatpy.replies.BaseReply`` :

.. code-block:: python

    from wechatpy.replies import deserialize_reply

    origin_reply = create_reply('text reply', message=message)
    xml = origin_reply.render()
    deserialized_reply = deserialize_reply(xml)
