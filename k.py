#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import random


def init_db():
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client['test']
    return db

db = init_db()
for i in xrange(4):
    db.test.create_index([('prop_{}'.format(i), pymongo.ASCENDING)])

def gen_photos():
    photo_num = 100000
    for i in xrange(photo_num):
        insert_dict = {}
        for i in xrange(20):
            insert_dict['prop_{}'.format(i)] = random.random()
        db.test.insert(insert_dict)

gen_photos()
