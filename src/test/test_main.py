import sys, os
sys.path.append(os.getcwd())

import pytest
import asyncio
import socket
import pickle
# import threading
import ssl
from time import sleep
from redis import Redis

# Run server
# from src.main import main
# main()


@pytest.fixture
def redis():
    redis = Redis(db=1)
    yield redis
    redis.flushdb()




# from test_main import run_client
# run_client("CLIENT_1")
# run_client("CLIENT_2")


@pytest.mark.skip()
def test_server_save_to_redis_success(redis, client):
    data = {"psql-1": 3}
    client.connect(('127.0.0.1', 3333))
    client.send(pickle.dumps(data))
    client.close()

    actual = redis.get("psql-1")
    assert int(actual) == value

@pytest.mark.skip()
def test_refuse_client_without_ssl(redis):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 3333))
    client.send(pickle.dumps(("psql-1", 3)))
    client.close()

    assert len(redis.keys()) == 0

@pytest.mark.skip()
def test_refuse_client_by_invalid_certificate():
    ssl_context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH, cafile="../server.crt"
    )
    ssl_context.load_cert_chain('unallowed_client.crt', 'unallowed_client.key')
    client = ssl_context.wrap_socket(
        socket.socket(), server_hostname='example.com'
    )

    with pytest.raises(Exception):
        client.connect(('127.0.0.1', 3333))

# def test_accept_only_key_value():
# pytest --disable-warnings
