.. wechatpy documentation master file, created by
   sphinx-quickstart on Thu Sep 25 14:26:14 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

wechatpy 使用文档
====================================

wechatpy 是一个微信 (WeChat) 公众平台的第三方 Python SDK, 实现了普通公众平台和企业号公众平台的解析消息、生成回复和主动调用等 API。

快速入门
-------------

.. toctree::
   :maxdepth: 2

   install
   quickstart

微信公众平台接口
-------------------

.. toctree::
   :maxdepth: 2

   messages
   events
   replies
   client
   pay
   oauth

微信企业号平台接口
---------------------

.. toctree::
   :maxdepth: 2
   :glob:

   enterprise/quickstart
   enterprise/client


微信公众号第三方平台接口
-----------------------------

.. toctree::
   :maxdepth: 2

   component


示例项目/扩展程序
---------------------

1. `django restful demo <https://github.com/wechatpy/django-wechat-example/>`_
2. `WeCron 基于微信的定时提醒 <https://github.com/polyrabbit/WeCron>`_
3. `flask-wechatpy <https://github.com/cloverstd/flask-wechatpy>`_ Flask 扩展


Changelogs
---------------

.. toctree::
   :maxdepth: 2

   changelog
