import logging
import asyncio
import pdb
import ssl
from redis import Redis
import pickle
import time


async def connect_client(reader, writer):
    try:
        addr = writer.get_extra_info('peername')
        print('Recieved connection from {}'.format(str(addr)))

        while True:
            data = await asyncio.wait_for(reader.read(1024), timeout=5)
            data = pickle.loads(data)
            redis.mset(data)

            if not data:
                writer.close()
                print('Closed connection from ' + str(addr))
                break

            print(str(addr) + " wrote: ")
            print(str(data))
    except Exception as e:
        print(e)
        writer.close()


async def run_server():
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.load_cert_chain('server.crt', 'server.key')
    ssl_context.load_verify_locations(cafile="client_certs.crt")

    global redis
    redis = Redis(db=1)

    coro = await asyncio.start_server(
        connect_client, '127.0.0.1', 3333, ssl=ssl_context
    )

    async with coro:
        await coro.serve_forever()


def main():
    asyncio.run(run_server())

main()
