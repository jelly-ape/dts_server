#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
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
        return store

    def insert(self, albums_info):
        """插入一本写真集信息

        参数:
            albums_info: 写真集的各种参数信息, 格式必须为:
            {
                'name': 写真集名称,
                'press': 出版社, 和写真集名称一起唯一,
                'models': [模特1, 模特2, ...],
                'tags': [tag1, tag2, ...],
                'date': 出版日期, 如果找不到我会记作加入日期, 精度到日,
                'cover_url': 封面 URL,
                'description': 描述文字,
                'photos': 照片数目,
                'views': 浏览次数, 定时求和照片的浏览次数,
                'likes': 点赞数目, 定时求和照片的点赞次数,
                'rand': 0 ~ 1 之间的一个随机数. 可以定期更新, 索引!
            }
            也支持上述结构的列表.

        返回:
            成功返回 id, 否则抛出异常.

        异常:
            pymongo.errors.DuplicateKeyError: 已存在
        """
        for album in albums_info:
            if 'date' not in album:
                album['date'] = datetime.datetime.utcnow()
        return self.__store.insert(albums_info)

    def get(self, albums_info):
        """可以通过任意维度来查询, 但是只对 `name` 和 `press` 建了索引

        参数:
            albums_info: 请看 `insert_album` 的注释.

        返回:
            返回迭代器, 出错抛出异常
        """
        return self.__store.find(albums_info).sort('_id', pymongo.DESCENDING)
