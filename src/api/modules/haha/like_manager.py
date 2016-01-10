#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import time
import api.libs.database
import api.libs.utils


@api.libs.utils.singleton
class LikeManager(object):
    """点赞管理器
    """

    def __init__(self):
        self.__store = self.__init_store()

    def __init_store(self):
        """初始化储存
        """
        store = api.libs.database.Database().likes
        store.create_index(
            [('uid', pymongo.ASCENDING), ('photo_id', pymongo.ASCENDING)],
            unique=True,
        )
        return store

    def insert(self, uid, photo_id):
        """添加一个点赞

        参数:
            uid: 用户 ID
            photo_id: 照片 ID

        返回:
            返回点赞成功与否
        """
        like_info = {
            'uid': uid,
            'photo_id': photo_id,
            'ts': time.time(),  # UTC 时间戳
        }
        try:
            return self.__store.insert(like_info)
        except pymongo.errors.DuplicateKeyError:
            return True
        except Exception as e:
            raise e

    def get(self, uid):
        """获取用户的点赞情况

        参数:
            uid: 用户 ID

        返回:
            返回点赞的照片 ID
        """
        return self.__store.find({'uid': uid})

    def rank(self):
        """获取点赞排行榜

        返回:
            返回点赞数从高到底的结果的迭代器
        """
        return self.__store.group(
            ['photo_id'],
            None,
            {'count': 0},
            'function(obj, prev){prev.count++;}',
        )
