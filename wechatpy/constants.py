# -*- coding: utf-8 -*-
from enum import Enum, IntEnum, unique


@unique
class UserFormInfoFlag(Enum):
    """微信卡券会员卡格式化的选项类型"""

    MOBILE = "USER_FORM_INFO_FLAG_MOBILE"  # 手机号
    SEX = "USER_FORM_INFO_FLAG_SEX"  # 性别
    NAME = "USER_FORM_INFO_FLAG_NAME"  # 姓名
    BIRTHDAY = "USER_FORM_INFO_FLAG_BIRTHDAY"  # 生日
    IDCARD = "USER_FORM_INFO_FLAG_IDCARD"  # 身份证
    EMAIL = "USER_FORM_INFO_FLAG_EMAIL"  # 邮箱
    LOCATION = "USER_FORM_INFO_FLAG_LOCATION"  # 详细地址
    EDUCATION_BACKGRO = "USER_FORM_INFO_FLAG_EDUCATION_BACKGRO"  # 教育背景
    INDUSTRY = "USER_FORM_INFO_FLAG_INDUSTRY"  # 行业
    INCOME = "USER_FORM_INFO_FLAG_INCOME"  # 收入
    HABIT = "USER_FORM_INFO_FLAG_HABIT"  # 兴趣爱好


@unique
class ReimburseStatus(Enum):
    """发票报销状态"""

    INIT = "INVOICE_REIMBURSE_INIT"  # 初始状态，未锁定，可提交报销
    LOCK = "INVOICE_REIMBURSE_LOCK"  # 已锁定，无法重复提交报销
    CLOSURE = "INVOICE_REIMBURSE_CLOSURE"  # 已核销，从用户卡包中移除


@unique
class WeChatErrorCode(IntEnum):
    """
    微信接口返回码，全局返回码请参考 https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Global_Return_Code.html
    """

    # 系统错误
    SYSTEM_ERROR = -1000

    # 系统繁忙
    # 此时请开发者稍候再试
    SYSTEM_BUSY = -1

    # 请求成功
    SUCCESS = 0

    # AppSecret 错误，或是 Access Token 无效
    # 请开发者认真比对AppSecret的正确性，或查看是否正在为恰当的公众号调用接口
    INVALID_CREDENTIAL = 40001

    # 错误的凭证类型
    INVALID_CREDENTIAL_TYPE = 40002

    # 错误的 OpenID
    # 请开发者确认 OpenID 是否已关注公众号，或是否是其他公众号的 OpenID
    INVALID_OPENID = 40003

    # 不支持的媒体文件类型
    INVALID_MEDIA_TYPE = 40004

    # 不支持的文件类型
    INVALID_FILE_TYPE = 40005

    # 不支持的文件大小
    INVALID_FILE_SIZE = 40006

    # 错误的 MediaID
    INVALID_MEDIA_ID = 40007

    # 错误的消息类型
    INVALID_MESSAGE_TYPE = 40008

    # 不支持的图片大小
    # 图片格式不对有时也会报这个错
    INVALID_IMAGE_SIZE = 40009

    # 不支持的语音文件大小
    INVALID_VOICE_SIZE = 40010

    # 不支持的视频文件大小
    INVALID_VIDEO_SIZE = 40011

    # 不支持的缩略图大小
    INVALID_THUMB_SIZE = 40012

    # 错误的 AppID
    # 目前 AppID 格式都是 /^wx\d{16}$/
    INVALID_APP_ID = 40013

    # 不合法的 Access Token
    # 请开发者认真比对 Access Token 的有效性（如是否过期），或查看是否正在为恰当的公众号调用接口
    INVALID_ACCESS_TOKEN = 40014

    # 错误的按钮类型
    INVALID_BUTTON_TYPE = 40015

    # 不支持的主菜单按钮个数
    # 微信自定义菜单按钮个数应该在 1~3 个之间
    INVALID_BUTTON_SIZE = 40016

    # 不支持的子菜单按钮个数
    # 微信自定义子菜单按钮个数应该在 1~5 个之间
    INVALID_SUB_BUTTON_SIZE = 40017

    # 不支持的按钮名字长度
    INVALID_BUTTON_NAME_SIZE = 40018

    # 不支持的按钮 key 长度
    INVALID_BUTTON_KEY_SIZE = 40019

    # 不支持的按钮 url 长度
    INVALID_BUTTON_URL_SIZE = 40020

    # 不合法的菜单版本号
    INVALID_MENU_VERSION = 40021

    # 不合法的子菜单级数
    INVALID_SUB_BUTTON_LEVEL = 40022

    # 不合法的子菜单按钮个数
    INVALID_SUB_BUTTON_COUNT = 40023

    # 不合法的子菜单按钮类型
    INVALID_SUB_BUTTON_TYPE = 40024

    # 不合法的子菜单按钮名字长度
    INVALID_SUB_BUTTON_NAME_SIZE = 40025

    # 不合法的子菜单按钮 key 长度
    INVALID_SUB_BUTTON_KEY_SIZE = 40026

    # 不合法的子菜单按钮 url 长度
    INVALID_SUB_BUTTON_URL_SIZE = 40027

    # 不合法的自定义菜单使用用户
    INVALID_MENU_USER = 40028

    # 错误的 OAuth Code
    INVALID_OAUTH_CODE = 40029

    # 错误的 Refresh Token
    INVALID_REFRESH_TOKEN = 40030

    # 错误的 OpenID 列表
    INVALID_OPENID_LIST = 40031

    # 错误的 OpenID 列表长度
    # 列表内最多10000个 OpenID
    INVALID_OPENID_LIST_SIZE = 40032

    # 不支持的请求字符
    # 不能包含 \uxxxx 格式的字符
    INVALID_REQUEST_CHARSET = 40033

    # 不合法的参数
    INVALID_PARAMETER = 40035

    # 错误的模板消息 ID
    # Template ID 失效了，请重新刷新一次 Template ID
    INVALID_TEMPLATE = 40037

    # 不合法的请求格式
    INVALID_REQUEST_FORMAT = 40038

    # 不合法的 url 长度
    INVALID_URL_SIZE = 40039

    # 无效的 url
    INVALID_URL_DOMAIN = 40048

    # 不合法的分组 ID
    INVALID_GROUP_ID = 40050

    # 不合法的分组名字
    # 40117 也是这个错误
    INVALID_GROUP_NAME = 40051

    # 不支持的操作
    # 可能是该公众号已经申请完了十万个二维码
    INVALID_ACTION_INFO = 40053

    # 自定义菜单的按钮里，网址有误
    INVALID_BUTTON_DOMAIN = 40054

    # 自定义子菜单的按钮里，网址有误
    INVALID_SUB_BUTTON_DOMAIN = 40055

    # 删除单篇图文时，指定的 article_idx 不合法
    INVALID_DELETE_ARTICLE_ID = 40060

    # 错误的行业号
    # 有一些模板消息只会在特定的行业下申请
    INVALID_INDUSTRY_ID = 40102

    # 不支持的 MediaID 长度
    INVALID_MEDIA_ID_SIZE = 40118

    # button 类型错误
    INVALID_USE_BUTTON_TYPE = 40119

    # 子 button 类型错误
    INVALID_USE_SUB_BUTTON_TYPE = 40120

    # 不支持的 MediaID 类型
    INVALID_MEDIA_ID_TYPE = 40121

    # 无效的 AppSecret
    INVALID_APP_SECRET = 40125

    # 微信号不合法
    INVALID_WECHAT_ID = 40132

    # 不支持的图片格式
    INVALID_IMAGE_FORMAT = 40137

    # 请勿添加其他公众号的主页链接
    CONTAIN_OTHER_HOME_PAGE_URL = 40155

    # OAuth Code 已使用
    CODE_BEEN_USED = 40163

    # 缺少 Access Token 参数
    MISSING_ACCESS_TOKEN = 41001

    # 缺少 AppID 参数
    MISSING_APP_ID = 41002

    # 缺少 Refresh Token 参数
    MISSING_REFRESH_TOKEN = 41003

    # 缺少 AppSecret 参数
    MISSING_APP_SECRET = 41004

    # 缺少多媒体文件数据
    MISSING_MEDIA_DATA = 41005

    # 缺少 MediaID 参数
    MISSING_MEDIA_ID = 41006

    # 缺少子菜单数据
    MISSING_SUB_BUTTONS = 41007

    # 缺少 OAuth Code
    MISSING_OAUTH_CODE = 41008

    # 缺少 OpenID
    MISSING_OPENID = 41009

    # page 路径不正确，需要保证在现网版本小程序中存在，与 app.json 保持一致
    INVALID_PAGE = 41030

    # Access Token 已失效
    # 请检查 Access Token 的有效期，重新刷新 Access Token
    EXPIRED_ACCESS_TOKEN = 42001

    # Refresh Token 已失效
    EXPIRED_REFRESH_TOKEN = 42002

    # OAuth Code 已失效
    EXPIRED_OAUTH_CODE = 42003

    # 授权已失效
    # 用户修改微信密码，Access Token, Refresh Token 均已失效，需要重新授权
    EXPIRED_AUTHORIZATION = 42007

    # 需要 Get 请求
    REQUIRE_GET = 43001

    # 需要 Post 请求
    REQUIRE_POST = 43002

    # 需要 Https 请求
    REQUIRE_HTTPS = 43003

    # 用户没有关注公众号
    REQUIRE_SUBSCRIBE = 43004

    # 需要好友关系
    REQUIRE_FRIEND = 43005

    # 用户被拉黑
    # 需要公众号把该用户从黑名单里移除
    REQUIRE_UNBLOCK_USER = 43019

    # 超过了更换行业的限制
    # 一个月最多换一次
    OUT_OF_CHANGE_INDUSTRY_LIMIT = 43100

    # 用户拒绝接受消息，如果用户之前曾经订阅过，则表示用户取消了订阅关系
    USER_REFUSE_TO_ACCEPT_THE_MESSAGE = 43101

    # 多媒体文件为空
    EMPTY_MEDIA_DATA = 44001

    # POST 的数据包为空
    EMPTY_POST_DATA = 44002

    # 图文消息内容为空
    EMPTY_NEWS_DATA = 44003

    # 文本消息内容为空
    EMPTY_CONTENT = 44004

    # 多媒体文件大小超过限制
    # 最大允许 1MB
    OUT_OF_MEDIA_SIZE_LIMIT = 45001

    # 消息内容超过限制
    OUT_OF_CONTENT_SIZE_LIMIT = 45002

    # 标题长度超过限制
    # 最长允许 64 字符长度
    OUT_OF_TITLE_SIZE_LIMIT = 45003

    # 描述字段超过限制
    OUT_OF_DESCRIPTION_SIZE_LIMIT = 45004

    # 链接字段超过限制
    OUT_OF_URL_SIZE_LIMIT = 45005

    # 图片链接字段超过限制
    OUT_OF_PIC_URL_SIZE_LIMIT = 45006

    # 语音播放时间超过限制
    # 最长允许 60 秒
    OUT_OF_VOICE_TIME_LIMIT = 45007

    # 图文消息数量超过限制
    # 最多 10 条图文消息
    OUT_OF_ARTICLE_SIZE_LIMIT = 45008

    # 接口调用频率超过限制
    OUT_OF_API_FREQ_LIMIT = 45009

    # 创建菜单个数超过限制
    OUT_OF_MENU_SIZE_LIMIT = 45010

    # API 调用太频繁，请稍候再试
    API_MINUTE_QUOTA_REACH_LIMIT = 45011

    # 回复时间超过限制
    # 接受推送后，5 秒内未被动响应。或者是用户与公众号 48 小时无互动后，调用客服接口主动推送消息。
    OUT_OF_RESPONSE_TIME_LIMIT = 45015

    # 系统分组，不允许修改
    SYSTEM_GROUP_CANNOT_CHANGE = 45016

    # 分组名字过长
    OUT_OF_GROUP_NAME_SIZE_LIMIT = 45017

    # 分组数量超过上限
    OUT_OF_GROUP_SIZE_LIMIT = 45018

    # 模板消息数量超过限制
    OUT_OF_TEMPLATE_SIZE_LIMIT = 45026

    # 模板消息与行业信息冲突
    TEMPLATE_CONFLICT_WITH_INDUSTRY = 45027

    # 客服接口下行条数超过上限
    OUT_OF_RESPONSE_COUNT_LIMIT = 45047

    # 创建菜单包含未关联的小程序
    NO_PERMISSION_TO_USE_WEAPP_IN_MENU = 45064

    # 相同 clientmsgid 已存在群发记录，返回数据中带有已存在的群发任务的 msgid
    CLIENTMSGID_EXIST = 45065

    #  相同 clientmsgid 重试速度过快，请间隔1分钟重试
    OUT_OF_CLIENTMSGID_API_FREQ_LIMIT = 45066

    # clientmsgid 长度超过限制
    CLIENTMSGID_SIZE_OUT_OF_LIMIT = 45067

    # 不支持的图文消息内容
    # 请确认 content 里没有超链接标签
    INVALID_CONTENT = 45166

    # 不存在媒体数据
    MEDIA_DATA_NO_EXIST = 46001

    # 不存在的菜单版本
    MENU_VERSION_NOT_EXIST = 46002

    # 不存在的菜单数据
    MENU_NO_EXIST = 46003

    # 不存在的用户
    USER_NOT_EXIST = 46004

    # 解析 JSON/XML 内容错误
    DATA_FORMAT_ERROR = 47001

    # 模板参数不准确，可能为空或者不满足规则，errmsg 会提示具体是哪个字段出错
    INVALID_TEMPLATE_ARGUMENT = 47003

    # API 功能未授权
    # 请确认公众号已获得该接口，可以在公众平台官网-开发者中心页中查看接口权限
    UNAUTHORIZED_API = 48001

    # 用户拒收公众号消息
    # (在公众号选项中，关闭了“接收消息”)
    USER_BLOCK_MESSAGE = 48002

    # 公众号管理员没有同意微信群发协议
    # 请登录公众号后台点一下同意
    USER_NOT_AGREE_PROTOCOL = 48003

    # API 接口被封禁
    # 请登录公众号后台查看详情
    API_BANNED = 48004

    # API 禁止删除被自动回复和自定义菜单引用的素材
    API_DELETE_PROHIBITED = 48005

    # API 清零次数失败，因为清零次数达到上限
    OUT_OF_RESET_LIMIT = 48006

    # 没有该类型消息的发送权限
    NO_PERMISSION_FOR_THIS_MSGTYPE = 48008

    # 用户未授权该 API
    USER_UNAUTHORIZED = 50001

    # 用户受限，可能是违规后接口被封禁
    USER_LIMITED = 50002

    # 用户未关注的公众号
    UNSUBSCRIBE_OFFICIAL_ACCOUNT = 50005

    # 发布功能被封禁
    PUBLISH_LIMITED = 53500

    # 频繁请求发布
    OUT_OF_PUBLISH_LIMIT = 53501

    # Publish ID 无效
    INVALID_PUBLISH_ID = 53502

    # Article ID 无效
    INVALID_ARTICLE_ID = 53600

    # 公众号未授权给开放平台
    UNAUTHORIZED_COMPONENT = 61003

    # 公众号未授权该 API 给开放平台
    UNAUTHORIZED_COMPONENT_API = 61007

    # 错误的开放平台 Refresh Token
    INVALID_COMPONENT_REFRESH_TOKEN = 61023

    # 参数错误
    ERROR_PARAMETER = 61451

    # 无效客服账号
    INVALID_KF_ACCOUNT = 61452

    # 客服帐号已存在
    KF_ACCOUNT_EXISTED = 61453

    # 客服帐号名长度超过限制 ( 仅允许 10 个英文字符，不包括 @ 及 @ 后的公众号的微信号 )
    INVALID_KF_ACCOUNT_LENGTH = 61454

    # 客服帐号名包含非法字符 ( 仅允许英文 + 数字 )
    ILLEGAL_CHARTER_IN_KF_ACCOUNT = 61455

    # 客服帐号个数超过限制 (10 个客服账号 )
    KF_ACCOUNT_EXCEEDED = 61456

    # 无效头像文件类型
    INVALID_AVATAR_FILE_TYPE = 61457

    # 日期格式错误
    DATE_FORMAT_ERROR = 61500

    # 部分参数为空
    MISSING_PARAMETER = 63001

    # 无效的 JS SDK 签名
    INVALID_JS_SDK_SIGNATURE = 63002

    # 不存在此 menuid 对应的个性化菜单
    INVALID_MENU_ID = 65301

    # 没有默认菜单，不能创建个性化菜单
    THERE_IS_NO_SELFMENU = 65303

    # MatchRule 信息为空
    MATCH_RULE_EMPTY = 65304

    # 个性化菜单数量受限
    MENU_COUNT_LIMIT = 65305

    # 不支持个性化菜单的帐号
    INVALID_ACCOUNT_FOR_MENU = 65306

    # 个性化菜单信息为空
    EMPTY_MENU = 65307

    # 包含没有响应类型的 button
    BUTTON_MISSING_RESPONSE = 65308

    # 个性化菜单开关处于关闭状态
    DISABLE_MENU = 65309

    # 填写了省份或城市信息，国家信息不能为空
    MISSING_COUNTRY = 65310

    # 填写了城市信息，省份信息不能为空
    MISSING_PROVINCE = 65311

    # 不合法的国家信息
    INVALID_COUNTRY = 65312

    # 不合法的省份信息
    INVALID_PROVINCE = 65313

    # 不合法的城市信息
    INVALID_CITY_INFO = 65314

    # 该公众号的菜单设置了过多的域名外跳（最多跳转到 3 个域名的链接）
    DOMAIN_COUNT_REACH_LIMIT = 65316

    # 不合法的 URL
    INVALID_URL = 65317

    # 无效的签名
    INVALID_SIGNATURE = 87009

    # 内容可能潜在风险
    RISKY_CONTENT = 87014

    # POST 数据参数不合法
    INVALID_POST_DATA = 9001001

    # 远端服务不可用
    REMOTE_SERVICE_UNAVAILABLE = 9001002

    # Ticket 不合法
    INVALID_TICKET = 9001003

    # 获取摇周边用户信息失败
    GET_USER_FAILED = 9001004

    # 获取商户信息失败
    GET_MERCHANT_FAILED = 9001005

    # 获取 OpenID 失败
    GET_OPENID_FAILED = 9001006

    # 上传文件缺失
    UPLOAD_FILE_MISSING = 9001007

    # 上传素材的文件类型不合法
    UPLOAD_FILE_TYPE_ERROR = 9001008

    # 上传素材的文件尺寸不合法
    UPLOAD_FILE_SIZE_ERROR = 9001009

    # 上传失败
    UPLOAD_FAILED = 9001010

    # 帐号不合法
    INVALID_ACCOUNT = 9001020

    # 已有设备激活率低于 50% ，不能新增设备
    ACTIVE_DEVICE_LESS_THAN_HALF = 9001021

    # 设备申请数不合法，必须为大于 0 的数字
    INVALID_DEVICE_COUNT = 9001022

    # 已存在审核中的设备 ID 申请
    DEVICE_ID_EXISTED = 9001023

    # 一次查询设备 ID 数量不能超过 50
    OUT_OF_DEVICE_QUERY_LIMIT = 9001024

    # 设备 ID 不合法
    INVALID_DEVICE_ID = 9001025

    # 页面 ID 不合法
    INVALID_PAGE_ID = 9001026

    # 页面参数不合法
    INVALID_PAGE_PARAMETER = 9001027

    # 一次删除页面 ID 数量不能超过 10
    OUT_OF_PAGE_DELETE_LIMIT = 9001028

    # 页面已应用在设备中，请先解除应用关系再删除
    PAGE_APPLIED_IN_DEVICE = 9001029

    # 一次查询页面 ID 数量不能超过 50
    OUT_OF_PAGE_QUERY_LIMIT = 9001030

    # 时间区间不合法
    INVALID_TIME_RANGE = 9001031

    # 保存设备与页面的绑定关系参数错误
    BIND_DEVICE_PAGE_PARAMETER_ERROR = 9001032

    # 门店 ID 不合法
    INVALID_LOCATION_ID = 9001033

    # 设备备注信息过长
    OUT_OF_DEVICE_DESC_LENGTH_LIMIT = 9001034

    # 设备申请参数不合法
    INVALID_DEVICE_PARAMETER = 9001035

    # 查询起始值 begin 不合法
    INVALID_BEGIN = 9001036
