#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import api.handlers.base_handler
import api.modules.user_manager
import api.libs.log


class LikeHandler(api.handlers.base_handler.BaseHandler):
    """点赞 URI
    """

    def __init__(self, *args, **kwargs):
        super(LikeHandler, self).__init__(*args, **kwargs)
        self._logger = api.libs.log.get_logger('user')
        self.__user_mgr = api.modules.user_manager.UserManager()

    def __log_arguments(self):
        self._params['photo_id'] = self.get_argument('photo_id', None)

    def process(self):
        self.__log_arguments()
        self.__user_mgr.insert_a_like(
            self._params['uid'],
            self._params['photo_id'],
        )
