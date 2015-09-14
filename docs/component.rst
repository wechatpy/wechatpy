代公众号调用接口
=================

本模块提供了开放平台代公众号调用接口 API。进行公众号第三方平台开发的项目，可以从这里开始。

.. module:: wechatpy.component


WeChatComponent
---------------

WeChatComponent的基本使用方法::

    from wechatpy import WeChatComponent
    component = WeChatComponent('app_id', 'app_secret', 'verify_ticket')

此后，可以调用component的其它方法完成公众号的授权、令牌刷新、获取或者设置公众号信息等操作。

当需要代公众号调用接口时，有两种方法:

    - 将授权码传给component.get_client_by()，可以直接获取操作公众号 API 的对象。适用于刚刚获得授权的场景。
    - 将公众号 appid、由 component 获得的access_token和refresh_token，传入`component.get_client()`。适用于已经授权的场景。

操作公众号 API 的对象并非:class:`~wechatpy.client.WeChatClient`，但实现了同样的功能。在使用上相同::
    
    client = component.get_client(appid, refresh_token, access_token)
    menu_info = client.menu.get()


.. autoclass:: WeChatComponent
   :members:
