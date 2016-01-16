#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import tornado.web
import tornado.ioloop
import api.modules.update_manager
import api.handlers.albums_handler
import api.handlers.photos_handler
import api.handlers.like_handler
import api.handlers.liked_photos_handler
import api.handlers.random_handler
import api.handlers.ranking_handler


def release_run():
    root_path = r'/api/v1'
    application = tornado.web.Application([
        (root_path + r"/albums",
         api.handlers.albums_handler.AlbumsHandler),
        (root_path + r"/photos",
         api.handlers.photos_handler.PhotosHandler),
        (root_path + r"/user/like",
         api.handlers.like_handler.LikeHandler),
        (root_path + r"/user/liked_photos",
         api.handlers.liked_photos_handler.LikedPhotosHandler),
        (root_path + r"/random",
         api.handlers.random_handler.RandomHandler),
        (root_path + r"/ranking",
         api.handlers.ranking_handler.RankingHandler),
    ])

    # 定时任务
    update_mgr = api.modules.update_manager.UpdateManager()
    update_mgr.update_likes()

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    release_run()
