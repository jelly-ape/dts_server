#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
添加写真集信息
"""
import sys
import api.libs.database

db = api.libs.database.Database()
albums = []

uniq_set = set()

for line in sys.stdin:
    try:
        line = line.strip()
        #title, cover, models, press
        press, title, models, cover = line.split("\t")
        if title in uniq_set:
            continue

        uniq_set.add(title)
        first = cover.split("/")[-1]
        cover = "{}/{}/{}".format(press, title.split("-")[0], first)
        params = {
            'press': press,
            'name': title,
            'models': models.split(" "),
            'cover_url': cover,
        }
        #print params
        albums.append(params)
    except:
        continue
print db.insert_albums(albums)
