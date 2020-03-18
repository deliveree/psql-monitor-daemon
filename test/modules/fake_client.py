import ssl
import socket
from json import dumps
from modules.conf import load_conf


class FakeClient():
    def __init__(self, conf):
        daemon_conf = conf["daemon"]
        self.deamon_port = daemon_conf["port"]
        self.deamon_host = daemon_conf["host"]

        paths = conf["path"]

        self.client = self._get_ssl_context(paths).wrap_socket(
            socket.socket(), server_hostname=self.deamon_host
        )

    def _get_ssl_context(self, paths):
        ssl_context = ssl.create_default_context(
            ssl.Purpose.SERVER_AUTH, cafile=paths["server_crt_path"]
        )
        ssl_context.load_cert_chain(
            paths["client_crt_path"], paths["client_key_path"]
        )
        return ssl_context

    def connect(self):
        self.client.connect((self.deamon_host, self.deamon_port))

    def send(self, data):
        self.client.send(dumps(data).encode())

    def close(self):
        self.client.close()
