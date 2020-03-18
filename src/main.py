import asyncio
from conf import load_conf


def config_log(log_conf):
    log_path = log_conf.get("filepath", "main.log")
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
        asyncio.run(server.run())
    except KeyboardInterrupt:
        print("Server is shut down by KeyboardInterrupt")
