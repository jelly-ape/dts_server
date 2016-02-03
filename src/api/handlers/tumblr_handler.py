#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import api.handlers.base_handler
import api.libs.log
import api.modules.tumblr_manager


class TumblrHandler(api.handlers.base_handler.BaseHandler):
    """写真集 URI
    """

    def __init__(self, *args, **kwargs):
        super(TumblrHandler, self).__init__(*args, **kwargs)
        self._logger = api.libs.log.get_logger('tumblr')

    def process(self):
        tumblr_mgr = api.modules.tumblr_manager.TumblrManager()
        photos = tumblr_mgr.get(**self._params)
        self._rets['photos'] = []
        for photo in photos:
            self._rets['photos'].append({
                'ori': photo.format(pre=40, size=1280),
                'alt': photo.format(pre=41, size=500),
            })
