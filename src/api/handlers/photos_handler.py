#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import api.libs.log
import api.handlers.base_handler
import api.modules.photo_manager


class PhotosHandler(api.handlers.base_handler.BaseHandler):
    """照片 URI
    """

    def __init__(self, *args, **kwargs):
        super(PhotosHandler, self).__init__(*args, **kwargs)
        self._logger = api.libs.log.get_logger('photos')

    def __get_arguments(self):
        """获取需要记录日志的参数, 包括:

            beg: 起始位置 (从0开始, 默认0)
            press: 出版社
            album_name: 写真集名字
        """
        self.request.arguments.items
        self._params['press'] = self.get_argument('press', None)
        self._params['album_name'] = self.get_argument('album_name')

    def __get_photos(self):
        """获取图片
        """
        # 0 为不限制
        self._rets['photos'] = []

        photo_mgr = api.modules.photo_manager.PhotoManager()
        photos = photo_mgr.get({
            'press': self._params['press'],
            'album_name': self._params['album_name'],
        }, skip=self._params['skip'], max=self._params['max'])

        for photo in photos:
            url = self._make_url(photo['url'])
            photo_id = str(photo['_id'])
            self._rets['photos'].append({
                "url": url,
                "id": photo_id,
            })

    def __get_album_info(self):
        """获取专辑信息
        """
        album_mgr = api.modules.album_manager.AlbumManager()
        album_gen = album_mgr.get({
            'name': self._params['album_name'],
            'press': self._params['press'],
        })

        album = album_gen.next()
        self._rets['album_name'] = album['name']
        self._rets['press'] = album['press']
        self._rets['models'] = album['models']

    def process(self):
        self.__get_arguments()
        self.__get_photos()
        #self.__get_album_info()
