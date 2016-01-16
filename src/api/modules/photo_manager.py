#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import random
import pymongo
import time
import bson.objectid
import api.libs.database
import api.libs.utils


@api.libs.utils.singleton
class PhotoManager(object):
    """照片管理器
    """

    def __init__(self):
        self.__coll = api.libs.database.Database().photos
        self.__coll.create_index(
            [('name', pymongo.ASCENDING), ('press', pymongo.ASCENDING)],
        )
        self.__coll.create_index([('likes', pymongo.DESCENDING)])
        self.__coll.create_index([('rand', pymongo.ASCENDING)])

    def insert(self, photo):
        photo['ts'] = int(time.time())
        try:
            return self.__coll.insert(photo)
        except pymongo.errors.DuplicateKeyError:
            return True

    def get(self, photo={}):
        return self.__coll.find(photo)

    def shuffle(self):
        """随机刷新
        """
        photos = self.__coll.find({})
        for photo in photos:
            photo['rand'] = random.random()
            self.__coll.save(photo)

    def update_likes(self, photo_id, likes):
        """更新点赞数

        参数:
            photo_id: 照片 ID (字符串)
            likes: 点赞数

        返回:
            返回更新成功与否
        """
        if type(photo_id) is not bson.objectid.ObjectId:
            try:
                photo_id = bson.objectid.ObjectId(photo_id)
            except bson.errors.InvalidId:
                return False

        return self.__coll.update(
            {'_id': photo_id},
            {'$set': {'likes': int(likes)}},
        )
