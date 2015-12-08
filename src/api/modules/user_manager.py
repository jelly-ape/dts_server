#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import redis
import api.libs.config


class UserManager(object):
    """用户管理器. 实现了如下功能:

    1. 用户简介的添加和获取
    2. 用户点赞信息的获取, 为用户点赞.
    """

    def __init__(self):
        self.__redis = self.__init_redis()

    def __init_redis(self):
        conf = api.libs.config.get_config()
        host = conf.get('redis', 'host')
        port = conf.getint('redis', 'port')
        db_index = conf.getint('redis', 'db_index')
        return redis.StrictRedis(host=host, port=port, db=db_index)

    def set_profile(self, uid, profile_dict):
        """设定用户的简介. 必定是 key-value 结构

        参数:
            uid: 用户 ID
            profile_dict: 简介信息的词典

        返回:
            返回添加成功与否
        """
        assert type(profile_dict) is dict
        key = 'DTS_USER_PROFILE_' + uid
        return self.__redis.hmset(key, profile_dict)

    def get_profile(self, uid):
        """获取用户的简介

        参数:
            uid: 用户 ID

        返回:
            返回用户的简介词典. key-value 结构.
        """
        key = 'DTS_USER_PROFILE_' + uid
        return self.__redis.hgetall(key)

    def like(self, uid, photo_id):
        """点赞

        参数:
            uid: 用户 ID
            photo_id: 照片的 ID

        返回:
            返回添加成功与否
        """
        key = 'DTS_USER_LIKE_' + uid
        ret = self.__redis.sadd(key, photo_id)
        if ret == 0:  # 不成功或者已存在
            return self.__redis.sismember(key, photo_id)
        else:
            return True

    def get_likes(self, uid):
        """获取点赞的图片 ID 集合

        参数:
            uid: 用户 ID

        返回:
            返回该用户的点赞图片集合
        """
        key = 'DTS_USER_LIKE_' + uid
        return self.__redis.smembers(key)
