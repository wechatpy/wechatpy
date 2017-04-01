微信主动调用接口
===========================================

WeChatClient
--------------

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

.. module:: wechatpy.client.api

用户接口
----------------------

.. autoclass:: WeChatUser
   :members:
   :inherited-members:

用户分组接口
----------------------

.. autoclass:: WeChatGroup
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

二维码接口
---------------------------

.. autoclass:: WeChatQRCode
   :members:
   :inherited-members:

工具类接口
--------------------------

.. autoclass:: WeChatMisc
   :members:
   :inherited-members:

卡券接口
-------------------------

.. autoclass:: WeChatCard
   :members:
   :inherited-members:

微信小店接口
--------------------------

.. autoclass:: WeChatMerchant
   :members:
   :inherited-members:


客服消息接口
------------------------------------

.. autoclass:: WeChatCustomService
   :members:
   :inherited-members:


数据分析接口
-------------------------------

.. autoclass:: WeChatDataCube
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
   :inherited-members:


语义理解接口
-------------------------------

.. autoclass:: WeChatSemantic
   :members:
   :inherited-members:


摇一摇周边接口
---------------------------------

.. autoclass:: WeChatShakeAround
   :members:
   :inherited-members:

设备功能接口
---------------------------

.. autoclass:: WeChatDevice
   :members:
   :inherited-members:


模板消息相关接口
---------------------------------

.. autoclass:: WeChatTemplate
   :members:
   :inherited-members:


微信连 Wi-Fi 接口
----------------------------------

.. autoclass:: WeChatWiFi
   :members:
   :inherited-members:

微信扫一扫接口
----------------------------------

.. autoclass:: WeChatScan
   :members:
   :inherited-members:
