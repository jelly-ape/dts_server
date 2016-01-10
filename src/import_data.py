#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import sys
import json
import random
import api.modules.photo_manager
import api.modules.album_manager

def main():
    photo_mgr = api.modules.photo_manager.PhotoManager()
    album_mgr = api.modules.album_manager.AlbumManager()
    for line in sys.stdin:
        line = line.strip()
        js = json.loads(line)

        album = {
            'press': js['press'],
            'name': js['album'],
            'cover': js['cover'],
            'models': js['models'],
        }
        album_mgr.insert(album)

        photo = {
            'press': js['press'],
            'album_name': js['album'],
            'url': js['url'],
            'rand': random.random(),
        }
        photo_mgr.insert(photo)


if __name__ == '__main__':
    main()
