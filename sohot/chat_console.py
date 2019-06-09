#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import time
import logging
from sohot.db_orm import query_remote_user_ip_port
from sohot.message import Message

now = lambda : time.time()


def isay():
    start = now()
    message = input('I say:')
    name  = input('@:')
    logging.info("Time:%f", now() - start)
    inetip, port = query_remote_user_ip_port(name)
    return message,name,inetip,port

def talk_with_somebody():
    message, name, ip, port = isay()
    message = Message(name,message,ip,port,'0')
    return message

def callback(future):
    message = future.result()
    logging.info("callback:%s",future.result())