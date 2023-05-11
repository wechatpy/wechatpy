# payscore

微信支付分 SDK，包含签名校验、加解密、平台证书自动更新等内容。完成了所有公共 API。

# 安装与升级

目前 [payscore](https://github.com/kangour/payscore) 支持的 Python 环境为 python3+，依赖于 [wechatpy](https://github.com/jxtech/wechatpy) 库。

安装 wechatpy

推荐使用 pip 进行 wechatpy 的安装

```
pip install wechatpy
# with cryptography （推荐）
pip install wechatpy[cryptography]
# with pycryptodome
pip install wechatpy[pycrypto]
```

升级 wechatpy 到新版本:

pip install -U wechatpy
如果需要安装 GitHub 上的最新代码:

pip install https://github.com/jxtech/wechatpy/archive/master.zip

安装 payscore

直接克隆 payscore 到项目即可，之后计划合并到 wechatpy。


# 使用演示

```
#  引入
from payscore import WeChatPayscore
#  实例
wechat_payscore = WeChatPayscore()
#  调用接口查询用户服务状态
result = wechat_payscore.payscore.user_service_state(openid=openid)
logger.info('用户的支付分服务状态: %s', result)
```


# 公共接口介绍

def user_service_state(self, openid) -> bool:
    """
    查询用户授权状态API
    https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_8.shtml
    """

def create(self, out_order_no, service_introduction, risk_fund, notify_url, time_range={"start_time": "OnAccept"}, openid=None, **kwargs) -> bool:
    """
    创建支付分订单API
    https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_1.shtml
    """

def query(self, out_order_no=None, query_id=None):
    """
    查询支付分订单API
    https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_2.shtml
    """

def complete(self, out_order_no, post_payments, total_amount, time_range=None, **kwargs):
    """
    完结支付分订单API
    https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_5.shtml
    """

def cancel(self, out_order_no, reason):
    """
    取消支付分订单API
    https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_3.shtml
    """

def modify(self, out_order_no, post_payments, total_amount, reason, **kwargs):
    """
    修改订单金额API
    https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_4.shtml
    """

def pay(self, out_order_no, **kwargs):
    """
    商户发起催收扣款API
    https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_6.shtml
    """

def sync(self, out_order_no, detail, _type='Order_Paid', **kwargs):
    """
    同步服务订单信息API
    https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/payscore/chapter3_7.shtml
    """

其他免确认预授权 API 请看 payscore/api/payafter.py 文件
