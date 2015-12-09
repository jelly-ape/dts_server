#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import tornado.web
import tornado.ioloop
import api.handlers.albums_handler
import api.handlers.photos_handler
import api.handlers.like_handler
import api.handlers.liked_photos_handler


if __name__ == "__main__":
    root_path = r'/api/v1'
    application = tornado.web.Application([
        (root_path + r"/albums", api.handlers.albums_handler.AlbumsHandler),
        (root_path + r"/photos", api.handlers.photos_handler.PhotosHandler),
        (root_path + r"/user/like", api.handlers.like_handler.LikeHandler),
        (root_path + r"/user/liked_photos",
            api.handlers.liked_photos_handler.LikedPhotosHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
