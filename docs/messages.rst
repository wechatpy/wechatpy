.. _messages:

推送消息
==========

公共属性
--------

每一种消息都包括以下属性:

=========== =================================
name        value
=========== =================================
id          消息 id, 64 位整型。
source      消息的来源用户，即发送消息的用户。
target      消息的目标用户。
create_time 消息的发送时间，UNIX 时间戳
type        消息的类型
=========== =================================

.. module:: wechatpy.messages

文本消息
--------------------

.. autoclass:: TextMessage
   :members:
   :inherited-members:

TextMessage 的属性:

======= =================================
name    value
======= =================================
type    text
content 消息的内容
======= =================================

图片消息
---------------------
.. autoclass:: ImageMessage
   :members:
   :inherited-members:

ImageMessage 的属性:

======= =================================
name    value
======= =================================
type    image
image   图片的 URL 地址
======= =================================

语音消息
---------------------

.. autoclass:: VoiceMessage
   :members:
   :inherited-members:

VoiceMessage 的属性:

============ ===================================
name         value
============ ===================================
type         voice
media_id     微信内部的一个文件 ID
format       声音文件格式
recognition  语音识别结果(启用了语音识别时才有)
============ ===================================

视频消息
---------------------

.. autoclass:: VideoMessage
   :members:
   :inherited-members:

VideoMessage 的属性:

================= =================================
name              value
================= =================================
type              video
media_id          微信内部的一个文件 ID
thumb_media_id    视频缩略图文件 ID
================= =================================

地理位置消息
----------------------------

.. autoclass:: LocationMessage
   :members:
   :inherited-members:

LocationMessage 的属性:

============ =================================
name         value
============ =================================
type         location
location_x   地理位置纬度
location_y   地理位置经度
scale        地图缩放大小
label        地理位置信息
location     (纬度, 经度) 元组
============ =================================

链接消息
--------------------

.. autoclass:: LinkMessage
   :members:
   :inherited-members:

LinkMessage 的属性:

============ =================================
name         value
============ =================================
type         link
title        链接标题
description  链接描述
url          链接地址
============ =================================

短视频消息
----------------------------
.. autoclass:: ShortVideoMessage
   :members:
   :inherited-members:

=============== =================================
name            value
=============== =================================
type            shortvideo
media_id        短视频 media_id
thumb_media_id  短视频缩略图 media_id
=============== =================================

解析消息
-------------

wechatpy 提供了一个便捷的函数 ``parse_message`` 来处理由微信服务器发送过来的 XML 消息并解析生成对应的消息类:

.. code-block:: python

    from wechatpy import parse_message

    xml = 'some xml'
    msg = parse_message(xml)
    print(msg.type)
