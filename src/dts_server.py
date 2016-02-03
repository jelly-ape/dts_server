#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import tornado.web
import tornado.ioloop
import api.libs.config
import api.modules.update_manager
import api.handlers.albums_handler
import api.handlers.photos_handler
import api.handlers.like_handler
import api.handlers.liked_photos_handler
import api.handlers.random_handler
import api.handlers.ranking_handler
import api.handlers.tumblr_handler


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
        (root_path + r"/tumblr",
         api.handlers.tumblr_handler.TumblrHandler),
    ])

    conf = api.libs.config.get_config()
    update_likes_period = conf.getint('server', 'update_likes_period')
    update_rand_period = conf.getint('server', 'update_rand_period')
    port = conf.getint('server', 'port')

    # 定时任务
    update_mgr = api.modules.update_manager.UpdateManager()
    # 第一次运行
    update_mgr.update_likes()

    # 定时任务更新
    tornado.ioloop.PeriodicCallback(update_mgr.update_likes,
                                    update_likes_period).start()
    # 全部重新随机需要 4 秒
    tornado.ioloop.PeriodicCallback(update_mgr.update_rand,
                                    update_rand_period).start()

    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    release_run()
