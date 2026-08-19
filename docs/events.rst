.. _events:

推送事件
==========

事件本质上也是一种消息，故消息的公共属性在事件中也适用。

公共属性
----------

每一种事件都包括以下属性:

=========== =================================
name        value
=========== =================================
id          事件 id, 64 位整型。
source      事件的来源用户，即发送消息的用户。
target      事件的目标用户。
create_time 事件的发送时间，UNIX 时间戳
type        event
event       事件的类型
=========== =================================

.. module:: wechatpy.events

关注事件
-----------------------------

.. autoclass:: SubscribeEvent
   :members:
   :inherited-members:

SubscribeEvent 的属性:

======= =================================
name    value
======= =================================
event   subscribe
======= =================================

取消关注事件
-----------------------------------

.. autoclass:: UnsubscribeEvent
   :members:
   :inherited-members:

UnsubscribeEvent 的属性:

======= =================================
name    value
======= =================================
event   unsubscribe
======= =================================

未关注用户扫描带参数二维码事件
--------------------------------------------------

.. autoclass:: SubscribeScanEvent
   :members:
   :inherited-members:


SubscribeScanEvent 的属性:

========= ========================================
name      value
========= ========================================
event     subscribe_scan
scene_id  带参数二维码 scene_id，去除了前缀 `qrscene_`
ticket    带参数二维码 ticket
========= ========================================

已关注用户扫描带参数二维码事件
--------------------------------------------

.. autoclass:: ScanEvent
   :members:
   :inherited-members:

ScanEvent 的属性:

========= =================================
name      value
========= =================================
event     scan
scene_id  带参数二维码 scene_id
ticket    带参数二维码 ticket
========= =================================

上报地理位置事件
----------------------------------

.. autoclass:: LocationEvent
   :members:
   :inherited-members:


LocationEvent 的属性:

=========== =================================
name        value
=========== =================================
event       location
latitude    地理位置纬度
longitude   地理位置经度
precision   地理位置精度
=========== =================================

点击菜单拉取消息事件
----------------------------------

.. autoclass:: ClickEvent
   :members:
   :inherited-members:

ClickEvent 的属性:

======= =================================
name    value
======= =================================
event   click
key     自定义菜单 key 值
======= =================================

点击菜单跳转链接事件
----------------------------------

.. autoclass:: ViewEvent
   :members:
   :inherited-members:

ViewEvent 的属性:

======= =================================
name    value
======= =================================
event   view
url     跳转链接 url
======= =================================

群发消息发送任务完成事件
-------------------------------------------------

.. autoclass:: MassSendJobFinishEvent
   :members:
   :inherited-members:

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

模板消息发送任务完成事件
------------------------------------------------------

.. autoclass:: TemplateSendJobFinishEvent
   :members:
   :inherited-members:

TemplateSendJobFinishEvent 的属性:

======= =================================
name    value
======= =================================
event   templatesendjobfinish
status  模板消息发送状态
======= =================================

扫码推事件
--------------------------------

.. autoclass:: ScanCodePushEvent
   :members:
   :inherited-members:

ScanCodePushEvent 的属性:

=========== =================================
name        value
=========== =================================
event       scancode_push
key         自定义菜单 key
scan_type   扫描类型
scan_result 扫描结果
=========== =================================

扫码推事件且弹出“消息接收中”提示框
-------------------------------------------------------

.. autoclass:: ScanCodeWaitMsgEvent
   :members:
   :inherited-members:

ScanCodeWaitMsgEvent 的属性:

=========== =================================
name        value
=========== =================================
event       scancode_waitmsg
key         自定义菜单 key
scan_type   扫描类型
scan_result 扫描结果
=========== =================================

弹出系统拍照发图事件
-----------------------------------------

.. autoclass:: PicSysPhotoEvent
   :members:
   :inherited-members:

PicSysPhotoEvent 的属性:

=========== =================================
name        value
=========== =================================
event       pic_sysphoto
key         自定义菜单 key
count       发送的图片数量
pictures    图片列表
=========== =================================

弹出拍照或者相册发图事件
------------------------------------------------

.. autoclass:: PicPhotoOrAlbumEvent
   :members:
   :inherited-members:

PicPhotoOrAlbumEvent 的属性:

=========== =================================
name        value
=========== =================================
event       pic_photo_or_album
key         自定义菜单 key
count       发送的图片数量
pictures    图片列表
=========== =================================

弹出微信相册发图器事件
---------------------------------------

.. autoclass:: PicWeChatEvent
   :members:
   :inherited-members:

PicWeChatEvent 的属性:

=========== =================================
name        value
=========== =================================
event       pic_weixin
key         自定义菜单 key
count       发送的图片数量
pictures    图片列表
=========== =================================

弹出地理位置选择器事件
--------------------------------------------

.. autoclass:: LocationSelectEvent
   :members:
   :inherited-members:

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

资质认证成功事件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: QualificationVerifySuccessEvent
   :members:
   :inherited-members:

QualificationVerifySuccessEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        qualification_verify_success
expired_time 有效期，将于该时间戳认证过期
============ ============================================

资质认证失败事件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: QualificationVerifyFailEvent
   :members:
   :inherited-members:

QualificationVerifyFailEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        qualification_verify_fail
fail_time    失败发生时间
fail_reason  认证失败的原因
============ ============================================

名称认证成功
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: NamingVerifySuccessEvent
   :members:
   :inherited-members:

NamingVerifySuccessEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        naming_verify_success
expired_time 有效期，将于该时间戳认证过期
============ ============================================

名称认证失败
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: NamingVerifyFailEvent
   :members:
   :inherited-members:

NamingVerifyFailEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        naming_verify_fail
fail_time    失败发生时间
fail_reason  认证失败的原因
============ ============================================

年审通知
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: AnnualRenewEvent
   :members:
   :inherited-members:

AnnualRenewEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        annual_renew
expired_time 有效期，将于该时间戳认证过期，需尽快年审
============ ============================================

认证过期失效通知
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: VerifyExpiredEvent
   :members:
   :inherited-members:

VerifyExpiredEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        verify_expired
expired_time 有效期，表示已于该时间戳认证过期，需要重新发起微信认证
============ ============================================

微信扫一扫事件
--------------------

打开商品主页事件
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserScanProductEvent
   :members:
   :inherited-members:

UserScanProductEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        user_scan_product
standard     商品编码标准
key          商品编码内容
country      用户在微信内设置的国家
province     用户在微信内设置的省份
city         用户在微信内设置的城市
sex          用户的性别，1为男性，2为女性，0代表未知
scene        打开商品主页的场景，1为扫码，2为其他打开场景（如会话、收藏或朋友圈）
============ ============================================

进入公众号事件
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserScanProductEnterSessionEvent
   :members:
   :inherited-members:

UserScanProductEnterSessionEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        user_scan_product_enter_session
standard     商品编码标准
key          商品编码内容
============ ============================================

地理位置信息异步推送事件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserScanProductAsyncEvent
   :members:
   :inherited-members:

UserScanProductAsyncEvent 的属性:

============ ============================================
参数          值
============ ============================================
event        user_scan_product_async
standard     商品编码标准
key          商品编码内容
region_code  用户的实时地理位置信息
============ ============================================

商品审核结果事件
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserScanProductVerifyActionEvent
   :members:
   :inherited-members:

============ ============================================
参数          值
============ ============================================
event        user_scan_product_async
standard     商品编码标准
key          商品编码内容
result       审核结果。verify_ok 表示审核通过，verify_not_pass 表示审核未通过
reason       审核未通过的原因
============ ============================================

当用户在商品主页中关注公众号事件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: SubscribeScanProductEvent
   :members:
   :inherited-members:

============ ============================================
参数          值
============ ============================================
event        subscribe_scan_product
scene        scanbarcode 为扫码场景，scanimage 为扫封面（图像）场景
standard     商品编码标准
key          商品编码内容
============ ============================================

用户授权发票事件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UserAuthorizeInvoiceEvent
   :members:
   :inherited-members:

================ ============================================
参数              值
================ ============================================
event            user_authorize_invoice
success_order_id 授权成功的订单号
fail_order_id    授权失败的订单号
app_id           用于接收事件推送的公众号的AppId
auth_source      授权来源，web表示来自微信内H5，app标识来自app
================ ============================================

发票状态更新事件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UpdateInvoiceStatusEvent
   :members:
   :inherited-members:

=========== ============================================
参数         值
=========== ============================================
event       update_invoice_status
status      发票报销状态
card_id     发票卡券 Card ID
code        发票卡券 Code
=========== ============================================

用户提交发票抬头事件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: SubmitInvoiceTitleEvent
   :members:
   :inherited-members:

=========== ============================================
参数         值
=========== ============================================
event       submit_invoice_title
title       抬头
phone       联系方式
tax_no      税号
addr        地址
bank_type   银行类型
bank_no     银行号码
attach      附加字段
title_type  抬头类型，InvoiceUserTitlePersonType为个人抬头，InvoiceUserTitleBusinessType为公司抬头
=========== ============================================

