#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import time
import api.libs.database


class PhotoManager(object):

    def __init__(self):
        self.__coll = self.__init_collection()

    def __init_collection(self):
        coll = api.libs.database.Database().photos_test
        return coll

    def make_index(self):
        self.__coll.ensure_index(['props', pymongo.ASCENDING], unique=True)

    def insert(self, info_dict):
        props = [{'ts': time.time()}]
        for k, v in info_dict.items():
            k = str(k)
            props.append({k: v})
        return self.__coll.insert({'props': props})

    def find(self, condition={}):
        return self.__coll.find({'props': {'$elemMatch': condition}})

    def albums(self):
        print "begin"
        ret = self.__coll.group(
            ['album', 'press'],
            None,
            None,
            None,
        )
        print "end"
        return ret
