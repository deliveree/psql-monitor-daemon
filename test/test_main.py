import os, sys
sys.path.append(os.path.abspath('../src'))

import pytest
import asyncio
import socket
import ssl
from json import dumps
from time import sleep
from redis import Redis
import ssl
from multiprocessing import Process
from toml import load
from modules.conf import load_conf
from modules.server import Server
from modules.fake_client import FakeClient as Client


conf = load_conf("conf")
PORT = 1191
HOST = "localhost"


@pytest.fixture
def redis():
    redis_conf = conf["redis"]
    redis = Redis(db=redis_conf["db"])
    yield redis
    redis.flushdb()


def run_server():
    server = Server(conf)
    asyncio.run(server.start())


def test_handle_single_dict(redis):
    server_proc = Process(
        target=run_server, daemon=True
    )
    server_proc.start()

    key = "psql-1"
    value = "Power"
    
    client = Client(conf)
    client.connect()
    client.send({key: value})
    client.close()
    sleep(0.05)
    server_proc.terminate()

    actual = redis.get(key)
    assert actual is not None and actual.decode() == value


@pytest.mark.skip()
def test_test_handle_nested_dict(redis):
    key = "psql-1"
    field = "available_ram"
    value = 1000

    client = get_ssl_client()
    client.send(dumps({key: {field: value}}))
    sleep(0.05)
    actual_value = redis.hget(key, field)

    new_value = 100
    client.send(dumps({key: {field: new_value}}))
    sleep(0.05)
    actual_new_value = redis.hget(key, field)

    new_field = "delay"
    client.send(dumps({key: {new_field: value}}))
    client.close()
    sleep(0.05)

    actual_new_field_value = redis.hget(key, new_field)

    assert actual_value is not None and int(actual_value) == value
    assert actual_new_value is not None and int(actual_new_value) == new_value
    assert actual_new_field_value is not None


@pytest.mark.skip()
def test_store_success_from_multiple_client(redis):
    from test_payload import send_from_multiple_clients

    total_client = 100
    send_from_multiple_clients("localhost", total_client)
    sleep(0.05)
    actual_total = len(redis.keys())

    assert actual_total == total_client


@pytest.mark.skip()
def test_refuse_client_without_ssl(redis):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.send(dumps(("psql-1", 3)))
    client.close()

    assert len(redis.keys()) == 0


@pytest.mark.skip()
def test_refuse_client_by_invalid_certificate():
    ssl_context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH, cafile=SERVER_CERT_PATH
    )
    ssl_context.load_cert_chain('unallowed_client.crt', 'unallowed_client.key')
    client = ssl_context.wrap_socket(
        socket.socket(), server_hostname=HOST
    )

    with pytest.raises(OSError):
        client.connect((HOST, PORT))
