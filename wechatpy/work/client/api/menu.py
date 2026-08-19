# -*- coding: utf-8 -*-


from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMenu(BaseWeChatAPI):
    """
    自定义菜单
    """

    def create(self, agent_id: int, menu_data: dict) -> dict:
        """
        创建菜单

        详情请参考：
        https://developer.work.weixin.qq.com/document/path/90231

        :param agent_id: 应用id
        """
        return self._post("menu/create", params={"agentid": agent_id}, data=menu_data)

    def get(self, agent_id: int) -> dict:
        """
        获取菜单

        详情请参考：
        https://developer.work.weixin.qq.com/document/path/90232

        :param agent_id: 应用id
        """
        return self._get("menu/get", params={"agentid": agent_id})

    def delete(self, agent_id: int) -> dict:
        """
        删除菜单

        详情请参考：
        https://developer.work.weixin.qq.com/document/path/90233

        :param agent_id: 应用id
        """
        return self._get("menu/delete", params={"agentid": agent_id})

    def update(self, agent_id: int, menu_data: dict) -> dict:
        self.delete(agent_id)
        return self.create(agent_id, menu_data)
