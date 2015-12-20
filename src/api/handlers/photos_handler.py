#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import api.libs.log
import api.handlers.base_handler
import api.modules.photo_manager
import api.modules.user_manager


class PhotosHandler(api.handlers.base_handler.BaseHandler):
    """照片 URI
    """

    def __init__(self, *args, **kwargs):
        super(PhotosHandler, self).__init__(*args, **kwargs)
        self._logger = api.libs.log.get_logger('photos')
        self.__photo_mgr = api.modules.photo_manager.PhotoManager()
        self.__album_mgr = api.modules.album_manager.AlbumManager()
        self.__user_mgr = api.modules.user_manager.UserManager()
        self.__cdn_domain = self._conf.get('cdn', 'domain')

    def __log_arguments(self):
        """获取需要记录日志的参数, 包括:

            max: 最大加载数目 (默认: 0, 无限制)
            beg: 起始位置 (从0开始, 默认0)
            press: 出版社
            album_name: 写真集名字
        """
        try:
            self._params['max'] = int(self.get_argument('max'))
        except:
            self._params['max'] = 0

        try:
            self._params['beg'] = int(self.get_argument('beg'))
        except:
            self._params['beg'] = 0

        self._params['press'] = self.get_argument('press', None)
        self._params['album_name'] = self.get_argument('album_name', None)

    def __get_photos(self, liked_photos):
        """获取图片
        """
        # 0 为不限制
        self._rets['photos'] = []

        photos = self.__photo_mgr.get({
            'album_name': self.get_argument('album_name', None),
            'press': self.get_argument('press', None),
        }).skip(self._params['beg']).limit(self._params['max'])

        for photo in photos:
            photo_id = str(photo['_id'])
            self._rets['photos'].append({
                "url": "{0}/{1}".format(self.__cdn_domain, photo['url']),
                "id": photo_id,
                'is_like': True if photo_id in liked_photos else False,
            })

    def __get_album_info(self):
        """获取专辑信息
        """
        album_gen = self.__album_mgr.get({
            'name': self._params['album_name'],
            'press': self._params['press'],
        })

        album = album_gen.next()
        self._rets['album_name'] = album['name']
        self._rets['press'] = album['press']
        self._rets['models'] = album['models']

    def __get_liked_photos(self):
        liked_photos = set()
        photo_gen = self.__user_mgr.get_likes(self._params['uid'])
        for photo in photo_gen:
            liked_photos.add(bson.objectid.ObjectId(photo['photo_id']))
        return liked_photos

    def process(self):
        self.__log_arguments()
        liked_photos = self.__get_liked_photos()
        self.__get_photos(liked_photos)
        self.__get_album_info()
