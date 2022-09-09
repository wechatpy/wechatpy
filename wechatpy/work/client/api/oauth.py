# -*- coding: utf-8 -*-

from urllib.parse import quote

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatOAuth(BaseWeChatAPI):
    OAUTH_BASE_URL = "https://open.weixin.qq.com/connect/oauth2/authorize"

    def authorize_url(self, redirect_uri, state=None,scope='snsapi_base',agent_id=None):
        """
        构造网页授权链接
        详情请参考
        https://work.weixin.qq.com/api/doc#90000/90135/91022

        :param redirect_uri: 授权后重定向的回调链接地址
        :param state: 重定向后会带上 state 参数
        :param scope: 应用授权作用域。
                      snsapi_base：静默授权，可获取成员的基础信息（UserId与DeviceId）
                      snsapi_privateinfo：手动授权，可获取成员的详细信息，包含头像、二维码等敏感信息
        :param agent_id: 应用agentid，snsapi_privateinfo时必填
        :return: 返回的 JSON 数据包
        """
        redirect_uri = six.moves.urllib.parse.quote(redirect_uri, safe=b'')
        url_list = [
            self.OAUTH_BASE_URL,
            '?appid=',
            self._client.corp_id,
            '&redirect_uri=',
            redirect_uri,
            
        ]
        
        if scope=='snsapi_privateinfo' :
            if agent_id is None:
                raise ValueError('when set snsapi_privateinfo to scope,must set agent_id')
            url_list.append(f'&agentid={agent_id}')
                
        url_list.append(f'&scope={scope}')
        
        if state:
            url_list.extend(['&state=', state])
        url_list.append('#wechat_redirect')
        return ''.join(url_list)

    def get_user_info(self, code):
        """
        获取访问用户身份
        详情请参考
        https://developer.work.weixin.qq.com/document/path/91023

        :param code: 通过成员授权获取到的code
        :return: 返回的 JSON 数据包
        """

        return self._get(
            'auth/getuserinfo',
            params={
                'code': code,
            }
        )

    def get_user_detail(self, user_ticket):
        """
        获取访问用户敏感信息
        详情请参考
        https://developer.work.weixin.qq.com/document/path/95833
        
        :param user_ticket : 成员票据
        :return :    
        """
        return self._post('auth/getuserdetail', data={
            "user_ticket": user_ticket
        })

