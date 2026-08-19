# -*- coding: utf-8 -*-


from wechatpy.client.api.base import BaseWeChatAPI


class WeChatMedia(BaseWeChatAPI):
    """素材管理

    https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html
    """

    def upload(self, media_type, media_file):
        """
        新增临时素材
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html

        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param media_file: 要上传的文件，一个 File-object

        :return: 返回的 JSON 数据包
        """
        return self._post(url="media/upload", params={"type": media_type}, files={"media": media_file})

    def download(self, media_id):
        """
        获取临时素材
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Get_temporary_materials.html

        :param media_id: 媒体文件 ID

        :return: requests 的 Response 实例
        """
        return self._get("media/get", params={"media_id": media_id})

    def get_url(self, media_id):
        """
        获取临时素材下载地址

        :param media_id: 媒体文件 ID
        :return: 临时素材下载地址
        """
        return f"https://api.weixin.qq.com/cgi-bin/media/get?access_token={self.access_token}&media_id={media_id}"

    def upload_video(self, media_id, title, description):
        """
        群发视频消息时获取视频 media_id
        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param media_id: 需通过基础支持中的上传下载多媒体文件 :func:`upload` 来得到
        :param title: 视频标题
        :param description: 视频描述

        :return: 返回的 JSON 数据包
        """
        return self._post(
            url="media/uploadvideo",
            data={"media_id": media_id, "title": title, "description": description},
        )

    def upload_articles(self, articles):
        """
        上传图文消息素材
        详情请参考
        http://mp.weixin.qq.com/wiki/15/5380a4e6f02f2ffdc7981a8ed7a40753.html

        :param articles: 图文消息数组
        :return: 返回的 JSON 数据包
        """
        articles_data = []
        for article in articles:
            articles_data.append(
                {
                    "thumb_media_id": article["thumb_media_id"],
                    "title": article["title"],
                    "content": article["content"],
                    "author": article.get("author", ""),
                    "content_source_url": article.get("content_source_url", ""),
                    "digest": article.get("digest", ""),
                    "show_cover_pic": article.get("show_cover_pic", 0),
                }
            )
        return self._post("media/uploadnews", data={"articles": articles_data})

    def upload_image(self, media_file):
        """
        上传群发消息内的图片
        详情请参考
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Adding_Permanent_Assets.html

        :param media_file: 要上传的文件，一个 File-object
        :return: 上传成功时返回图片 URL
        """
        res = self._post(
            url="media/uploadimg",
            files={"media": media_file},
            result_processor=lambda x: x["url"],
        )
        return res

    upload_mass_image = upload_image
