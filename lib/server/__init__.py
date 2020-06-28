import jwt, asyncio, websockets, threading

from lib import params

async def _srv(ws: websockets.server.WebSocketServerProtocol, path: str) -> None:
    print(f'< {await ws.recv()}')
    await ws.send('Hello World!')

def __start(l: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(l)
    l.run_until_complete(websockets.serve(_srv, params.HOST, params.PORT))
    l.run_forever()

def start() -> None:
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=__start, args=(loop,), daemon=True)
    t.start()