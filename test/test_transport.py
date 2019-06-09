import asyncio
from sohot.transport import receive_listen
from sohot import context
import json

if __name__ == '__main__':
    asyncio.run(receive_listen(context.get('server')['server_name'],context.get('server')['listen']))
    # ss = '{"myname":"edsnickname","opponent":"ss", "sms":"hi", "remote_ip":"127.0.0.1","remote_port":"12000","server" : {"listen": 12000, "server_name": "127.0.0.1", "root": "/usr", "hot": {"count": 4}} }'
    # dd = {'s':'a','dd':1}
    # print(json.loads(ss))



