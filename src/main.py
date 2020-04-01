import asyncio
import logging

from modules.utils import load_conf
from modules.server import Server


def config_log(log_conf):
    log_path = log_conf["filepath"]
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(message)s"
    )


if __name__ == "__main__":
    conf = load_conf()
    config_log(conf["log"])
    server = Server(conf)

    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logging.info("Server is shut down by KeyboardInterrupt")
