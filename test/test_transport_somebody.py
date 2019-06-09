import asyncio
from sohot.transport import receive_listen


if __name__ == '__main__':
    asyncio.run(receive_listen('0.0.0.0',6666))


