# -*- coding: utf-8 -*-


from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMisc(BaseWeChatAPI):
    def get_wechat_ips(self):
        """
        获取企业微信服务器的ip段

        https://work.weixin.qq.com/api/doc#90000/90135/90238/%E8%8E%B7%E5%8F%96%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%9A%84ip%E6%AE%B5

        :return: 企业微信回调的IP段
        """
        res = self._get("getcallbackip")
        return res["ip_list"]
