"""The entry point for the websocket server"""

import jwt, asyncio, websockets, threading, json, os, hashlib, datetime, sys
import pash.shell
from io import StringIO
from getpass import getpass
from typing import Dict, Any

from lib import params, utils
from lib.server.models.user import User

"""The configuration of the websocket server"""
conf: Dict[str, Any] = dict()
"""The main CLI shell"""
sh: pash.shell.Shell = None

def verify_tkn(req: Dict[str, Any]) -> bool:
    """
    Checks the JWT of the given request for validity.
    """
    try:
        tkn = jwt.decode(req['tkn'], conf['secret'], algorithms=['HS256'])
        return bool(User.load(tkn['uname']))
    except KeyError as e:
        return False

async def _srv(ws: websockets.server.WebSocketServerProtocol, path: str) -> None:
    """
    Actually dispatch the websocket-requests.
    """
    while True:
        try:
            req = json.loads(await ws.recv())
        except json.decoder.JSONDecodeError:
            continue
        except websockets.exceptions.ConnectionClosed:
            return
        try:
            if req['cmd'] == 'auth':
                u = User.load(req['uname'])
                if u.verify(req['pwd']):
                    await ws.send(json.dumps({
                        'success': True,
                        'tkn': jwt.encode({
                                'uname': u.uname, 
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
                            }, conf['secret'], algorithm='HS256').decode(),
                    }))
                else:
                    await ws.send(json.dumps({
                        'success': False,
                        'msg': 'Wrong password provided!',
                    }))
                continue
            if not verify_tkn(req):
                await ws.send(json.dumps({
                    'success': False,
                    'msg': 'Verification failed!',
                }))
            stdout = sys.stdout
            sys.stdout = cmdout = StringIO()
            sh.parse(req['cmd'])
            sys.stdout = stdout
            await ws.send(json.dumps({
                'success': True,
                'msg': cmdout.getvalue(),
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

def start(shell: pash.shell.Shell) -> None:
    """
    Starts the server; starts listening for websocket connections
    """
    global conf, sh
    with open(os.path.join(params.BPATH, 'lib', 'server', 'conf.json')) as f:
        conf = json.load(f)
    sh = shell
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=__start, args=(loop,), daemon=True)
    t.start()