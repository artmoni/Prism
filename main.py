import argparse
import logging
import asyncio
import websockets
from prism import Commander

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logging.getLogger("digi").setLevel(logging.WARNING)  # disable logging for digi module


@asyncio.coroutine
def websocket_on_recv(websocket, shining_path):
    data = yield from websocket.recv()
    print(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Prism')
    parser.add_argument('--com', required=True, help="COM/tty port")
    parser.add_argument('--port', help="Websocket listen port")

    args = parser.parse_args()
    commander = Commander(args.com)

    commander.discover_peer()
    commander.listen_remote_event()
    # commander.light_play()

    input()

    # commander.stop_all_task()
