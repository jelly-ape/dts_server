#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import api.handlers.base_handler
import api.modules.user_manager
import api.libs.log


class GetLikesHandler(api.handlers.base_handler.BaseHandler):
    """用户点赞信息 URI
    """

    def __init__(self, *args, **kwargs):
        super(GetLikesHandler, self).__init__(*args, **kwargs)
        self.__user_mgr = api.modules.user_manager.UserManager()

    def __log_arguments(self):
        self._logs['uid'] = self.get_argument('uid', None)
        self._logs['os'] = self.get_argument('os', None)
        self._logs['ver'] = self.get_argument('ver', None)

    def get(self):
        logger_level = 'info'
        try:
            logger = api.libs.log.get_logger('user')
            self.__log_arguments()
            photo_ids = self.__user_mgr.get_likes(
                self.get_argument('uid'),
            )
            self._rets['liked_photos'] = list(photo_ids)
        except Exception as e:
            self._errno = api.libs.define.ERR_FAILURE
            self._logs['msg'] = str(e)
            logger_level = 'warning'
        finally:
            self._logs['errno'] = self._errno
            logger.flush(logger_level, self._logs)
            self._write()
