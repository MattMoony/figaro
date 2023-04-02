"""
Utility functions for communicating via websockets.
"""

import json
import secrets
from base64 import b64encode
from typing import Optional

import websockets
import websockets.server
from Crypto.Cipher import AES


async def send(ws: websockets.server.WebSocketServerProtocol, key: bytes, success: bool, msg: str, 
               rid: Optional[str] = None, **kwargs) -> None:
    """
    Sends a message via the websocket understandable to a Figaro client.

    Args:
        ws (websockets.server.WebsocketServerProtocol): The websocket to send the data to.
        key (bytes): The key of the websocket.
        success (bool): Whether the request was successful or not.
        msg (str): The message to send.
        rid (Optional[str]): The request id.
    """
    cipher: AES = AES.new(key, AES.MODE_GCM, nonce=secrets.token_bytes(12))
    c: bytes = cipher.encrypt(json.dumps({
                    'success': success,
                    'msg': msg,
                    'rid': rid,
                    **kwargs, }).encode())
    await ws.send(b64encode(cipher.nonce + cipher.digest() + c))

async def success(ws: websockets.server.WebSocketServerProtocol, key: bytes, msg: str, 
                  rid: Optional[str] = None, **kwargs) -> None:
    """
    Sends a success-message via a websocket

    Args:
        ws (websockets.server.WebSocketServerProtocol): The websocket to send the data to.
        key (bytes): The key of the websocket.
        msg (str): The message to send.
        rid (Optional[str]): The request id.
    """
    await send(ws, key, True, msg, rid, **kwargs)

async def error(ws: websockets.server.WebSocketServerProtocol, key: bytes, msg: str, 
                rid: Optional[str] = None, **kwargs) -> None:
    """
    Sends an error/fail message via a websocket.

    Args:
        ws (websockets.server.WebSocketServerProtocol): The websocket to send the data to.
        key (bytes): The key of the websocket.
        msg (str): The message to send.
        rid (Optional[str]): The request id.
    """
    await send(ws, key, False, msg, rid, **kwargs)
