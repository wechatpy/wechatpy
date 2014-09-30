推送事件
=======

目前 wechatpy 支持一下几种事件推送类型：`SubscribeEvent`, `UnsubscribeEvent`, `SubscribeScanEvent`, `ScanEvent`, `LocationEvent`, `ClickEvent`, `ViewEvent`, `MassSendJobFinishEvent`, `TemplateSendJobFinishEvent`, `ScanCodePushEvent`, `ScanCodeWaitMsgEvent`, `PicSysPhotoEvent`, `PicPhotoOrAlbumEvent`, `PicWeChatEvent` 和 `LocationSelectEvent`。

事件本质上也是一种消息，故消息的公共属性在事件中也适用。

公共属性
-------

每一种事件都包括以下属性:

======= =================================
name    value
======= =================================
id      消息 id, 64 位整型。
source  消息的来源用户，即发送消息的用户。
target  消息的目标用户。
time    消息的发送时间，UNIX 时间戳
type    event
event   事件的类型
======= =================================