import logging
import asyncio
import pdb
from redis import Redis
import pickle


async def connect_client(reader, writer):
    try:
        addr = writer.get_extra_info('peername')
        print('Recieved connection from {}'.format(str(addr)))

        while True:
            data = await asyncio.wait_for(reader.read(1024), timeout=5)
            # array = pickle.loads(data)
            # key, value = array[0], array[1]
            # redis.set(key, value)

            if not data:
                writer.close()
                print('Closed connection from ' + str(addr))
                break

            print(str(addr) + " wrote: ")
            print(str(data))
            # await writer.drain()
    except Exception as e:
        print(e)
        writer.close()


def get_corotine():
    global redis
    redis = Redis(db=1)


async def run_server():
    global redis
    redis = Redis(db=1)

    coro = await asyncio.start_server(connect_client, '127.0.0.1', 3333)

    try:
        async with coro:
            await coro.serve_forever()
    except KeyboardInterrupt:
        print("I AM BEING KeyboardInterrupt")
        pass


def main():
    asyncio.run(run_server())

# from main import main