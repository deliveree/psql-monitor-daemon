import os, sys
sys.path.append(os.path.abspath('../src'))

import pytest
import asyncio
import socket
import ssl
import logging
from json import dumps
from time import sleep
from redis import Redis
from multiprocessing import Process
from toml import load
import pdb

from modules.conf import load_conf
from modules.server import Server
from modules.fake_client import FakeClient as Client
from modules.test_payload import send_from_multiple_clients


conf = load_conf("conf")
host, port = conf["daemon"]["host"], conf["daemon"]["port"]

logging.basicConfig(
    filename="./test_main.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


@pytest.fixture
def redis():
    redis_conf = conf["redis"]
    redis = Redis(db=redis_conf["db"])
    yield redis
    redis.flushdb()


@pytest.fixture
def start_server_process(autouse=True):
    server_proc = Process(target=run_server, daemon=True)
    server_proc.start()
    sleep(0.05)
    yield
    server_proc.terminate()


def run_server():
    server = Server(conf)
    asyncio.run(server.start())


# @pytest.mark.skip()
def test_handle_single_dict(start_server_process, redis):
    key = "psql-1"
    value = "Power"

    client = Client(conf)
    client.connect()
    client.send({key: value})
    client.close()

    actual = redis.get(key)
    assert actual is not None and actual.decode() == value


# @pytest.mark.skip()
def test_handle_nested_dict(start_server_process, redis):
    key = "psql-1"
    field = "available_ram"
    value = 1000

    field_1 = "delay"
    value_1 = 100

    client = Client(conf)
    client.connect()
    client.send({
            key: {
                field: value,
                field_1: value_1
            }
    })
    actual_value = redis.hget(key, field)
    actual_value_1 = redis.hget(key, field_1)

    new_value = 100
    client.send(
        {key: {field: new_value}}
    )
    actual_new_value = redis.hget(key, field)

    new_field = "delay"
    client.send({key: {new_field: value}})
    client.close()

    actual_new_field_value = redis.hget(key, new_field)

    assert actual_value is not None and int(actual_value) == value
    assert actual_value_1 is not None and int(actual_value_1) == value_1
    assert actual_new_value is not None and int(actual_new_value) == new_value
    assert actual_new_field_value is not None


# @pytest.mark.skip()
def test_store_success_from_multiple_client(start_server_process, redis):
    total_client = 100
    send_from_multiple_clients(total_client, conf)
    actual_total = len(redis.keys())

    assert actual_total == total_client

# @pytest.mark.skip()
def test_refuse_client_without_ssl(start_server_process, redis):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(dumps({"psql-1": 3}).encode())
    client.close()

    assert len(redis.keys()) == 0


def test_refuse_client_by_invalid_certificate(start_server_process, redis):
    ssl_context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH, cafile=conf["path"]["server_crt_path"]
    )
    ssl_context.load_cert_chain(
        'creds/unallowed_client.crt', 'creds/unallowed_client.key'
    )
    client = ssl_context.wrap_socket(
        socket.socket(), server_hostname=host
    )

    client.connect((host, port))
    client.close()

    assert len(redis.keys()) == 0
