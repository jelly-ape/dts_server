#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import api.modules.like_manager


class UpdateManager(object):

    def update_likes(self):
        """更新 like
        """
        # 获取全量点赞数
        like_mgr = api.modules.like_manager.LikeManager()
        photo_mgr = api.modules.photo_manager.PhotoManager()
        photos = like_mgr.rank()
        for photo in photos:
            photo_mgr.update_likes(
                photo['photo_id'],
                photo['count'],
            )
