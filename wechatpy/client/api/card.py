# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatCard(BaseWeChatAPI):

    API_BASE_URL = 'https://api.weixin.qq.com/'

    def create(self, card_data):
        """
        创建卡券

        :param card_data: 卡券信息
        :return: 创建的卡券 ID
        """
        result = self._post(
            'card/create',
            data=card_data,
            result_processor=lambda x: x['card_id']
        )
        return result

    def batch_add_locations(self, location_data):
        """
        批量导入门店信息

        :param location_data: 门店信息
        :return: 门店 ID 列表，插入失败的门店元素值为 -1
        """
        result = self._post(
            'card/location/batchadd',
            data=location_data,
            result_processor=lambda x: x['location_id_list']
        )
        return result

    def batch_get_locations(self, offset=0, count=0):
        """
        批量获取门店信息
        """
        return self._post(
            'card/location/batchget',
            data={
                'offset': offset,
                'count': count
            }
        )

    def get_colors(self):
        """
        获得卡券的最新颜色列表，用于创建卡券
        :return: 颜色列表
        """
        result = self._get(
            'card/getcolors',
            result_processor=lambda x: x['colors']
        )
        return result

    def create_qrcode(self, qrcode_data):
        """
        创建卡券二维码

        :param qrcode_data: 二维码信息
        :return: 二维码 ticket，可使用 :func:show_qrcode 换取二维码文件
        """
        result = self._post(
            'card/qrcode/create',
            data=qrcode_data,
            result_processor=lambda x: x['ticket']
        )
        return result

    def create_landingpage(self, buffer_data):
        """
        创建货架
        """
        result = self._post(
            'card/landingpage/create',
            data=buffer_data
        )
        return result

    def get_html(self, card_id):
        """
        图文消息群发卡券
        """
        result = self._post(
            'card/mpnews/gethtml',
            data={
                'card_id': card_id
            },
            result_processor=lambda x: x['content']
        )
        return result

    def consume_code(self, code, card_id=None):
        """
        消耗 code
        """
        card_data = {
            'code': code
        }
        if card_id:
            card_data['card_id'] = card_id
        return self._post(
            'card/code/consume',
            data=card_data
        )

    def decrypt_code(self, encrypt_code):
        """
        解码加密的 code
        """
        result = self._post(
            'card/code/decrypt',
            data={
                'encrypt_code': encrypt_code
            },
            result_processor=lambda x: x['code']
        )
        return result

    def delete(self, card_id):
        """
        删除卡券
        """
        return self._post(
            'card/delete',
            data={
                'card_id': card_id
            }
        )

    def get_code(self, code, card_id=None, check_consume=True):
        """
        查询 code 信息
        """
        card_data = {
            'code': code
        }
        if card_id:
            card_data['card_id'] = card_id
        if not check_consume:
            card_data['check_consume'] = check_consume
        return self._post(
            'card/code/get',
            data=card_data
        )

    def get_card_list(self, openid, card_id=None):
        """
        用于获取用户卡包里的，属于该appid下的卡券。
        """
        card_data = {
            'openid': openid
        }
        if card_id:
            card_data['card_id'] = card_id
        return self._post(
            'card/user/getcardlist',
            data=card_data
        )

    def batch_get(self, offset=0, count=50, status_list=None):
        """
        批量查询卡券信息
        """
        card_data = {
            'offset': offset,
            'count': count
        }
        if status_list:
            card_data['status_list'] = status_list
        return self._post(
            'card/batchget',
            data=card_data
        )

    def get(self, card_id):
        """
        查询卡券详情
        """
        result = self._post(
            'card/get',
            data={
                'card_id': card_id
            },
            result_processor=lambda x: x['card']
        )
        return result

    def update_code(self, card_id, old_code, new_code):
        """
        更新卡券 code
        """
        return self._post(
            'card/code/update',
            data={
                'card_id': card_id,
                'code': old_code,
                'new_code': new_code
            }
        )

    def invalid_code(self, code, card_id=None):
        """
        设置卡券失效
        """
        card_data = {
            'code': code
        }
        if card_id:
            card_data['card_id'] = card_id
        return self._post(
            'card/code/unavailable',
            data=card_data
        )

    def update(self, card_data):
        """
        更新卡券信息
        """
        return self._post(
            'card/update',
            data=card_data
        )

    def set_paycell(self, card_id, is_open):
        """
        更新卡券信息
        """
        return self._post(
            'card/paycell/set',
            data={
                'card_id': card_id,
                'is_open': is_open
            }
        )

    def set_test_whitelist(self, openids=None, usernames=None):
        """
        设置卡券测试用户白名单
        """
        openids = openids or []
        usernames = usernames or []
        return self._post(
            'card/testwhitelist/set',
            data={
                'openid': openids,
                'username': usernames
            }
        )

    def activate_membercard(self, membership_number, code, init_bonus=0,
                            init_balance=0, card_id=None):
        """
        激活/绑定会员卡
        """
        card_data = {
            'membership_number': membership_number,
            'code': code,
            'init_bonus': init_bonus,
            'init_balance': init_balance
        }
        if card_id:
            card_data['card_id'] = card_id
        return self._post(
            'card/membercard/activate',
            data=card_data
        )

    def update_membercard(self, code, add_bonus=0, record_bonus='',
                          add_balance=0, record_balance='', card_id=None):
        """
        会员卡交易更新信息
        """
        card_data = {
            'code': code,
            'add_bonus': add_bonus,
            'add_balance': add_balance,
            'record_bonus': record_bonus,
            'record_balance': record_balance
        }
        if card_id:
            card_data['card_id'] = card_id
        return self._post(
            'card/membercard/updateuser',
            data=card_data
        )

    def update_movie_ticket(self, code, ticket_class, show_time, duration,
                            screening_room, seat_number, card_id=None):
        """
        更新电影票
        """
        ticket = {
            'code': code,
            'ticket_class': ticket_class,
            'show_time': show_time,
            'duration': duration,
            'screening_room': screening_room,
            'seat_number': seat_number
        }
        if card_id:
            ticket['card_id'] = card_id
        return self._post(
            'card/movieticket/updateuser',
            data=ticket
        )

    def checkin_boardingpass(self, code, passenger_name, seat_class,
                             etkt_bnr, seat='', gate='', boarding_time=None,
                             is_cancel=False, qrcode_data=None, card_id=None):
        """
        飞机票接口
        """
        data = {
            'code': code,
            'passenger_name': passenger_name,
            'class': seat_class,
            'etkt_bnr': etkt_bnr,
            'seat': seat,
            'gate': gate,
            'is_cancel': is_cancel
        }
        if boarding_time:
            data['boarding_time'] = boarding_time
        if qrcode_data:
            data['qrcode_data'] = qrcode_data
        if card_id:
            data['card_id'] = card_id
        return self._post(
            'card/boardingpass/checkin',
            data=data
        )

    def update_luckymoney_balance(self, code, balance, card_id=None):
        """
        更新红包余额
        """
        card_data = {
            'code': code,
            'balance': balance
        }
        if card_id:
            card_data['card_id'] = card_id
        return self._post(
            'card/luckymoney/updateuserbalance',
            data=card_data
        )

    def get_redirect_url(self, url, encrypt_code, card_id):
        """
        获取卡券跳转外链
        """
        from wechatpy.utils import WeChatSigner

        code = self.decrypt_code(encrypt_code)

        signer = WeChatSigner()
        signer.add_data(self.secret)
        signer.add_data(code)
        signer.add_data(card_id)
        signature = signer.signature

        r = '{url}?encrypt_code={code}&card_id={card_id}&signature={signature}'
        return r.format(
            url=url,
            code=encrypt_code,
            card_id=card_id,
            signature=signature
        )

    def deposit_code(self, card_id, codes):
        """
        导入code
        """
        card_data = {
            'card_id': card_id,
            'code': codes
        }
        return self._post(
            'card/code/deposit',
            data=card_data
        )

    def get_deposit_count(self, card_id):
        """
        查询导入code数目
        """
        card_data = {
            'card_id': card_id,
        }
        return self._post(
            'card/code/getdepositcount',
            data=card_data
        )

    def check_code(self, card_id, codes):
        """
        核查code
        """
        card_data = {
            'card_id': card_id,
            'code': codes
        }
        return self._post(
            'card/code/checkcode',
            data=card_data
        )

    def modify_stock(self, card_id, n):
        """
        修改库存
        """
        if n == 0:
            return
        card_data = {
            'card_id': card_id,
        }
        if n > 0:
            card_data['increase_stock_value'] = n
        elif n < 0:
            card_data['reduce_stock_value'] = -n
        return self._post(
            'card/modifystock',
            data=card_data
        )
