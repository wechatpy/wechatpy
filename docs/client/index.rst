微信主动调用接口
===========================================

.. module:: wechatpy.client

.. autoclass:: WeChatClient
   :members:
   :inherited-members:

`WeChatClient` 基本使用方法::

   from wechatpy import WeChatClient

   client = WeChatClient('app_id', 'secret')
   user = client.user.get('user id')
   menu = client.menu.get()
   client.message.send_text('user id', 'content')
   # 以此类推，参见下面的 API 说明
   # client.media.xxx()
   # client.group.xxx()

如果不提供 ``session`` 参数，默认使用 ``wechatpy.session.memorystorage.MemoryStorage`` session 类型，
注意该类型不是线程安全的，不推荐生产环境使用。

.. toctree::
   :maxdepth: 2
   :glob:

   *
