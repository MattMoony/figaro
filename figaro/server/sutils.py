"""Utility functions for communicating via websockets"""

import json
import websockets
from typing import Optional

async def send(ws: websockets.server.WebSocketServerProtocol, success: bool, msg: str, rid: Optional[str] = None, **kwargs) -> None:
    """
    Sends a message via the websocket understandable to a Figaro client.
    """
    await ws.send(json.dumps({
        'success': success,
        'msg': msg,
        'rid': rid,
        **kwargs,
    }))

async def success(ws: websockets.server.WebSocketServerProtocol, msg: str, rid: Optional[str] = None, **kwargs) -> None:
    """
    Sends a success-message via a websocket
    """
    await send(ws, True, msg, rid, **kwargs)

async def error(ws: websockets.server.WebSocketServerProtocol, msg: str, rid: Optional[str] = None, **kwargs) -> None:
    """
    Sends an error/fail message via a websocket.
    """
    await send(ws, False, msg, rid, **kwargs)
