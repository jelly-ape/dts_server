#!/usr/bin/env python
# -*- encoding: utf-8 -*-
STAT_SUCCESS = 'success'
STAT_FAILURE = 'failure'
STAT_INVALID_PARAMS = 'invalid_parameters'


class LogException(Exception):
    """用来记录日志的异常

    只有一个参数: status.
    """

    def __init__(self, status):
        self.__status = status

    @property
    def status(self):
        return self.__status
