#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import os
import api.libs.utils


@api.libs.utils.singleton
class TumblrManager(object):

    def __init__(self):
        self._photos = self.__load()

    def __load(self):
        photos = []

        photo_file = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '../../../data',
            'porn_imgs.part',
        )
        with open(photo_file) as f:
            for line in f:
                line = line.strip()
                photos.append(line)
        return photos

    def get(self, **kwargs):
        skip = int(kwargs.get('skip', 0))
        limit = int(kwargs.get('max', 20))

        return self._photos[skip: skip + limit]
