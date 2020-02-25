# Goal: Make sure this server can handle 100 payload / second
# How to run the test:
# from test_payload import run_client
# run_client("CLIENT_1")
# run_client("CLIENT_2")

import ssl
import socket
from time import time, sleep
import pickle


def run_client(name):
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="../server.crt")
    ssl_context.load_cert_chain('client.crt', 'client.key')

    client = ssl_context.wrap_socket(
        socket.socket(), server_hostname='example.com'
    )

    client.connect(('127.0.0.1', 3333))

    start = time()
    for num in range(100):
        start_loop = time()
        key = name + "-" + str(num)
        data = {key: str(num)}
        client.send(pickle.dumps(data))
        print("Send " + str(num))
        sleep(0.005 - (time() - start_loop))
    print("Runtime: " + str(time() - start))
    client.close()
