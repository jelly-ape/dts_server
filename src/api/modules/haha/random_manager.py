#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import bson.objectid
import random
import pymongo


@api.libs.utils.singleton
class RandomManager(object):
    """id 是固定的, 只有 id 和 photo_id 两个维度
    """

    def __init__(self):
        self.__store = self.__init_store()

    def __init_store(self):
        """初始化储存
        """
        store = api.libs.database.Database().photos
        store.create_index(
            [('rand', pymongo.ASCENDING)],
            unique=True,
        )
        return store

    def update(self):
        """更新所有照片
        """
        # 获取所有照片

