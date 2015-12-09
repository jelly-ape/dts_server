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
        self.__user_mgr = api.modules.user_manager.UserManager()

    def __log_arguments(self):
        self._logs['uid'] = self.get_argument('uid', None)
        self._logs['os'] = self.get_argument('os', None)
        self._logs['ver'] = self.get_argument('ver', None)
        self._logs['photo_id'] = self.get_argument('photo_id', None)

    def get(self):
        logger_level = 'info'
        try:
            logger = api.libs.log.get_logger('user')
            self.__log_arguments()
            self.__user_mgr.insert_a_like(
                self.get_argument('uid'),
                self.get_argument('photo_id'),
            )
        except Exception as e:
            self._errno = api.libs.define.ERR_FAILURE
            self._logs['msg'] = str(e)
            logger_level = 'warning'
        finally:
            self._logs['errno'] = self._errno
            logger.flush(logger_level, self._logs)
            self._write()
