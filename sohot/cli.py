#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import asyncio
import logging
from sohot.transport import push_message,BroadcastClient
import json
from sohot.message import Message
from sohot.chat_console import talk_with_somebody
import click
from sohot import engine,Base
from sohot.transport import receive_listen
from sohot import context

@click.command(help='sohot commands')
@click.option('--init', is_flag=True, help='Init the db.')
@click.option('--run',is_flag=True, help='Run the sohot server.')
@click.option('--talk',is_flag=True, help='Talk to opponent.')
def start_so(init,run,talk):
    if init:
        Base.metadata.create_all(engine)
    if talk:
        broad = BroadcastClient(12000)
        message = Message(context.get('user')['nickname'], 'hi', context.get('server')['server_name'],
                          context.get('server')['listen'], '1')
        js = json.dumps(message.__dict__)
        broad.broadcast(js)

        while True:
            try:
                # start_echo_server()

                message = talk_with_somebody()
                js = json.dumps(message.__dict__)
                asyncio.run(push_message(js, (message.remote_ip, message.remote_port)), debug=True)
            except Exception as e:
                logging.error(e)
    if run:
        asyncio.run(receive_listen(context.get('server')['server_name'], context.get('server')['listen']))