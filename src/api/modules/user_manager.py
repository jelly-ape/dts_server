#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import time
import api.libs.database
import api.libs.utils


@api.libs.utils.singleton
class UserManager(object):
    """用户管理器. 实现了如下功能:

    1. 用户简介的添加和获取
    2. 用户点赞信息的获取, 为用户点赞.
    """

    def __init__(self):
        self.__like_store = self.__init_store()

    def __init_store(self):
        """初始化储存
        """
        like_store = api.libs.database.Database().likes
        like_store.create_index(
            [('uid', pymongo.ASCENDING), ('photo_id', pymongo.ASCENDING)],
            unique=True,
        )
        return like_store

    def insert_a_like(self, uid, photo_id):
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
            'date': time.time(),  # UTC 时间戳
        }
        try:
            return self.__like_store.insert(like_info)
        except pymongo.errors.DuplicateKeyError:
            return True
        except Exception as e:
            raise e

    def get_likes(self, uid):
        """获取用户的点赞情况

        参数:
            uid: 用户 ID

        返回:
            返回点赞的照片 ID
        """
        return self.__like_store.find({'uid': uid})
