代公众号调用接口
=================

本模块提供了开放平台代公众号调用接口 API。进行公众号第三方平台开发的项目，可以从这里开始。

.. module:: wechatpy.component


WeChatComponent
---------------

WeChatComponent的基本使用方法:

.. code-block:: python

    from wechatpy import WeChatComponent
    component = WeChatComponent('app_id', 'app_secret', 'component_token', 'encoding_aes_key')

默认使用 ``wechatpy.session.memorystorage.MemoryStorage`` 缓存component的component_verify_ticket和授权码。通过component获取的公众号 client，也会使用component.session 作为缓存对象。

如果要使用外部的 session 对象，只要接口符合 ``wechatpy.session.SessionStorage`` ,都可以使用。只要增加 ``session=some_object`` 即可。

推荐使用外部的 session 对象，因为 ``wechatpy.session.memorystorage.MemoryStorage`` 暂不支持多线程操作。

此后，可以调用component的其它方法完成公众号的授权、令牌刷新、获取或者设置公众号信息等操作。


component_verify_ticket 的处理
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

收到微信服务器发送的推送请求之后，只要调用 ``cache_component_verify_ticket(self, msg, signature, timestamp, nonce)`` 即可恰当地缓存component_verify_ticket。


公众号 client 对象的获取
^^^^^^^^^^^^^^^^^^^^^^^^

强烈建议使用component对象获取公众号 client。

当需要代公众号调用接口时，有两种方法:

    - 将授权码传给 ``component.get_client_by_authorization_code()`` ，可以直接获取操作公众号 API 的对象。适用于刚刚获得授权的场景。
    - 将公众号 appid传入 ``component.get_client_by_appid()`` 。适用于已经授权的场景。

公众号的授权码和刷新码内部自动缓存。

操作公众号 API 的对象并非 :class:`~wechatpy.client.WeChatClient` ，但实现了同样的功能。在使用上相同:

.. code-block:: python
 
    client = component.get_client(appid, refresh_token, access_token)
    menu_info = client.menu.get()


公众号的授权码和刷新码的更新
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

授权码和刷新码有效期为7200秒，需要在失效之前更新授权码。由于各个项目的差异性和复杂性，本项目并未实现更新逻辑，需要调用者根据项目来自己实现。在失效之前，只要调用 `client.fetch_access_token()` 即可刷新缓存，所以这个逻辑很简单。


.. autoclass:: WeChatComponent
   :members:
   :inherited-members:
