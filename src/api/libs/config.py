#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
封装读取配置的对象
"""
import ConfigParser
import os


__all__ = ['get_config']
__config = None


def get_config(config_file='server.cfg'):
    """获取配置文件信息的 ConfigParser. 工厂模式

    参数:
        config_file: 配置文件 (直接从 conf 文件夹下开始)

    返回:
        返回 ConfigParser 对象
    """
    global __config

    # 工厂模式，只有一个实例
    if __config is None:
        config = ConfigParser.ConfigParser()
        # 默认配置文件位于项目根目录下的 conf 文件夹下
        # 文件名为 server.cfg
        config_file = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '../../../conf',
            config_file,
        )
        config.read(config_file)

    return config
