"""The entry point for the websocket server"""

import jwt, asyncio, websockets, threading, json, os, hashlib
from io import StringIO
from getpass import getpass
from typing import Dict, Any

from lib import params, utils
from lib.server.models.user import User

conf: Dict[str, Any] = dict()

async def _srv(ws: websockets.server.WebSocketServerProtocol, path: str) -> None:
    """
    Actually dispatch the websocket-requests.
    """
    try:
        req = json.loads(await ws.recv())
    except json.decoder.JSONDecodeError:
        return
    if path.lower() == '/auth':
        try:
            u = User.load(req['uname'])
            if u.verify(req['pwd']):
                await ws.send(json.dumps({
                    'success': True,
                    'token': jwt.encode({'uname': u.uname,}, conf['secret'], algorithm='HS256').decode(),
                }))
            else:
                await ws.send(json.dumps({
                    'success': False,
                    'msg': 'Wrong password provided!',
                }))
        except KeyError as e:
            await ws.send(json.dumps({
                'success': False,
                'msg': 'Internal Server Error!',
            }))

def __start(l: asyncio.AbstractEventLoop) -> None:
    """
    Start the websocket-request-polling on a separate thread.
    """
    asyncio.set_event_loop(l)
    l.run_until_complete(websockets.serve(_srv, params.HOST, params.PORT))
    l.run_forever()

def create_conf_prompt() -> None:
    """
    Prompt the user to create a config file.
    """
    with open(os.path.join(params.BPATH, 'lib', 'server', 'conf.json'), 'w') as f:
        while True:
            secret = getpass('Enter a new secret: ')
            if getpass('Confirm new secret: ') == secret:
                break
            utils.printerr('Secrets don\'t match!')
        f.write(json.dumps(dict(secret=hashlib.sha256(secret.encode()).hexdigest())))

def start() -> None:
    """
    Starts the server; starts listening for websocket connections
    """
    global conf
    with open(os.path.join(params.BPATH, 'lib', 'server', 'conf.json')) as f:
        conf = json.load(f)
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=__start, args=(loop,), daemon=True)
    t.start()