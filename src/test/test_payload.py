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


class Client:
    def __init__(self, name, con):
        self.name = name
        self.con = con

    def send(self):
        payload_min_interval = 0.008

        start_loop = time()
        data = {self.name: 1}
        self.con.send(pickle.dumps(data))
        print(self.name + " sent")
        remain_time = time() - start_loop

        if remain_time < payload_min_interval:
            sleep(0.008 - remain_time)

    def close(self):
        self.con.close()


def run(server_hostname, total_client):
    """
    Parameters:
    name (str): Name to be sent in the payload to differentiate among Clients
    """

    clients = []
    ssl_context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH, cafile="../server.crt"
    )
    ssl_context.load_cert_chain('client.crt', 'client.key')

    for num in range(total_client):
        client_name = "CLIENT_" + str(num)
        con = ssl_context.wrap_socket(
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
