#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import api.handlers.base_handler
import api.modules.photo_manager
import api.libs.log


class RankingHandler(api.handlers.base_handler.BaseHandler):

    def __init__(self, *args, **kwargs):
        super(RankingHandler, self).__init__(*args, **kwargs)
        self._logger = api.libs.log.get_logger('ranking')

    def __get_ranking(self):
        photo_mgr = api.modules.photo_manager.PhotoManager()
        photos = photo_mgr.get().sort('likes', pymongo.DESCENDING)
        photos = photos.skip(self._params['skip']).limit(self._params['max'])
        self._rets['photos'] = []
        for photo in photos:
            url = self._make_url(photo['url'])
            photo_id = str(photo['_id'])
            likes = int(photo.get('likes', 0))
            if likes > 0:
                self._rets['photos'].append({
                    'id': photo_id,
                    'url': url,
                    'likes': likes,
                })

    def process(self):
        self.__get_ranking()
