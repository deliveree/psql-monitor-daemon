import pytest
import asyncio
import socket
import pickle
import ssl
from redis import Redis


PORT = 1191
HOST = "localhost"


@pytest.fixture
def redis():
    redis = Redis(db=1)
    yield redis
    redis.flushdb()


def test_server_save_to_redis_success(redis):
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="../server.crt")
    ssl_context.load_cert_chain('client.crt', 'client.key')
    client = ssl_context.wrap_socket(
        socket.socket(), server_hostname=HOST
    )

    key = "psql-1"
    value = 3
    client.connect((HOST, PORT))
    client.send(pickle.dumps({key: value}))
    client.close()

    actual = redis.get(key)
    assert int(actual) == value


def test_store_success_from_multiple_client(redis):
    from test_payload import run

    total_client = 10
    run("localhost", total_client)

    actual_total = len(redis.keys())
    assert actual_total == total_client


def test_refuse_client_without_ssl(redis):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.send(pickle.dumps(("psql-1", 3)))
    client.close()

    assert len(redis.keys()) == 0


def test_refuse_client_by_invalid_certificate():
    ssl_context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH, cafile="../server.crt"
    )
    ssl_context.load_cert_chain('unallowed_client.crt', 'unallowed_client.key')
    client = ssl_context.wrap_socket(
        socket.socket(), server_hostname=HOST
    )

    with pytest.raises(Exception):
        client.connect((HOST, PORT))

