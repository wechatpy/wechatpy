from operator import itemgetter

from wechatpy.client.api.base import BaseWeChatAPI


class WeChatExport(BaseWeChatAPI):
    """
    对于数据量大的企业，企业微信提供异步导出、CDN下载数据的方式来获取通讯录数据。

    https://developer.work.weixin.qq.com/document/path/94850
    """

    def export_simple_user(self, encoding_aeskey: str, block_size: int = 10**6) -> str:
        """
        导出成员

        详情请参考：
        https://developer.work.weixin.qq.com/document/path/94849

        :param encoding_aeskey: 必填。base64encode的加密密钥，长度固定为43，base64decode之后即得到AESKey。
                                加密方式采用AES-256-CBC方式，数据采用PKCS#7填充至32字节的倍数；
                                IV初始向量大小为16字节，取AESKey前16字节，详见：http://tools.ietf.org/html/rfc2315
        :param block_size：选填。每块数据的人员数，支持范围 [10^4,10^6]，默认值为10^6。

        :return: 任务 ID，可通过获取导出结果接口查询任务结果。
        :rtype: str
        """
        data = {
            "encoding_aeskey": encoding_aeskey,
            "block_size": block_size,
        }
        return self._post("export/simple_user", data=data, result_processor=itemgetter("jobid"))

    def export_user(self, encoding_aeskey: str, block_size: int = 10**6) -> str:
        """
        导出成员详情

        详情请参考：
        https://developer.work.weixin.qq.com/document/path/94851
        """
        data = {
            "encoding_aeskey": encoding_aeskey,
            "block_size": block_size,
        }
        return self._post("export/user", data=data, result_processor=itemgetter("jobid"))

    def export_department(self, encoding_aeskey: str, block_size: int = 10**6) -> str:
        """
        导出部门

        详情请参考：
        https://developer.work.weixin.qq.com/document/path/94852
        """
        data = {
            "encoding_aeskey": encoding_aeskey,
            "block_size": block_size,
        }
        return self._post("export/department", data=data, result_processor=itemgetter("jobid"))

    def export_taguser(self, tagid: int, encoding_aeskey: str, block_size: int = 10**6) -> str:
        """
        导出标签成员

        详情请参考：
        https://developer.work.weixin.qq.com/document/path/94853

        :param tagid: 必填。需要导出的标签。
        :param encoding_aeskey: 必填。base64encode的加密密钥。
        :param block_size：选填。每块数据的人员数。

        :return: 任务 ID，可通过获取导出结果接口查询任务结果。
        """
        data = {
            "tagid": tagid,
            "encoding_aeskey": encoding_aeskey,
            "block_size": block_size,
        }
        return self._post("export/taguser", data=data, result_processor=itemgetter("jobid"))

    def get_result(self, jobid: str) -> dict:
        """
        获取导出结果

        详情请参考：
        https://developer.work.weixin.qq.com/document/path/94854

        :param jobid: 任务 ID。
        """
        params = {"jobid": jobid}
        return self._get("export/get_result", params=params)
