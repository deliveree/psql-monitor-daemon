import asyncio
import ssl
from redis import Redis
import pickle


def _get_ssl_context():
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.load_cert_chain('server.crt', 'server.key')
    ssl_context.load_verify_locations(cafile="client_certs.crt")
    return ssl_context


def _store(data):
    for key, value in data.items():
        if type(value) is dict:
            for field, field_value in value.items():
                redis.hset(key, field, field_value)
        else:
            redis.set(key, value)


async def _handle_client(reader, writer):
    try:
        addr = writer.get_extra_info('peername')
        print('Received connection from {}'.format(str(addr)))

        while True:
            data = await reader.read(2048)

            if not data:
                writer.close()
                print('Closed connection from ' + str(addr))
                break

            data = pickle.loads(data)
            _store(data)
            print(str(addr) + " wrote: ")
            print(str(data))
    except Exception as e:
        print(e)
        writer.close()


async def run_server():
    global redis
    redis = Redis(db=1)

    coro = await asyncio.start_server(
        _handle_client, '0.0.0.0', 1191, ssl=_get_ssl_context()
    )

    async with coro:
        await coro.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("Server is shut down by KeyboardInterrupt")
