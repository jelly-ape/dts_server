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
        self.__coll = api.libs.database.Database().albums
        self.__coll.create_index(
            [('name', pymongo.ASCENDING), ('press', pymongo.ASCENDING)],
            unique=True,
        )

    def insert(self, album):
        """插入写真集信息

        参数:
            album: 写真集的各种参数信息, 格式必须为:
            {
                'name': 写真集名称,
                'press': 出版社, 和写真集名称一起唯一,
                'models': [模特1, 模特2, ...],
                'ts': 添加的时间戳,
                'cover_url': 封面 URL,
            }
            也支持上述结构的列表.

        返回:
            成功返回 id, 否则为 None
        """
        album['ts'] = int(time.time())
        try:
            return self.__coll.insert(album)
        except pymongo.errors.DuplicateKeyError:
            return True

    def get(self, album={}):
        """可以通过任意维度来查询

        参数:
            album: 请看 `insert` 的注释.

        返回:
            返回迭代器, 出错抛出异常
        """
        return self.__coll.find(album)
