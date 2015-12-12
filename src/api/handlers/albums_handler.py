#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import bson.objectid
import api.handlers.base_handler
import api.modules.album_manager
import api.libs.log


class AlbumsHandler(api.handlers.base_handler.BaseHandler):
    """写真集 URI
    """

    def __init__(self, *args, **kwargs):
        super(AlbumsHandler, self).__init__(*args, **kwargs)
        self._logger = api.libs.log.get_logger('albums')
        self.__album_mgr = api.modules.album_manager.AlbumManager()
        self.__cdn_domain = self._conf.get('cdn', 'domain')

    def __log_arguments(self):
        """获取需要记录日志的参数, 包括:

        参数:
            max: 最大加载数目 (默认: 10)
            beg_id: 起始 ID
        """
        # 最大张数
        try:
            self._params['max'] = int(self.get_argument('max'))
        except:
            self._params['max'] = 10

        # 起始位置
        self._params['beg_id'] = self.get_argument('beg_id', None)

    def __get_albums(self):
        """从服务器中获取写真集列表
        """
        try:
            albums_info = {'_id': {
                '$lt': bson.objectid.ObjectId(self._params['beg_id']),
            }}
        except:
            albums_info = {}

        # 拼接图片 URL
        self._rets['albums'] = []
        last_id = None

        albums = self.__album_mgr.get(albums_info).limit(self._params['max'])
        for album in albums:
            last_id = album['_id']
            del album['_id']
            del album['date']
            # 为图片添加域名, 这样比较灵活
            cover_url = '{0}/{1}'.format(
                self.__cdn_domain,
                album['cover_url']
            )
            album['cover_url'] = cover_url
            self._rets['albums'].append(album)
        self._rets['last_id'] = str(last_id)

    def process(self):
        self.__log_arguments()
        self.__get_albums()
