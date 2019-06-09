#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import logging
import wrapt
import yaml
import logging.config
# ***************************************************
# 设置loggin参数
# ***************************************************
def setup_logging(config,default_level = logging.INFO):
    if config is not None:
        logging.config.dictConfig(config.get('logging'))
    else:
        logging.basicConfig(level = default_level)

def sohot_init(default_conf):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        props = Config(default_conf)  # 读取文件
        return wrapped(props,*args, **kwargs)
    return wrapper

class Config():
    def __init__(self,config):
        file = open(config, encoding='utf-8')
        self.conf = yaml.safe_load(file)

    def get(self,key):
        return self.conf.get(key)