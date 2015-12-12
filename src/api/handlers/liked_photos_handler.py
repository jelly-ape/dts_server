#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import bson.objectid
import api.handlers.base_handler
import api.modules.user_manager
import api.modules.photo_manager
import api.libs.log


class LikedPhotosHandler(api.handlers.base_handler.BaseHandler):
    """用户点赞信息 URI
    """

    def __init__(self, *args, **kwargs):
        super(LikedPhotosHandler, self).__init__(*args, **kwargs)
        self._logger = api.libs.log.get_logger('user')
        self.__cdn_domain = self._conf.get('cdn', 'domain')
        self.__user_mgr = api.modules.user_manager.UserManager()
        self.__photo_mgr = api.modules.photo_manager.PhotoManager()

    def __get_photos(self):
        rets, photo_ids, date_dict = [], [], {}

        photo_gen = self.__user_mgr.get_likes(self._params['uid'])
        for photo in photo_gen:
            photo_ids.append(bson.objectid.ObjectId(photo['photo_id']))
            date_dict[photo['photo_id']] = photo['date']

        photos = self.__photo_mgr.get({'_id': {'$in': photo_ids}})
        for photo in photos:
            photo_id = str(photo['_id'])
            photo_url = '{0}/{1}'.format(
                self.__cdn_domain,
                photo['url'],
            )
            rets.append({
                'date': date_dict[photo_id],
                'photo_id': photo_id,
                'url': photo_url,
            })

        return rets

    def process(self):
        photos = self.__get_photos()
        self._rets['liked_photos'] = photos
