import asyncio
import logging
import argparse

from modules.utils import load_conf
from modules.server import Server


parser = argparse.ArgumentParser()
parser.add_argument(
    "--loglevel", "-l", type=str, default="ERROR",
    help="The log level (default: ERROR)"
)
parser.add_argument(
    "--logfile", "-f", type=str,
    help="The path to logfile (default: None)"
)


if __name__ == "__main__":
    args = parser.parse_args()
    loglevel = args.loglevel
    logfile = args.logfile

    logging.basicConfig(
        filename=logfile,
        level=loglevel,
        format="%(asctime)s - %(message)s"
    )

    conf = load_conf()
    server = Server(conf)

    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logging.info("Server is shut down by KeyboardInterrupt")
