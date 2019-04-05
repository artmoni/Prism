import argparse
import logging
import asyncio
import websockets
from prism import Commander

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logging.getLogger("digi").setLevel(logging.WARNING)  # disable logging for digi module


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Prism')
    parser.add_argument('--com', required=True, help="COM/tty port")
    parser.add_argument('--port', default=8080, help="Websocket listen port")

    args = parser.parse_args()
    
    commander = Commander(args.com)

    loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def websocket_on_recv(websocket, shining_path):

        def success():
            logging.info("SUCESSFULLY IDENT")
            asyncio.set_event_loop(loop)
            asyncio.run_coroutine_threadsafe(websocket.send("OK"),  asyncio.get_event_loop())
        
        def error():
            logging.warn("WRONG CODE")
            asyncio.set_event_loop(loop)
            asyncio.run_coroutine_threadsafe(websocket.send("ER"),  asyncio.get_event_loop())

        commander.set_on_success(success)
        commander.set_on_error(error)
        data = yield from websocket.recv()

    commander.listen_remote()

    tasks = [
        #asyncio.ensure_future(commander.discover_peer()),
        asyncio.ensure_future(websockets.serve(websocket_on_recv, 'localhost', args.port))
    ]

    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
    asyncio.get_event_loop().run_forever()