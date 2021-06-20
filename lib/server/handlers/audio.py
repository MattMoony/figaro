"""Handles requests related to audio/sound updates from websockets"""

import json
import struct
import asyncio
import websockets, websockets.server
from typing import Dict, Any

from lib.server import sutils
from lib.channel import Channel

async def send_audio(ws: websockets.server.WebSocketServerProtocol, ch: Channel, scale: float):
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

async def send_sounds(ws: websockets.server.WebSocketServerProtocol, ch: Channel):
    """
    Regularly sends the currently running sounds.
    """
    while True:
        try:
            await ws.send(json.dumps(list(map(lambda s: s.toJSON(), ch.get_sounds()))))
        except websockets.exceptions.ConnectionClosed:
            return
        await asyncio.sleep(0.1)

async def get_audio(ws: websockets.server.WebSocketServerProtocol, key: bytes, req: Dict[str, Any], rid: str, ch: Channel) -> None:
    """
    Handles a request to send periodical audio info coming from a websocket.
    """
    if 'scale' not in req.keys():
        await sutils.error(ws, key, 'Missing parameter `scale`!')
        return
    asyncio.ensure_future(send_audio(ws, ch, req['scale']))

async def get_sounds(ws: websockets.server.WebSocketServerProtocol, key: bytes, req: Dict[str, Any], rid: str, ch: Channel) -> None:
    """
    Handles a request to send periodical sound info coming from a websocket.
    """
    asyncio.ensure_future(send_sounds(ws, ch))
