"""Handles authentication requests from the websocket"""

import jwt
import datetime
import websockets, websockets.server
from typing import Dict, Any, List

from lib.server import sutils

"""The configuration needed for authentication"""
conf: Dict[str, Any] = dict()

async def auth_status(ws: websockets.server.WebSocketServerProtocol, key: bytes, req: Dict[str, Any], rid: str, *args) -> None:
    """
    Informs about the client about its current authentication status.
    """
    await sutils.success(ws, key, None, rid, logged_in=True)

def init(_conf: Dict[str, Any]) -> None:
    """
    Extract the config needed for authentication from the total server config.
    """
    global conf
    keys: List[str] = ['secret',]
    conf = { k: v for k, v in _conf.items() if k in keys }
