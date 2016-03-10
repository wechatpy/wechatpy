微信主动调用接口操作类
===========================================

WeChatClient
--------------

.. module:: wechatpy.client

.. autoclass:: WeChatClient
   :members:

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

.. module:: wechatpy.client.api

用户接口
----------------------

.. autoclass:: WeChatUser
   :members:

用户分组接口
----------------------

.. autoclass:: WeChatGroup
   :members:

主动消息接口
-----------------------------

.. autoclass:: WeChatMessage
   :members:

自定义菜单接口
----------------------------

.. autoclass:: WeChatMenu
   :members:

媒体文件接口
---------------------------

.. autoclass:: WeChatMedia
   :members:

二维码接口
---------------------------

.. autoclass:: WeChatQRCode
   :members:

工具类接口
--------------------------

.. autoclass:: WeChatMisc
   :members:

卡券接口
-------------------------

.. autoclass:: WeChatCard
   :members:

微信小店接口
--------------------------

.. autoclass:: WeChatMerchant
   :members:


客服消息接口
------------------------------------

.. autoclass:: WeChatCustomService
   :members:


数据分析接口
-------------------------------

.. autoclass:: WeChatDataCube
   :members:


JS-SDK 接口
---------------------------

.. autoclass:: WeChatJSAPI
   :members:


素材接口
--------------------------

.. autoclass:: WeChatMaterial
   :members:


语义理解接口
-------------------------------

.. autoclass:: WeChatSemantic
   :members:


摇一摇周边接口
---------------------------------

.. autoclass:: WeChatShakeAround
   :members:

设备功能接口
---------------------------

.. autoclass:: WeChatDevice
   :members:


模板消息相关接口
---------------------------------

.. autoclass:: WeChatTemplate
   :members:


微信连 Wi-Fi 接口
----------------------------------

.. autoclass:: WeChatWiFi
   :members:

微信扫一扫接口
----------------------------------

.. autoclass:: WeChatScan
   :members:
