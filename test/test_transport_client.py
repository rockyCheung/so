import asyncio
from sohot.transport import EchoServerProtocol,EchoClientProtocol,BroadcastClient


async def testEchoClientProtocol():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()
    message = "Hello World!"
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoClientProtocol(message, loop),
        remote_addr=('127.0.0.1', 9999),allow_broadcast=False)

    try:
        await protocol.on_con_lost
    finally:
        transport.close()
def test_EchoClientProtocol():
    asyncio.run(testEchoClientProtocol())

import socket


if __name__ == '__main__':
    '''
    客户端使用UDP时，首先仍然创建基于UDP的Socket，然后，不需要调用connect()，直接通过sendto()给服务器发数据：
    '''



    test_EchoClientProtocol()
    client = BroadcastClient(9999)
    client.broadcast('hello')