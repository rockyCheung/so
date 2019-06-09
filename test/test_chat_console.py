from sohot import context
from sohot.transport import BroadcastClient
import json
from sohot.message import Message

if __name__ == '__main__':
    broad = BroadcastClient(12000)
    message = Message(context.get('user')['nickname'], 'hi', context.get('server')['server_name'], context.get('server')['listen'], '1')
    js = json.dumps(message.__dict__)
    broad.broadcast(js)

    # while True:
    #     try:
    #         # start_echo_server()
    #
    #         message = talk_with_somebody()
    #         js = json.dumps(message.__dict__)
    #         asyncio.run(push_message(js,(message.remote_ip, message.remote_port)),debug=True)
    #     except Exception as e:
    #         logging.error(e)