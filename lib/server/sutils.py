"""Utility functions for communicating via websockets"""

import json
import secrets
import websockets, websockets.server
from base64 import b64encode
from Crypto.Cipher import AES
from typing import Optional

async def send(ws: websockets.server.WebSocketServerProtocol, key: bytes, success: bool, msg: str, rid: Optional[str] = None, **kwargs) -> None:
    """
    Sends a message via the websocket understandable to a Figaro client.
    """
    cipher: AES = AES.new(key, AES.MODE_GCM, nonce=secrets.token_bytes(12))
    c: bytes = cipher.encrypt(json.dumps({
                    'success': success,
                    'msg': msg,
                    'rid': rid,
                    **kwargs, }).encode())
    await ws.send(b64encode(cipher.nonce + cipher.digest() + c))

async def success(ws: websockets.server.WebSocketServerProtocol, key: bytes, msg: str, rid: Optional[str] = None, **kwargs) -> None:
    """
    Sends a success-message via a websocket
    """
    await send(ws, key, True, msg, rid, **kwargs)

async def error(ws: websockets.server.WebSocketServerProtocol, key: bytes, msg: str, rid: Optional[str] = None, **kwargs) -> None:
    """
    Sends an error/fail message via a websocket.
    """
    await send(ws, key, False, msg, rid, **kwargs)
