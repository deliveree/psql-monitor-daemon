import pytest
import asyncio
import socket
import ssl
from pickle import dumps
from time import sleep
from redis import Redis
from ssl import SSLCertVerificationError


PORT = 1191
HOST = "localhost"
SERVER_CERT_PATH = "../src/server.crt"


@pytest.fixture
def redis():
    redis = Redis(db=1)
    yield redis
    redis.flushdb()


def get_ssl_client():
    ssl_context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH, cafile=SERVER_CERT_PATH
    )
    ssl_context.load_cert_chain('client.crt', 'client.key')

    client = ssl_context.wrap_socket(
        socket.socket(), server_hostname=HOST
    )
    client.connect((HOST, PORT))
    return client


def test_handle_single_dict(redis):
    key = "psql-1"
    value = "Power"
    client = get_ssl_client()
    client.send(dumps({key: value}))
    client.close()
    sleep(0.05)

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


# @pytest.mark.skip()
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
