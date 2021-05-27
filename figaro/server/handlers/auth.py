"""Handles authentication requests from the websocket"""

import jwt
import datetime
import websockets
from typing import Dict, Any, List

from figaro.server import sutils
from figaro.server.models.user import User

"""The configuration needed for authentication"""
conf: Dict[str, Any] = dict()

def verify_tkn(req: Dict[str, Any]) -> bool:
    """
    Checks the JWT of the given request for validity.
    """
    try:
        # tkn = jwt.decode(req['tkn'], conf['secret'], algorithms=['HS256'], options={'require': ['exp', 'uname',]})
        tkn = jwt.decode(req['tkn'], conf['secret'], algorithms=['HS256'], options={'require': ['uname',]})
        return bool(User.load(tkn['uname']))
    # except (jwt.ExpiredSignatureError, jwt.InvalidAlgorithmError, jwt.InvalidSignatureError, KeyError) as e:
    except Exception:
        return False

async def auth(ws: websockets.server.WebSocketServerProtocol, req: Dict[str, Any], rid: str) -> None:
    """
    Handles a user authentication request coming from a websocket.
    """
    u = User.load(req['uname'])
    if not u:
        await sutils.error(ws, 'Unknown user!', rid)
        return
    if u.verify(req['pwd']):
        await sutils.success(ws, None, rid, tkn=jwt.encode({
                                'uname': u.uname, 
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
                            }, conf['secret'], algorithm='HS256'))
    else:
        await sutils.error(ws, 'Wrong password provided!', rid)

async def auth_status(ws: websockets.server.WebSocketServerProtocol, req: Dict[str, Any], rid: str) -> None:
    """
    Informs about the client about its current authentication status.
    """
    await sutils.success(ws, None, rid, logged_in=verify_tkn(req))

def init(_conf: Dict[str, Any]) -> None:
    """
    Extract the config needed for authentication from the total server config.
    """
    global conf
    keys: List[str] = ['secret',]
    conf = { k: v for k, v in _conf.items() if k in keys }
