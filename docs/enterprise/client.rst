企业微信主动调用接口
==============================

企业微信有 ``企业内部开发`` ， ``第三方应用开发`` 和 ``智慧硬件开发`` 三种接入场景。
同一个接口根据场景不容，掺入参数的含义可能不一样。开发过程中，请根据实际场景，按照文档传入正确的参数。
部分“微信企业号”文档存在，企业微信 API 文档不存在的接口，名称后面会标注 ``(旧接口，建议更换)`` 。建议更换成企业微信提供的新接口。

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

应用管理
----------------------
.. autoclass:: WeChatAgent
   :members:
   :inherited-members:

群聊会话
----------------------
.. autoclass:: WeChatAppChat
   :members:
   :inherited-members:

异步任务
----------------------
.. autoclass:: WeChatBatch
   :members:
   :inherited-members:

企业会话(旧接口，建议更换)
----------------------
.. autoclass:: WeChatChat
   :members:
   :inherited-members:

部门管理
----------------------

.. autoclass:: WeChatDepartment
   :members:
   :inherited-members:

JS-SDK 接口
---------------------------

.. autoclass:: WeChatJSAPI
   :members:
   :inherited-members:

素材接口(旧接口，建议更换)
--------------------------

.. autoclass:: WeChatMaterial
   :members:
   :inherited-members:

素材管理
---------------------------

.. autoclass:: WeChatMedia
   :members:
   :inherited-members:

自定义菜单
----------------------------

.. autoclass:: WeChatMenu
   :members:
   :inherited-members:

应用消息
-----------------------------

.. autoclass:: WeChatMessage
   :members:
   :inherited-members:

工具类接口
--------------------------

.. autoclass:: WeChatMisc
   :members:
   :inherited-members:

身份验证(OAuth2)
--------------------------

.. autoclass:: WeChatOAuth
   :members:
   :inherited-members:

应用授权（服务商、第三方应用开发相关）
--------------------------

.. autoclass:: WeChatService
   :members:
   :inherited-members:

摇一摇周边接口(旧接口，建议更换)
---------------------------------

.. autoclass:: WeChatShakeAround
   :members:
   :inherited-members:

标签管理
----------------------

.. autoclass:: WeChatTag
   :members:
   :inherited-members:

用户管理
----------------------

.. autoclass:: WeChatUser
   :members:
   :inherited-members:
