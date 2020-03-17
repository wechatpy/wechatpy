# -*- coding: utf-8 -*-
from enum import Enum, IntEnum, unique


@unique
class UserFormInfoFlag(Enum):
    """ 微信卡券会员卡格式化的选项类型 """

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
    """ 发票报销状态 """

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

    # 不合法的分组 ID
    INVALID_GROUP_ID = 40050

    # 不合法的分组名字
    INVALID_GROUP_NAME = 40051

    # 不支持的操作
    # 可能是该公众号已经申请完了十万个二维码
    INVALID_ACTION_INFO = 40053

    # 自定义菜单的按钮里，网址有误
    INVALID_BUTTON_DOMAIN = 40054

    # 自定义子菜单的按钮里，网址有误
    INVALID_SUB_BUTTON_DOMAIN = 40055

    # 错误的图文消息 ID
    INVALID_ARTICLE_ID = 40060

    # 错误的行业号
    # 有一些模板消息只会在特定的行业下申请
    INVALID_INDUSTRY_ID = 40102

    # 不支持的 MediaID 长度
    INVALID_MEDIA_ID_SIZE = 40118

    # 不支持的 MediaID 类型
    INVALID_MEDIA_ID_TYPE = 40121

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

    # 用户被拉黑
    # 需要公众号把该用户从黑名单里移除
    REQUIRE_UNBLOCK_USER = 43019

    # 超过了更换行业的限制
    # 一个月最多换一次
    OUT_OF_CHANGE_INDUSTRY_LIMIT = 43100

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

    # 回复时间超过限制
    # 接受推送后，5 秒内未被动响应。或者是用户与公众号 48 小时无互动后，调用客服接口主动推送消息。
    OUT_OF_RESPONSE_TIME_LIMIT = 45015

    # 模板消息数量超过限制
    OUT_OF_TEMPLATE_SIZE_LIMIT = 45026

    # 模板消息与行业信息冲突
    TEMPLATE_CONFLICT_WITH_INDUSTRY = 45027

    # 不支持的图文消息内容
    # 请确认 content 里没有超链接标签
    INVALID_CONTENT = 45166

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

    # 公众号未授权给开放平台
    UNAUTHORIZED_COMPONENT = 61003

    # 公众号未授权该 API 给开放平台
    UNAUTHORIZED_COMPONENT_API = 61007

    # 错误的开放平台 Refresh Token
    INVALID_COMPONENT_REFRESH_TOKEN = 61023
