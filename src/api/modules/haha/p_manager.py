#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import time
import api.libs


class PhotoManager(object):

    def __init__(self):
        self.__coll = self.__init_collection()

    def __init_collection(self):
        coll = api.libs.database.Database().photos
        coll.ensure_index(['props', pymongo.ASCENDING], unique=True)
        return coll

    def insert(self, info_dict):
        props = [{'ts': time.time()}]
        for k, v in info_dict.items():
            k = str(k)
            props.append({k: v})
        return self.__coll.insert({'props': props})

    def find(self, condition={}):
        return self.__coll.find({'props': condition})

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
