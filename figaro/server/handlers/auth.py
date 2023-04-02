"""
Handles authentication requests from the websocket.
"""

import datetime
from typing import Any, Dict, List

import jwt
import websockets
import websockets.server

from figaro.server import sutils

conf: Dict[str, Any] = {}
"""The configuration needed for authentication"""

async def auth_status(ws: websockets.server.WebSocketServerProtocol, key: bytes, req: Dict[str, Any], 
                      rid: str, *args) -> None:
    """
    Informs about the client about its current authentication status.

    Args:
        ws (websockets.server.WebSocketServerProtocol): The websocket to send the data to.
        key (bytes): The key of the websocket.
        req (Dict[str, Any]): The request data.
        rid (str): The request id.
    """
    await sutils.success(ws, key, None, rid, logged_in=True)

def init(_conf: Dict[str, Any]) -> None:
    """
    Extract the config needed for authentication from the total server config.

    Args:
        _conf (Dict[str, Any]): The total server config.
    """
    global conf
    keys: List[str] = ['secret',]
    conf = { k: v for k, v in _conf.items() if k in keys }
