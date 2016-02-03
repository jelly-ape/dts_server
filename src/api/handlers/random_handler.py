#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import random
import api.handlers.base_handler
import api.modules.photo_manager
import api.libs.log


class RandomHandler(api.handlers.base_handler.BaseHandler):

    def __init__(self, *args, **kwargs):
        super(RandomHandler, self).__init__(*args, **kwargs)
        self._logger = api.libs.log.get_logger('photos')

    def __get_photos(self):
        photo_mgr = api.modules.photo_manager.PhotoManager()
        photos = photo_mgr.get().sort('rand', pymongo.ASCENDING)
        photos = photos.skip(self._params['skip']).limit(self._params['max'])

        self._rets['photos'] = []
        for photo in photos:
            url = self._make_url(photo['url'])
            photo_id = str(photo['_id'])
            self._rets['photos'].append({
                "url": url,
                "id": photo_id,
                'likes': photo.get('likes', 0),
                'album_name': photo.get('albums_name'),
                'press': photo.get('press'),
            })

    def process(self):
        self.__get_photos()
