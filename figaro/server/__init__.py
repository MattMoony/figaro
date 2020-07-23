"""The entry point for the websocket server"""

import jwt, asyncio, websockets, threading, json, os, hashlib, datetime, sys, time, struct, secrets, base64
import numpy as np
import pash.shell
from io import StringIO
from getpass import getpass
from typing import Dict, Any

from figaro import params, utils
from figaro.channel import Channel
from figaro.server.models.user import User

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
        tkn = jwt.decode(req['tkn'], conf['secret'], algorithms=['HS256'], options={'require': ['exp', 'uname',]})
        return bool(User.load(tkn['uname']))
    # except (jwt.ExpiredSignatureError, jwt.InvalidAlgorithmError, jwt.InvalidSignatureError, KeyError) as e:
    except Exception:
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

async def send_sounds(ws: websockets.server.WebSocketServerProtocol):
    """
    Regularly sends the currently running sounds.
    """
    while True:
        try:
            await ws.send(json.dumps(list(map(lambda s: s.toJSON(), ch.get_sounds()))))
        except websockets.exceptions.ConnectionClosed:
            return
        await asyncio.sleep(0.1)

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
                if req['cmd'] == 'auth':
                    u = User.load(req['uname'])
                    if not u:
                        await ws.send(json.dumps({
                            'success': False,
                            'msg': 'Unknown user!',
                            'rid': rid,
                        }))
                        continue
                    if u.verify(req['pwd']):
                        await ws.send(json.dumps({
                            'success': True,
                            'tkn': jwt.encode({
                                    'uname': u.uname, 
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
                                }, conf['secret'], algorithm='HS256').decode(),
                            'rid': rid,
                        }))
                    else:
                        await ws.send(json.dumps({
                            'success': False,
                            'msg': 'Wrong password provided!',
                            'rid': rid,
                        }))
                    continue
                if req['cmd'] == 'auth-status':
                    await ws.send(json.dumps({
                        'success': True,
                        'logged_in': verify_tkn(req),
                        'rid': rid,
                    }))
                    continue
                if not verify_tkn(req):
                    await ws.send(json.dumps({
                        'success': False,
                        'msg': 'Authentication failed!',
                        'rid': rid,
                    }))
                if req['cmd'] == 'get-conf':
                    await ws.send(json.dumps({
                        'success': True,
                        'BUF': params.BUF,
                        'SMPRATE': params.SMPRATE,
                        'CHNNLS': params.CHNNLS,
                        'rid': rid,
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
                if req['cmd'] == 'get-sounds':
                    asyncio.ensure_future(send_sounds(ws))
                    continue
                stdout = sys.stdout
                sys.stdout = cmdout = StringIO()
                sh.parse(req['cmd'].strip() + ' --json')
                sys.stdout = stdout
                try:
                    out = json.loads(cmdout.getvalue())
                except json.decoder.JSONDecodeError:
                    await ws.send(json.dumps({
                        'success': False,
                        'msg': 'Internal Server Error!',
                        'rid': rid,
                    }))
                    continue
                await ws.send(json.dumps({
                    'success': 'error' not in out.keys(),
                    'msg': out['error'] if 'error' in out.keys() else None,
                    'rid': rid,
                    **{k: v for k, v in out.items() if k != 'error'},
                }))
            except KeyError as e:
                await ws.send(json.dumps({
                    'success': False,
                    'msg': 'Internal Server Error!',
                    'rid': rid,
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
        secret = base64.b64encode(secrets.token_bytes(secret_len//8)).decode()
        f.write(json.dumps(dict(secret=secret)))
        with open(os.path.join(params.BPATH, 'figaro', 'gui', '.tkn'), 'w') as o:
            root = User.load_root()
            o.write(jwt.encode({ 'uname': root.uname, }, secret, algorithm='HS256').decode())

def start(shell: pash.shell.Shell, channel: Channel) -> None:
    """
    Starts the server; starts listening for websocket connections
    """
    global conf, sh, ch
    with open(os.path.join(params.BPATH, 'figaro', 'server', 'conf.json')) as f:
        conf = json.load(f)
    sh = shell
    ch = channel
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=__start, args=(loop,), daemon=True)
    t.start()