#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import tornado.web
import json
import urllib
import api.libs.define
import api.libs.config
import api.libs.log
import api.libs.version


class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self._conf = api.libs.config.get_config()
        self._domain = self._conf.get('server', 'domain')
        # 子类中可以修改为自己所属的, 不然默认为 root logger
        self._logger = api.libs.log.get_logger('root')
        self._rets = {}
        self.__log_arguments()

    def __log_arguments(self):
        """获取那些每个都需要的参数
        """
        # 输入参数
        self._params = {
            'ip': self.request.remote_ip,
            'status': api.libs.define.STAT_SUCCESS,
            'uid': self.get_argument('uid', None),
            'os': self.get_argument('os', None),
            'ver': api.libs.version.Version(self.get_argument('ver', '0.0')),
        }

    def _write(self):
        """传送到客户端, json 封装
        """
        ret = {
            'status': self._params['status'],
            'data': self._rets if self._rets else None,
        }
        ret_json = json.dumps(ret)
        super(BaseHandler, self).write(ret_json)
        # 时间消耗
        self._params['rt'] = '{0:.03f}'.format(
            1000 * self.request.request_time()
        )

    def _trace_url(self, tokens):
        """为链接包装一层跳转, 用来记录特殊事件.
        """
        token.update(self._params)
        url = '{0}/trace?{1}'.format(
            self._domain,
            urllib.urlencode(tokens),
        )
        return url

    def process(self):
        pass

    def get(self):
        try:
            self.process()
            logger_level = 'info'
        except api.libs.define.LogException as e:
            self._params['status'] = e.status
            logger_level = 'warning'
        except Exception as e:
            self._params['status'] = str(e).replace("\n", "-")
            logger_level = 'warning'
        finally:
            self._write()
            self._logger.flush(logger_level, self._params)
