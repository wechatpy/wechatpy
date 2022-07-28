# -*- coding: utf-8 -*-
import hashlib
import json

from wechatpy.pay.v3.api.base import BaseWeChatPayAPI


class WeChatMedia(BaseWeChatPayAPI):
    def upload_image(self, file_bytes, filename, mimetype="image/jpg"):
        """
        上传图片

        :param file_bytes: 上传的文件二进制
        :param filename: 文件名
        :param mimetype: 文件mime type
        :return: 返回的结果数据
        """
        meta = {"filename": filename, "sha256": hashlib.sha256(file_bytes).hexdigest()}
        data = {
            "meta": json.dumps(meta),
        }
        return self._post(
            "merchant/media/upload", files=[("file", (filename, file_bytes, mimetype))], data=data, sign_data=meta
        )
