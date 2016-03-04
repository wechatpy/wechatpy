``wechatpy.WeChatClient`` - 微信 API 操作类
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

WeChatUser 用户 API
----------------------

.. autoclass:: WeChatUser
   :members:

WeChatGroup 分组 API
----------------------

.. autoclass:: WeChatGroup
   :members:

WeChatMessage 主动消息 API
-----------------------------

.. autoclass:: WeChatMessage
   :members:

WeChatMenu 自定义菜单 API
----------------------------

.. autoclass:: WeChatMenu
   :members:

WeChatMedia 媒体文件 API
---------------------------

.. autoclass:: WeChatMedia
   :members:

WeChatQRCode 二维码 API
---------------------------

.. autoclass:: WeChatQRCode
   :members:

WeChatMisc 工具类 API
--------------------------

.. autoclass:: WeChatMisc
   :members:

WeChatCard 卡券 API
-------------------------

.. autoclass:: WeChatCard
   :members:

WeChatMerchant 小店 API
--------------------------

.. autoclass:: WeChatMerchant
   :members:


WeChatCustomService 客服消息 API
------------------------------------

.. autoclass:: WeChatCustomService
   :members:


WeChatDataCube 数据分析 API
-------------------------------

.. autoclass:: WeChatDataCube
   :members:


WeChatJSAPI  JS-SDK API
---------------------------

.. autoclass:: WeChatJSAPI
   :members:


WeChatMaterial 素材 API
--------------------------

.. autoclass:: WeChatMaterial
   :members:


WeChatSemantic 语义理解 API
-------------------------------

.. autoclass:: WeChatSemantic
   :members:


WeChatShakeAround 摇一摇周边 API
---------------------------------

.. autoclass:: WeChatShakeAround
   :members:

WeChatDevice 设备功能 API
---------------------------

.. autoclass:: WeChatDevice
   :members:


WeChatTemplate 模板消息相关接口
---------------------------------

.. autoclass:: WeChatTemplate
   :members:


WeChatWiFi  微信连 Wi-Fi 接口
----------------------------------

.. autoclass:: WeChatWiFi
   :members:
