#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
其实原本我是想用 motor 的, 但是我不会用, 而且感觉不优雅.
"""
import pymongo
from bson.objectid import ObjectId
import utils
import config


@utils.singleton
class Database(object):
    """数据储存的类, 封装了几个函数
    """

    def __init__(self):
        """初始化数据库以及对应的 collections
        """
        self.__db = self.__init_db()

    def __init_db(self):
        conf = config.get_config()
        host = conf.get('mongodb', 'host')
        port = conf.getint('mongodb', 'port')
        db_name = conf.get('mongodb', 'db_name')
        client = pymongo.MongoClient(host, port)
        db = client[db_name]
        return db

    def __getattr__(self, collection_name):
        return self.__db.__getattr__(collection_name)
