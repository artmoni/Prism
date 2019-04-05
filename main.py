import argparse
import logging
import asyncio
import websockets
from prism import Commander

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logging.getLogger("digi").setLevel(logging.WARNING)  # disable logging for digi module

commander = None

@asyncio.coroutine
def websocket_on_recv(websocket, shining_path):
    data = yield from websocket.recv()
    print(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Prism')
    parser.add_argument('--com', required=True, help="COM/tty port")
    parser.add_argument('--port', default=8080, help="Websocket listen port")

    args = parser.parse_args()
    
    commander = Commander(args.com)
    commander.listen_remote()

    tasks = [
        asyncio.ensure_future(commander.discover_peer()),
        asyncio.ensure_future(websockets.serve(websocket_on_recv, 'localhost', args.port))
    ]

    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
    asyncio.get_event_loop().run_forever()