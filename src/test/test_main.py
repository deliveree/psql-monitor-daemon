import sys, os
sys.path.append(os.getcwd())

import pytest
# import asyncio
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
    redis.flushdb()
    return redis

# @pytest.mark.skip(reason="counter")
def test_client_save_to_redis_success_with_ssl(redis):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.load_verify_locations("client.crt")

    client = ssl_context.wrap_socket(
        socket.socket(socket.AF_INET, socket.SOCK_STREAM),
        server_hostname='localhost'
    )
    client.connect(('localhost', 3333))

    key = "psql-1"
    value = 3

    client.send(pickle.dumps((key, value)))
    client.close()

    actual = redis.get(key)
    assert str(actual) == str(value)

@pytest.mark.skip()
def test_refuse_client_without_ssl(redis):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 3333))
    client.send(b'Ping')
    client.close()

    assert len(redis.keys()) == 0

@pytest.mark.skip()
def test_refuse_client_by_autosigned_ssl(redis):
    ssl_context = ssl.create_default_context()
    client = ssl_context.wrap_socket(
        socket.socket(), server_hostname='localhost'
    )

    with pytest.raises(ssl.SSLCertVerificationError):
        client.connect(('localhost', 3333))
        client.send(b'Ping')
        client.close()

    assert len(redis.keys()) == 0


# pytest --disable-warnings

# Test in console
# import socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(('localhost', 3333))