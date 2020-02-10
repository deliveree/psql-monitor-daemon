from toml import load
import logging
import asyncio


async def connect_client(reader, writer):
    try:
        addr = writer.get_extra_info('peername')
        print('Recieved connection from {}'.format(str(addr)))

        while True:
            data = await asyncio.wait_for(reader.read(1024), timeout=5)

            if not data:
                writer.close()
                print('Closed connection from ' + str(addr))
                break

            print(str(addr) + " wrote: ")
            print(str(data))
            # await writer.drain()
    except Exception as e:
        print(e)
    finally:
        writer.close()


async def run_server():
    server = await asyncio.start_server(connect_client, '127.0.0.1', 3333)
    await server.serve_forever()


def main():
    asyncio.run(run_server())

# from main import main