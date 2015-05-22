Changelog
================

Version 0.8.6
-------------------

+ 修复了图文消息图文数量一直递增的问题
+ 从此版本开始不再支持 Python 3.2（cryptography 不支持，PyCrypto 应该还可以）
+ 从此版本开始 Travis CI 上增加了 Python nightly build（Python 3.5-dev） 的测试

Version 0.8.5
-------------------

+ WeChatOAuth 增加 qrconnect_url 属性
+ 被动响应消息增加 create_time 属性（通过解析 time 时间戳获得的 datetime.datetime 对象）
+ 增加了模板消息设置行业接口
+ 增加了模板消息获取模板 ID 接口

Version 0.8.4
--------------------

+ 修复了 WeChatOAuth 编码问题
+ 修复了企业号更新部门接口 parentid 参数错误问题
+ 企业号创建部门接口增加 order 和 id 可选参数

Version 0.8.3
--------------------

+ 群发消息接口增加 is_to_all 参数
+ 群发消息接口支持预览（增加 preview 参数）
+ 修复了群发消息的一个 bug
+ 素材管理接口增加获取素材数量 API

Version 0.8.2
---------------------

+ 修复 WeChatClient access_token 过期自动重试的一个 bug
+ 增加摇一摇周边接口
+ 增加设备功能接口

Version 0.8.1
---------------------

+ 增加获取菜单配置接口
+ 增加获取自动回复规则接口
+ 更新客服消息接口，支持使用特定客服账号发送消息
+ 修复 OAuth 验证接口错误

Version 0.8.0
---------------------

+ 消息加解密兼容 cryptography 和 PyCrypto 库
+ 企业号增加异步任务接口
+ 增加小视频消息类型

Version 0.7.6
---------------------

+ 增加 JSSDK 接口
+ 增加语义理解接口
+ 增加素材管理接口
+ 增加客服会话管理接口
+ 企业号增加 agent 管理接口
