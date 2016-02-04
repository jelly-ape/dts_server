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

    def parse_photo(self, photo, small_width=250):
        ret = {'ori': {}, 'thumb': {}}
        pattern = photo['url']
        width = photo['width']
        height = photo['height']
        # 原图
        ret['ori']['url'] = pattern.format(pre=40, size=1280)
        ret['ori']['width'] = width
        ret['ori']['height'] = height

        # 缩略图
        if width > small_width:
            small_height = int(float(small_width) / width * height)
        else:
            small_height = height

        ret['thumb']['url'] = pattern.format(pre=41, size=small_width)
        ret['thumb']['width'] = small_width
        ret['thumb']['height'] = small_height
        return ret

    def process(self):
        tumblr_mgr = api.modules.tumblr_manager.TumblrManager()
        photos = tumblr_mgr.get(**self._params)
        self._rets['photos'] = []
        for photo in photos:
            self._rets['photos'].append(self.parse_photo(photo))
