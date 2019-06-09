#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from sohot import context


class Message():
    def __init__(self,opponent,sms,ip,port,broadcast):
        self.nickname = context.get('user')['nickname']
        self.opponent = opponent
        self.sms = sms
        self.remote_ip = ip
        self.remote_port = port
        self.broadcast = broadcast
        self.server = context.get('server')
    def __repr__(self):
        return "{'myname':'%s','opponent':'%s', 'sms':'%s', 'remote_ip':'%s','remote_port':'%s','broadcast': '%s',server' : %s }" % (
            self.nickname, self.opponent, self.sms,self.remote_ip, self.remote_port, self.broadcast,self.server)
