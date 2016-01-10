#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import api.handlers.base_handler
import api.modules.album_manager
import api.libs.log


class AlbumsHandler(api.handlers.base_handler.BaseHandler):
    """写真集 URI
    """

    def __init__(self, *args, **kwargs):
        super(AlbumsHandler, self).__init__(*args, **kwargs)
        self._logger = api.libs.log.get_logger('albums')

    def __get_albums(self):
        """从服务器中获取写真集列表
        """
        self._rets['albums'] = []
        #photo_mgr = api.modules.photo_manager.PhotoManager()
        #photos = photo_mgr.find(condition).sort('_id', pymongo.DESCENDING)
        #photos = photos.skip(self._params['skip']).limit(self._params['max'])

        print "lala"
        album_mgr = api.modules.album_manager.AlbumManager()
        albums = album_mgr.get().sort('ts', pymongo.DESCENDING)
        albums = albums.skip(self._params['skip']).limit(self._params['max'])

        for album in albums:
            # 为图片添加域名, 这样比较灵活
            album['_id'] = str(album['_id'])
            album['cover_url'] = self._make_url(album['cover_url'])
            self._rets['albums'].append(album)

    def process(self):
        self.__get_albums()
