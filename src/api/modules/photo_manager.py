#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import random
import pymongo
import time
import api.libs.database
import api.libs.utils


@api.libs.utils.singleton
class PhotoManager(object):
    """照片管理器
    """

    def __init__(self):
        self.__coll = api.libs.database.Database().photos

    def insert(self, photo):
        photo['ts'] = int(time.time())
        return self.__coll.insert(photo)

    def get(self, photo={}):
        return self.__coll.find(photo)

    def shuffle(self):
        photos = self.__coll.find({})
        for photo in photos:
            photo['rand'] = random.random()
            self.__coll.save(photo)
