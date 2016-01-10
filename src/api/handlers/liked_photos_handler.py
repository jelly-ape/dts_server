#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import bson.objectid
import api.handlers.base_handler
import api.modules.like_manager
import api.modules.photo_manager
import api.libs.log


class LikedPhotosHandler(api.handlers.base_handler.BaseHandler):
    """用户点赞信息 URI
    """

    def __init__(self, *args, **kwargs):
        super(LikedPhotosHandler, self).__init__(*args, **kwargs)
        self._logger = api.libs.log.get_logger('user')

    def __get_liked_photos(self):
        liked_photos = {}
        like_mgr = api.modules.like_manager.LikeManager()
        photos = like_mgr.get(self._params['uid'])
        for photo in photos:
            photo_id = photo['_id']
            liked_photos[photo_id] = photo['ts']
        return liked_photos

    def __add_photo_url(self, liked_photos):
        photo_mgr = api.modules.photo_manager.PhotoManager()
        photos = photo_mgr.get({'_id': {'$in': list(liked_photos.keys())}})
        rets = []
        for photo in photos:
            photo_id = photo['_id']
            photo_url = self._make_url(photo['url'])
            rets.append({
                'ts': liked_photos[photo_id],
                'photo_id': str(photo_id),
                'url': photo_url,
            })
        self._params['liked_photos'] = rets

    def process(self):
        liked_photos = self.__get_liked_photos()
        self.__add_photo_url(liked_photos)
