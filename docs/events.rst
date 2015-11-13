推送事件
==========

目前 wechatpy 支持一下几种事件推送类型：`SubscribeEvent`, `UnsubscribeEvent`, `SubscribeScanEvent`, `ScanEvent`, `LocationEvent`, `ClickEvent`, `ViewEvent`, `MassSendJobFinishEvent`, `TemplateSendJobFinishEvent`, `ScanCodePushEvent`, `ScanCodeWaitMsgEvent`, `PicSysPhotoEvent`, `PicPhotoOrAlbumEvent`, `PicWeChatEvent` 和 `LocationSelectEvent`。

事件本质上也是一种消息，故消息的公共属性在事件中也适用。

公共属性
----------

每一种事件都包括以下属性:

======= =================================
name    value
======= =================================
id      事件 id, 64 位整型。
source  事件的来源用户，即发送消息的用户。
target  事件的目标用户。
time    事件的发送时间，UNIX 时间戳
type    event
event   事件的类型
======= =================================

.. module:: wechatpy.events

SubscribeEvent 关注事件
-----------------------------

.. autoclass:: SubscribeEvent
   :members:

SubscribeEvent 的属性:

======= =================================
name    value
======= =================================
event   subscribe
======= =================================

UnsubscribeEvent 取消关注事件
-----------------------------------

.. autoclass:: UnsubscribeEvent
   :members:

UnsubscribeEvent 的属性:

======= =================================
name    value
======= =================================
event   unsubscribe
======= =================================

SubscribeScanEvent 未关注用户扫描带参数二维码事件
--------------------------------------------------

.. autoclass:: SubscribeScanEvent
   :members:


SubscribeScanEvent 的属性:

========= ========================================
name      value
========= ========================================
event     subscribe_scan
scene_id  带参数二维码 scene_id，去除了前缀 `qrscene_`
ticket    带参数二维码 ticket
========= ========================================

ScanEvent 已关注用户扫描带参数二维码事件
--------------------------------------------

.. autoclass:: ScanEvent
   :members:

ScanEvent 的属性:

========= =================================
name      value
========= =================================
event     scan
scene_id  带参数二维码 scene_id
ticket    带参数二维码 ticket
========= =================================

LocationEvent 上报地理位置事件
----------------------------------

.. autoclass:: LocationEvent
   :members:


LocationEvent 的属性:

=========== =================================
name        value
=========== =================================
event       location
latitude    地理位置纬度
longitude   地理位置经度
precision   地理位置精度
=========== =================================

ClickEvent 点击菜单拉取消息事件
----------------------------------

.. autoclass:: ClickEvent
   :members:

ClickEvent 的属性:

======= =================================
name    value
======= =================================
event   click
key     自定义菜单 key 值
======= =================================

ViewEvent 点击菜单跳转链接事件
----------------------------------

.. autoclass:: ViewEvent
   :members:

ViewEvent 的属性:

======= =================================
name    value
======= =================================
event   view
url     跳转链接 url
======= =================================

MassSendJobFinishEvent 群发消息发送任务完成事件
-------------------------------------------------

.. autoclass:: MassSendJobFinishEvent
   :members:

MassSendJobFinishEvent 的属性:

============= =================================
name          value
============= =================================
event         masssendjobfinish
status        群发任务状态
total_count   发送的总粉丝数
filter_count  过滤后准备发送的粉丝数
sent_count    发送成功的粉丝数
error_count   发送失败的粉丝数
============= =================================

TemplateSendJobFinishEvent 模板消息发送任务完成事件
------------------------------------------------------

.. autoclass:: TemplateSendJobFinishEvent
   :members:

TemplateSendJobFinishEvent 的属性:

======= =================================
name    value
======= =================================
event   templatesendjobfinish
status  模板消息发送状态
======= =================================

ScanCodePushEvent 扫码推事件
--------------------------------

.. autoclass:: ScanCodePushEvent
   :members:

ScanCodePushEvent 的属性:

=========== =================================
name        value
=========== =================================
event       scancode_push
key         自定义菜单 key
scan_type   扫描类型
scan_result 扫描结果
=========== =================================

ScanCodeWaitMsgEvent 扫码推事件且弹出“消息接收中”提示框
-------------------------------------------------------

.. autoclass:: ScanCodeWaitMsgEvent
   :members:

ScanCodeWaitMsgEvent 的属性:

=========== =================================
name        value
=========== =================================
event       scancode_waitmsg
key         自定义菜单 key
scan_type   扫描类型
scan_result 扫描结果
=========== =================================

PicSysPhotoEvent 弹出系统拍照发图事件
-----------------------------------------

.. autoclass:: PicSysPhotoEvent
   :members:

PicSysPhotoEvent 的属性:

=========== =================================
name        value
=========== =================================
event       pic_sysphoto
key         自定义菜单 key
count       发送的图片数量
pictures    图片列表
=========== =================================

PicPhotoOrAlbumEvent 弹出拍照或者相册发图事件
------------------------------------------------

.. autoclass:: PicPhotoOrAlbumEvent
   :members:

PicPhotoOrAlbumEvent 的属性:

=========== =================================
name        value
=========== =================================
event       pic_photo_or_album
key         自定义菜单 key
count       发送的图片数量
pictures    图片列表
=========== =================================

PicWeChatEvent 弹出微信相册发图器事件
---------------------------------------

.. autoclass:: PicWeChatEvent
   :members:

PicWeChatEvent 的属性:

=========== =================================
name        value
=========== =================================
event       pic_weixin
key         自定义菜单 key
count       发送的图片数量
pictures    图片列表
=========== =================================

LocationSelectEvent 弹出地理位置选择器事件
--------------------------------------------

.. autoclass:: LocationSelectEvent
   :members:

LocationSelectEvent 的属性:

=========== =================================
name        value
=========== =================================
event       location_select
key         自定义菜单 key
location_x  地理位置纬度
location_y  地理位置经度
location    地理位置元组: (纬度, 经度)
scale       地理位置精度
label       地理位置信息字符串
poiname     朋友圈 POI 的名字，可能为空
=========== =================================


微信认证事件推送
----------------

QualificationVerifySuccessEvent 资质认证成功事件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: QualificationVerifySuccessEvent
   :members:

QualificationVerifySuccessEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        qualification_verify_success
expired_time 有效期 (整形)，指的是时间戳，将于该时间戳认证过期
============ ============================================

QualificationVerifyFailEvent 资质认证失败事件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: QualificationVerifyFailEvent
   :members:

QualificationVerifyFailEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        qualification_verify_fail
fail_time    失败发生时间 (整形)，时间戳
fail_reason  认证失败的原因
============ ============================================

NamingVerifySuccessEvent 名称认证成功
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: NamingVerifySuccessEvent
   :members:

NamingVerifySuccessEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        naming_verify_success
expired_time 有效期 (整形)，指的是时间戳，将于该时间戳认证过期
============ ============================================

NamingVerifyFailEvent 名称认证失败
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: NamingVerifyFailEvent
   :members:

NamingVerifyFailEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        naming_verify_fail
fail_time    失败发生时间 (整形)，时间戳
fail_reason  认证失败的原因
============ ============================================

AnnualRenewEvent 年审通知
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: AnnualRenewEvent
   :members:

AnnualRenewEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        annual_renew
expired_time 有效期 (整形)，指的是时间戳，将于该时间戳认证过期，需尽快年审
============ ============================================

VerifyExpiredEvent 认证过期失效通知
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: VerifyExpiredEvent
   :members:

VerifyExpiredEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        verify_expired
expired_time 有效期 (整形)，指的是时间戳，表示已于该时间戳认证过期，需要重新发起微信认证
============ ============================================
