#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import logging
import logging.config
import asyncio
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime
import socket
from sohot.tasks import write_db

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        logging.info(type(message))
        logging.info('Receiced %r from %s' % (message, addr))
        mesdict = json.loads(message)
        write_db.delay(mesdict)

class EchoClientProtocol:
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None
        self.on_con_lost = loop.create_future()

    def connection_made(self, transport):
        self.transport = transport
        logging.info('I Send mesage:%s', self.message)
        self.transport.sendto(self.message.encode())
        self.transport.close()
#客户端只发不收，服务端只收不发
    def datagram_received(self, data, addr):
        logging.info("Received:%s", data.decode())

        logging.info("Close the socket")
        # self.transport.close()

    def error_received(self, exc):
        logging.info('Error received:', exc)

    def connection_lost(self, exc):
        logging.info("Connection closed")
        self.on_con_lost.set_result(True)

# ***************************************************
# 广播主机信息：ip、port 用户信息：别名、用户唯一识别码
# 如果用户信息在本地数据库中不存在，将生成信息，并插入数据库中
# 将用户信息转化为json广播出去
# ***************************************************
class BroadcastClient():
    def __init__(self,port):
        self.dest = ('<broadcast>', port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client.setblocking(False)

    def broadcast(self,message):
        try:
            self.client.sendto(message.encode("utf-8"), self.dest)
        finally:
            self.client.close()

class TCPServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()

class TCPClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost, loop):
        self.message = message
        self.loop = loop
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


# ***************************************************
# 客户端向服务端推送信息
# ***************************************************
async def push_message(message,default_dest = ('127.0.0.1', 12000)):
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoClientProtocol(message, loop),
        remote_addr=default_dest)
    try:
        await protocol.on_con_lost
    finally:
        transport.close()


async def receive_listen(ip,port):
    print("Starting UDP server")

    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr=(ip, port))
    while True:
        await asyncio.sleep(300)


async def start_tcp_server():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: TCPServerProtocol(),
        '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()

async def start_tcp_client():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    message = 'Hello World!'

    transport, protocol = await loop.create_connection(
        lambda: TCPClientProtocol(message, on_con_lost, loop),
        '127.0.0.1', 8888)

    # Wait until the protocol signals that the connection
    # is lost and close the transport.
    try:
        await on_con_lost
    finally:
        transport.close()

def alchemy_to_json():
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    data = obj.__getattribute__(field)
                    try:
                        if isinstance(data, datetime):
                            data = data.strftime('%Y-%m-%d %H:%M:%S')
                        json.dumps(data)  # this will fail on non-encodable values, like other classes
                        fields[field] = data
                    except TypeError:
                        fields[field] = None
                return fields

            return json.JSONEncoder.default(self, obj)
    return AlchemyEncoder


