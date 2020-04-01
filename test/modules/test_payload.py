"""
This file is used to test maximum load of server
It will create 100 Clients and connect server_hostname. Then each Client will send a dict to server

To run the test, in python console:

from test_payload import run
run(server_hostname, total_client)
"""

import ssl
import socket
from time import time, sleep
from json import dumps

from modules.utils import load_conf
from modules.fake_client import FakeClient as Client


def send_from_multiple_clients(total_client, conf):
    """
    Params:
    server_hostname (str): The server's name that clients send data to
    total_client (int): number of clients that send data to server
    """

    clients = []
    for num in range(total_client):
        client_name = "CLIENT_" + str(num)
        client = Client(conf, client_name)
        client.connect()
        clients.append(client)
        print(client_name + " connected")

    start = time()
    for client in clients:
        data = {client.name: 1}
        client.send(data)
    print("Runtime: " + str(time() - start))

    for client in clients:
        client.close()


def send_from_a_client(server_hostname):
    con = _get_ssl_context().wrap_socket(
        socket.socket(), server_hostname=server_hostname
    )
    con.connect((server_hostname, 1191))

    start = time()
    for num in range(100):
        key = "SINGLE_CLIENT_" + str(num)
        con.send(pickle.dumps({key: str(num)}))
        print("Send :" + str(num))
    print("Runtime: " + str(time() - start))

    con.close()
