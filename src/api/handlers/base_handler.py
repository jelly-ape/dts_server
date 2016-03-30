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
        self._cdn_domain = self._conf.get('cdn', 'domain')
        # 子类中可以修改为自己所属的, 不然默认为 root logger
        self._logger = api.libs.log.get_logger('root')
        self._rets = {}

    def __get_arguments(self):
        """获取那些每个都需要的参数
        """
        # 输入参数
        self._params = api.libs.define.Dict()
        self._params['status'] = api.libs.define.STAT_SUCCESS
        self._params['ip'] = self.request.remote_ip
        self._params['uid'] = self.get_argument('uid')
        self._params['os'] = self.get_argument('os')
        self._params['skip'] = int(self.get_argument('skip', 0))
        self._params['max'] = int(self.get_argument('max', 20))
        self._params['ver'] = api.libs.version.Version(
            self.get_argument('ver', '0.0')
        )
        self._params['audit_ver'] = api.libs.version.Version(
            self._conf.get('server', 'audit_ver')
        )

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

    def _make_url(self, url_suffix):
        url = '{0}/{1}'.format(
            self._cdn_domain,
            url_suffix,
        )
        return url

    def _for_audit(self):
        condition = {}
        if self._params['audit_ver'] <= self._params['ver']:
            condition['press'] = 'ForAudit'
        else:
            condition['press'] = {'$ne': 'ForAudit'}
        return condition

    def process(self):
        pass

    def get(self):
        try:
            self.set_header("Access-Control-Allow-Origin", "*")
            self.__get_arguments()
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
