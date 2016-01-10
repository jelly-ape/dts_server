#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import api.handlers.base_handler
import api.modules.like_manager
import api.libs.log


class LikeHandler(api.handlers.base_handler.BaseHandler):
    """点赞 URI
    """

    def __init__(self, *args, **kwargs):
        super(LikeHandler, self).__init__(*args, **kwargs)
        self._logger = api.libs.log.get_logger('user')

    def __get_arguments(self):
        self._params['photo_id'] = self.get_argument('photo_id', None)

    def __insert_like(self):
        like_mgr = api.modules.like_manager.LikeManager()
        uid = self._params['uid']
        photo_id = self._params['photo_id']
        like_mgr.insert(uid, photo_id)

    def process(self):
        self.__get_arguments()
        self.__insert_like()
