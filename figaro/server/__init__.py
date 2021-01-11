"""The entry point for the websocket server"""

import jwt, asyncio, websockets, threading, json, os, hashlib, sys, time, secrets, base64
import numpy as np
import pash.shell
from io import StringIO
from getpass import getpass
from typing import Dict, Any, Callable

from figaro import params, utils
from figaro.server import sutils
from figaro.channel import Channel
from figaro.server.handlers import auth, audio, config
from figaro.server.models.user import User

"""The configuration of the websocket server"""
conf: Dict[str, Any] = dict()
"""The main CLI shell"""
sh: pash.shell.Shell = None
"""The main audio channel"""
ch: Channel = None

"""Special unauthenticated websockets commands"""
noauth_cmds: Dict[str, Callable[[websockets.server.WebSocketServerProtocol, Dict[str, Any], str, Dict[str, Any]], None]] = {
    'auth': auth.auth,
    'auth-status': auth.auth_status,
}

"""Special authenticated websockets commands"""
auth_cmds: Dict[str, Callable[[websockets.server.WebSocketServerProtocol, Dict[str, Any], str, Channel], None]] = {
    'get-conf': config.get_conf,
    'get-audio': audio.get_audio,
    'get-sounds': audio.get_sounds,
}

async def _srv(ws: websockets.server.WebSocketServerProtocol, path: str) -> None:
    """
    Actually dispatch the websocket-requests.
    """
    try:
        async for req in ws:
            try:
                req = json.loads(req)
            except json.decoder.JSONDecodeError:
                continue
            try:
                rid = ''
                if 'timestamp' in req.keys():
                    rid = base64.b64encode((req['cmd'] + str(req['timestamp'])).encode()).decode()
                if req['cmd'] in noauth_cmds.keys():
                    await noauth_cmds[req['cmd']](ws, req, rid)
                    continue
                if not auth.verify_tkn(req):
                    await sutils.error(ws, 'Authentication failed!', rid)
                    continue
                if req['cmd'] in auth_cmds.keys():
                    await auth_cmds[req['cmd']](ws, req, rid, ch)
                    continue
                stdout = sys.stdout
                sys.stdout = cmdout = StringIO()
                sh.parse(req['cmd'].strip() + ' --json')
                sys.stdout = stdout
                try:
                    out = json.loads(cmdout.getvalue())
                except json.decoder.JSONDecodeError:
                    await sutils.error(ws, 'Internal Server Error!', rid)
                    continue
                await sutils.send(ws,
                                  'error' not in out.keys(), 
                                  out['error'] if 'error' in out.keys() else None, 
                                  rid, 
                                  **{k: v for k, v in out.items() if k != 'error'})
            except KeyError as e:
                await sutils.error(ws, 'Internal Server Error!', rid)
    except websockets.exceptions.ConnectionClosed:
        return

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
    with open(os.path.join(params.BPATH, 'figaro', 'server', 'conf.json'), 'w') as f:
        while True:
            secret_len = input('Enter secret length [default 512 (bits)]: ')
            if not secret_len.strip():
                secret_len = 512
            else:
                try:
                    secret_len = int(secret_len)
                    if secret_len % 8 != 0:
                        utils.printwrn('No. bits should be divisible by 8 ... ')
                        continue
                except ValueError:
                    utils.printerr('Enter a valid number!')
                    continue
            break
        secret = secrets.token_bytes(secret_len//8)
        f.write(json.dumps(dict(secret=base64.b64encode(secret).decode())))
        with open(os.path.join(params.BPATH, 'figaro', 'gui', '.tkn'), 'w') as o:
            root = User.load_root()
            o.write(jwt.encode({ 'uname': root.uname, }, secret, algorithm='HS256').decode())

def load_conf() -> None:
    """
    Loads the config and decodes values where needed.
    """
    global conf
    with open(os.path.join(params.BPATH, 'figaro', 'server', 'conf.json')) as f:
        conf = json.load(f)
        conf['secret'] = base64.b64decode(conf['secret'])
        auth.init(conf)

def start(shell: pash.shell.Shell, channel: Channel) -> None:
    """
    Starts the server; starts listening for websocket connections
    """
    global sh, ch
    load_conf()
    sh = shell
    ch = channel
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=__start, args=(loop,), daemon=True)
    t.start()
