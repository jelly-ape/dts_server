#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
添加照片信息
"""
import sys
import api.libs.database

db = api.libs.database.Database()
photos = []

for line in sys.stdin:
    try:
        line = line.strip()
        press, title, models, url = line.split("\t")
        p = url.split("/")[-1]
        cover = "{}/{}/{}".format(press, title.split("-")[0], p)
        params = {
            'press': press,
            'album_name': title,
            'url': cover,
        }
        photos.append(params)
    except:
        continue
print db.insert_photos(photos)
