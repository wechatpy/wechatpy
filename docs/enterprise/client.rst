企业号主动调用接口
==============================

WeChatClient
------------------

.. module:: wechatpy.enterprise.client

.. autoclass:: WeChatClient
   :members:
   :inherited-members:

`WeChatClient` 基本使用方法::

   from wechatpy.enterprise import WeChatClient

   client = WeChatClient('corp_id', 'secret')
   user = client.user.get('user id')
   menu = client.menu.get()
   client.message.send_text('agent id', 'user id', 'content')
   # 以此类推，参见下面的 API 说明
   # client.media.xxx()
   # client.tag.xxx()

如果不提供 ``session`` 参数，默认使用 ``wechatpy.session.memorystorage.MemoryStorage`` session 类型，
注意该类型不是线程安全的，不推荐生产环境使用。

.. module:: wechatpy.enterprise.client.api


用户接口
----------------------

.. autoclass:: WeChatUser
   :members:
   :inherited-members:

标签接口
----------------------

.. autoclass:: WeChatTag
   :members:
   :inherited-members:

主动消息接口
-----------------------------

.. autoclass:: WeChatMessage
   :members:
   :inherited-members:

自定义菜单接口
----------------------------

.. autoclass:: WeChatMenu
   :members:
   :inherited-members:

媒体文件接口
---------------------------

.. autoclass:: WeChatMedia
   :members:
   :inherited-members:

工具类接口
--------------------------

.. autoclass:: WeChatMisc
   :members:
   :inherited-members:

JS-SDK 接口
---------------------------

.. autoclass:: WeChatJSAPI
   :members:
   :inherited-members:


素材接口
--------------------------

.. autoclass:: WeChatMaterial
   :members:

摇一摇周边接口
---------------------------------

.. autoclass:: WeChatShakeAround
   :members:
   :inherited-members:
