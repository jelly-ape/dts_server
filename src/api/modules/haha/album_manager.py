#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import time
import api.libs.database
import api.libs.utils


@api.libs.utils.singleton
class AlbumManager(object):
    """写真集管理器
    """

    def __init__(self):
        self.__store = self.__init_store()

    def __init_store(self):
        """初始化储存
        """
        store = api.libs.database.Database().albums
        store.create_index(
            [('name', pymongo.ASCENDING), ('press', pymongo.ASCENDING)],
            unique=True,
        )

        store.create_index(
            [('ts', pymongo.DESCENDING)],
            unique=False,
        )
        return store

    def insert(self, albums_info):
        """插入写真集信息

        参数:
            albums_info: 写真集的各种参数信息, 格式必须为:
            {
                'name': 写真集名称,
                'press': 出版社, 和写真集名称一起唯一,
                'models': [模特1, 模特2, ...],
                'ts': 添加的时间戳,
                'cover_url': 封面 URL,
                'likes': 点赞数目, 定时求和照片的点赞次数,
            }
            也支持上述结构的列表.

        返回:
            成功返回 id, 否则抛出异常.

        异常:
            pymongo.errors.DuplicateKeyError: 已存在
        """
        for album in albums_info:
            if 'ts' not in album:
                album['ts'] = time.time()
        return self.__store.insert(albums_info)

    def get(self, albums_info={}):
        """可以通过任意维度来查询, 但是只对 `name` 和 `press` 建了索引

        参数:
            albums_info: 请看 `insert_album` 的注释.

        返回:
            返回迭代器, 出错抛出异常
        """
        return self.__store.find(albums_info)
