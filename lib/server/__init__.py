"""The entry point for the websocket server"""

import jwt, asyncio, websockets, threading, json, os, hashlib, datetime, sys, time, struct
import numpy as np
import pash.shell
from io import StringIO
from getpass import getpass
from typing import Dict, Any

from lib import params, utils
from lib.channel import Channel
from lib.server.models.user import User

"""The configuration of the websocket server"""
conf: Dict[str, Any] = dict()
"""The main CLI shell"""
sh: pash.shell.Shell = None
"""The main audio channel"""
ch: Channel = None

def verify_tkn(req: Dict[str, Any]) -> bool:
    """
    Checks the JWT of the given request for validity.
    """
    try:
        tkn = jwt.decode(req['tkn'], conf['secret'], algorithms=['HS256'])
        return bool(User.load(tkn['uname']))
    except (jwt.ExpiredSignatureError, KeyError) as e:
        return False

async def send_audio(ws: websockets.server.WebSocketServerProtocol, scale: float):
    """
    Regularly sends the raw audio data to be displayed.
    """
    while True:
        try:
            buff = ch.buff * scale
            await ws.send(struct.pack('f'*len(buff), *buff))
        except websockets.exceptions.ConnectionClosed:
            return
        await asyncio.sleep(0.05)

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
                if req['cmd'] == 'auth':
                    u = User.load(req['uname'])
                    if not u:
                        await ws.send(json.dumps({
                            'success': False,
                            'msg': 'Unknown user!'
                        }))
                        continue
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
                if req['cmd'] == 'auth-status':
                    await ws.send(json.dumps({
                        'success': True,
                        'logged_in': verify_tkn(req),
                    }))
                    continue
                if not verify_tkn(req):
                    await ws.send(json.dumps({
                        'success': False,
                        'msg': 'Authentication failed!',
                    }))
                if req['cmd'] == 'get-conf':
                    await ws.send(json.dumps({
                        'success': True,
                        'BUF': params.BUF,
                        'SMPRATE': params.SMPRATE,
                        'CHNNLS': params.CHNNLS
                    }))
                    continue
                if req['cmd'] == 'get-audio':
                    if 'scale' not in req.keys():
                        await ws.send({
                            'success': False,
                            'msg': 'Missing parameter `scale`!',
                        })
                        continue
                    asyncio.ensure_future(send_audio(ws, req['scale']))
                    continue
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
    with open(os.path.join(params.BPATH, 'lib', 'server', 'conf.json'), 'w') as f:
        while True:
            secret = getpass('Enter a new secret: ')
            if getpass('Confirm new secret: ') == secret:
                break
            utils.printerr('Secrets don\'t match!')
        f.write(json.dumps(dict(secret=hashlib.sha256(secret.encode()).hexdigest())))

def start(shell: pash.shell.Shell, channel: Channel) -> None:
    """
    Starts the server; starts listening for websocket connections
    """
    global conf, sh, ch
    with open(os.path.join(params.BPATH, 'lib', 'server', 'conf.json')) as f:
        conf = json.load(f)
    sh = shell
    ch = channel
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=__start, args=(loop,), daemon=True)
    t.start()