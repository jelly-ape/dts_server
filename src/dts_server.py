#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import tornado.web
import tornado.ioloop
import api.handlers.albums_handler
import api.handlers.photos_handler
import api.handlers.like_handler
import api.handlers.get_likes_handler


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/api/v1/albums", api.handlers.albums_handler.AlbumsHandler),
        (r"/api/v1/photos", api.handlers.photos_handler.PhotosHandler),
        (r"/api/v1/like", api.handlers.like_handler.LikeHandler),
        (r"/api/v1/get_likes", api.handlers.get_likes_handler.GetLikesHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
