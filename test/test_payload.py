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
import pickle


SERVER_CERT_PATH = "../src/server.crt"


class Client:
    def __init__(self, name, con):
        self.name = name
        self.con = con

    def send(self):
        start_loop = time()
        data = {self.name: 1}
        self.con.send(pickle.dumps(data))
        print(self.name + " sent")

    def close(self):
        self.con.close()


def _get_ssl_context():
    ssl_context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH, cafile=SERVER_CERT_PATH
    )
    ssl_context.load_cert_chain('client.crt', 'client.key')
    return ssl_context


def send_from_multiple_clients(server_hostname, total_client):
    """
    Params:
    server_hostname (str): The server's name that clients send data to
    total_client (int): number of clients that send data to server
    """

    clients = []

    for num in range(total_client):
        client_name = "CLIENT_" + str(num)
        con = _get_ssl_context().wrap_socket(
            socket.socket(), server_hostname=server_hostname
        )
        con.connect((server_hostname, 1191))

        client_name = "CLIENT_" + str(num)
        clients.append(Client(client_name, con))
        print(client_name + " connected")

    start = time()
    for client in clients:
        client.send()
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
