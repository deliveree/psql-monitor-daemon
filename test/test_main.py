import sys, os
sys.path.append(os.getcwd())

from src.main import run_server
import pytest
import asyncio
import socket
import pickle
import threading
import signal
from redis import Redis


def test_send_successfull():
    def run_test_server():
        asyncio.run(run_server())

    try:
        svr_thread = threading.Thread(target=run_test_server, daemon=True)
        svr_thread.start()

        sock = socket.socket()
        sock.connect(('localhost', 3333))
        sock.send(b'OOKKKKKKKKKKK')
        sock.close()

        coro.close()
        mock.close
        svr_thread.join()
    except Exception as e:
        print(e)
        svr_thread.join()
