#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import bson.objectid
import pymongo
import api.libs.database
import api.libs.utils


@api.libs.utils.singleton
class PhotoManager(object):
    """照片管理器
    """

    def __init__(self):
        self.__store = self.__init_store()

    def __init_store(self):
        """初始化储存
        """
        store = api.libs.database.Database().photos
        store.create_index(
            [('album_name', pymongo.ASCENDING), ('press', pymongo.ASCENDING)],
            unique=False,
        )

        store.create_index([('_id', pymongo.DESCENDING)], unique=True)
        store.create_index([('likes', pymongo.DESCENDING)], unique=False)
        store.create_index([('rand', pymongo.ASCENDING)], unique=False)
        return store

    def insert(self, photos_info):
        """插入图片信息

        参数:
            photos_info: 照片信息, 如下信息是必要的:
            {
                'press': 出版社,
                'album_name': 写真集名称,
                'url': 图片的 URL,
                'likes': 图片被点赞的次数,
            }
            也支持上述结构的列表.

        返回:
            成功返回 id, 否则抛出异常.
        """
        return self.__store.insert(photos_info)

    def get(self, photos_info={}):
        """可以通过任意维度来查询, 但是只对 `album_name` 建了索引

        参数:
            photos_info: 请看 `insert_photos` 的注释.

        返回:
            返回迭代器, 出错抛出异常. 支持 mongodb 的其他操作
        """
        return self.__store.find(photos_info)

    def update_likes(self, photo_id, likes):
        """更新点赞数

        参数:
            photo_id: 照片 ID (字符串)
            likes: 点赞数

        返回:
            返回更新成功与否
        """
        if type(photo_id) is not bson.objectid.ObjectId:
            photo_id = bson.objectid.ObjectId(photo_id)

        return self.__store.update(
            {'_id': photo_id},
            {'$set': {'likes': int(likes)}},
        )
