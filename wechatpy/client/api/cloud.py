# -*- coding: utf-8 -*-

import json
from enum import IntEnum

import requests

from wechatpy.client.api.base import BaseWeChatAPI


class FileType(IntEnum):
    JSON = 1
    CSV = 2


class ConflictMode(IntEnum):
    INSERT = 1
    UPSERT = 2


class WeChatCloud(BaseWeChatAPI):
    API_BASE_URL = "https://api.weixin.qq.com/"

    def invoke_cloud_function(self, env, name, data=None):
        """
        触发云函数

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/functions/invokeCloudFunction.html

        :param env: 云开发环境 ID
        :param name: 云函数名称
        :param data: 云函数的传入参数，具体结构由开发者定义
        """
        return self._post(
            "tcb/invokecloudfunction",
            params={
                "env": env,
                "name": name,
            },
            data=data,
            result_processor=lambda x: json.loads(x["resp_data"]),
        )

    def db_import(self, env, collection, file_path, file_type, conflict_mode, stop_on_error=True):
        """
        数据库导入

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/database/databaseMigrateImport.html

        :param env: 云开发环境 ID
        :param collection: 导入 collection 名称
        :param file_path: 导入文件路径(导入文件需先上传到同环境的存储中，可使用开发者工具或 HTTP API的上传文件 API上传）
        :param file_type: 导入文件类型，文件格式参考数据库导入指引中的文件格式部分，值为数字，1 为 JSON，2 为 CSV
        :param stop_on_error: 是否在遇到错误时停止导入，默认为 True
        :param conflict_mode: 冲突处理模式, 值为数字，1 为 INSERT，2 为 UPSERT
        :return: 导入任务 ID，可使用数据库迁移进度查询 API 查询导入进度及结果
        """
        return self._post(
            "tcb/databasemigrateimport",
            data={
                "env": env,
                "collection_name": collection,
                "file_path": file_path,
                "file_type": file_type,
                "stop_on_error": stop_on_error,
                "conflict_mode": conflict_mode,
            },
            result_processor=lambda x: x["job_id"],
        )

    def db_export(self, env, file_path, file_type, query):
        """
        数据库导出

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/database/databaseMigrateExport.html

        :param env: 云开发环境 ID
        :param file_path: 导出文件路径(导入文件需先上传到同环境的存储中，可使用开发者工具或 HTTP API的上传文件 API上传）
        :param file_type: 导出文件类型，文件格式参考数据库导入指引中的文件格式部分，值为数字，1 为 JSON，2 为 CSV
        :param query: 导出条件
        :return: 导出任务 ID，可使用数据库迁移进度查询 API 查询导出结果，获取文件下载链接
        """
        return self._post(
            "tcb/databasemigrateexport",
            data={
                "env": env,
                "file_path": file_path,
                "file_type": file_type,
                "query": query,
            },
            result_processor=lambda x: x["job_id"],
        )

    def db_query_migrate_info(self, env, job_id):
        """
        数据库迁移状态查询

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/database/databaseMigrateQueryInfo.html

        :param env: 云开发环境 ID
        :param job_id: 任务 ID
        """
        return self._post(
            "tcb/databasemigratequeryinfo",
            data={
                "env": env,
                "job_id": job_id,
            },
        )

    def db_update_index(self, env, collection, create_indexes=None, drop_indexes=None):
        """
        变更数据库索引

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/database/updateIndex.html

        :param env: 云开发环境 ID
        :param collection: 导出 collection 名称
        """
        assert create_indexes or drop_indexes
        return self._post(
            "tcb/updateindex",
            data={
                "env": env,
                "collection_name": collection,
                "create_indexes": create_indexes or [],
                "drop_indexes": create_indexes or [],
            },
        )

    def db_add_collection(self, env, collection):
        """
        新增集合

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/database/databaseCollectionAdd.html

        :param env: 云开发环境 ID
        :param collection: 集合名称
        """
        return self._post(
            "tcb/databasecollectionadd",
            data={
                "env": env,
                "collection_name": collection,
            },
        )

    def db_delete_collection(self, env, collection):
        """
        删除集合

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/database/databaseCollectionDelete.html

        :param env: 云开发环境 ID
        :param collection: 集合名称
        """
        return self._post(
            "tcb/databasecollectiondelete",
            data={
                "env": env,
                "collection_name": collection,
            },
        )

    def db_get_collection(self, env, offset=0, limit=10):
        """
        获取特定云环境下集合信息

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/database/databaseCollectionGet.html

        :param env: 云开发环境 ID
        :param offset: 偏移量，默认为 0
        :param limit: 获取数量限制， 默认为 10
        """
        return self._post(
            "tcb/databasecollectionget",
            data={
                "env": env,
                "offset": offset,
                "limit": limit,
            },
        )

    def db_add(self, env, query):
        """
        数据库插入记录

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/database/databaseAdd.html

        :param env: 云开发环境 ID
        :param query: 数据库操作语句
        :return: 返回插入成功的数据集合主键 _id 列表
        """
        return self._post(
            "tcb/databaseadd",
            data={
                "env": env,
                "query": query,
            },
            result_processor=lambda x: x["id_list"],
        )

    def db_delete(self, env, query):
        """
        数据库删除记录

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/database/databaseDelete.html

        :param env: 云开发环境 ID
        :param query: 数据库操作语句
        :return: 返回删除记录数量
        """
        return self._post(
            "tcb/databasedelete",
            data={
                "env": env,
                "query": query,
            },
            result_processor=lambda x: x["deleted"],
        )

    def db_update(self, env, query):
        """
        数据更新记录

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/database/databaseUpdate.html

        :param env: 云开发环境 ID
        :param query: 数据库操作语句
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "tcb/databaseupdate",
            data={
                "env": env,
                "query": query,
            },
        )

    def db_query(self, env, query):
        """
        数据库查询记录

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/database/databaseQuery.html

        :param env: 云开发环境 ID
        :param query: 数据库操作语句
        :return: 返回的 JSON 数据包
        """
        return self._post(
            "tcb/databasequery",
            data={
                "env": env,
                "query": query,
            },
        )

    def db_aggregate(self, env, query):
        """
        数据库聚合

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/database/databaseAggregate.html

        :param env: 云开发环境 ID
        :param query: 数据库操作语句
        :return: 返回记录列表
        """
        return self._post(
            "tcb/databaseaggregate",
            data={
                "env": env,
                "query": query,
            },
            result_processor=lambda x: x["data"],
        )

    def db_count(self, env, query):
        """
        统计集合记录数或统计查询语句对应的结果记录数

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/database/databaseCount.html

        :param env: 云开发环境 ID
        :param query: 数据库操作语句
        :return: 返回记录数量
        """
        return self._post(
            "tcb/databasecount",
            data={
                "env": env,
                "query": query,
            },
            result_processor=lambda x: x["count"],
        )

    def upload_file(self, env, path):
        """
        获取文件上传链接

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/storage/uploadFile.html

        :param env: 云开发环境 ID
        """
        with open(path, "rb") as f:
            res = self._post(
                "tcb/uploadfile",
                data={
                    "env": env,
                    "path": path,
                },
            )
            signature = res["authorization"]
            token = res["token"]
            cos_file_id = res["cos_file_id"]
            upload_res = requests.post(
                res["url"],
                files={
                    "key": path,
                    "Signature": signature,
                    "x-cos-security-token": token,
                    "x-cos-meta-fileid": cos_file_id,
                    # 注意！file 字段须放在最后，否则上传大文件会失败
                    "file": f,
                },
            )
            upload_res.raise_for_status()
            return upload_res

    def download_files(self, env, file_list):
        """
        获取文件下载链接

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/storage/batchDownloadFile.html

        :param env: 云开发环境 ID
        :param file_list: 文件列表
        :return: 返回文件列表
        """
        return self._post(
            "tcb/batchdownloadfile",
            data={
                "env": env,
                "file_list": file_list,
            },
            result_processor=lambda x: x["file_list"],
        )

    def delete_files(self, env, fileid_list):
        """
        删除文件

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/storage/batchDeleteFile.html

        :param env: 云开发环境 ID
        :param fileid_list: 文件 ID 列表
        :return: 被删除的文件列表
        """
        return self._post(
            "tcb/batchdeletefile",
            data={
                "env": env,
                "fileid_list": fileid_list,
            },
            result_processor=lambda x: x["delete_list"],
        )

    def get_qcloud_token(self, lifespan=7200):
        """
        获取腾讯云 API 调用凭证

        详情请参考
        https://developers.weixin.qq.com/miniprogram/dev/wxcloud/reference-http-api/utils/getQcloudToken.html
        """
        return self._post("tcb/getqcloudtoken", data={"lifespan": lifespan})
