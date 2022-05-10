# -*- coding: utf-8 -*-
import json

from wechatpy.pay.api.base import BaseWeChatPayAPI


class WeChatMedia(BaseWeChatPayAPI):
    def upload_image(self, file_bytes, filename, sha256, mimetype="image/jpg"):
        """
        上传图片

        :param file_bytes: 上传的文件二进制
        :param filename: 文件名
        :param sha256: 图片文件的文件摘要，即对图片文件的二进制内容进行sha256计算得到的值。
        :param mimetype: 文件mime type
        :return: 返回的结果数据
        """
        meta = {"filename": filename, "sha256": sha256}
        data = {
            "meta": json.dumps(meta),
        }
        return self._post(
            "merchant/media/upload", files=[("file", (filename, file_bytes, mimetype))], data=data, sign_data=meta
        )
