import ssl
from redis import Redis
import json
import asyncio
import logging


class Server:
    def __init__(self, conf):
        redis_conf = conf["redis"]
        self.redis = Redis(
            db=redis_conf["db"],
            host=redis_conf["host"]
        )
        self.host = conf["daemon"]["host"]
        self.port = conf["daemon"]["port"]
        self.paths = conf["path"]

    def _get_ssl_context(self):
        paths = self.paths
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.load_cert_chain(
            paths["server_crt_path"], paths["server_key_path"]
        )
        ssl_context.load_verify_locations(cafile=paths["client_certs_path"])
        return ssl_context

    def _store(self, data):
        for key, value in data.items():
            if type(value) is dict:
                for field, field_value in value.items():
                    self.redis.hset(key, field, field_value)
            else:
                self.redis.set(key, value)

    async def _handle_client(self, reader, writer):
        try:
            addr = writer.get_extra_info('peername')
            print('Received connection from {}'.format(str(addr)))

            while True:
                data = await reader.read(2048)

                if not data:
                    writer.close()
                    print('Closed connection from ' + str(addr))
                    break

                data = json.loads(data)
                self._store(data)
                logging.info(str(addr) + " sent: ")
                logging.info(str(data))
        except Exception as e:
            print(e)
            writer.close()

    async def start(self):
        coro = await asyncio.start_server(
            self._handle_client,
            self.host,
            self.port,
            ssl=self._get_ssl_context()
        )

        async with coro:
            await coro.serve_forever()
