#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import api.modules.like_manager
import api.modules.photo_manager


class UpdateManager(object):

    def __init__(self):
        self._like_mgr = api.modules.like_manager.LikeManager()
        self._photo_mgr = api.modules.photo_manager.PhotoManager()

    def update_likes(self):
        """更新 like
        """
        # 获取全量点赞数
        photos = self._like_mgr.rank()
        for photo in photos:
            self._photo_mgr.update_likes(
                photo['photo_id'],
                photo['count'],
            )

    def update_rand(self):
        """更新随机数
        """
        self._photo_mgr.shuffle()
