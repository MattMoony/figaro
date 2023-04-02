"""
Handles requests related to audio/sound updates from websockets.
"""

import asyncio
import json
import struct
from typing import Any, Dict

import websockets
import websockets.server

from figaro.channel import Channel
from figaro.server import sutils


async def send_audio(ws: websockets.server.WebSocketServerProtocol, ch: Channel, scale: float) -> None:
    """
    Regularly sends the raw audio data to be displayed.

    Args:
        ws: The websocket to send the data to.
        ch: The channel to get the data from.
        scale: The scale to be applied to the data.
    """
    while True:
        try:
            buff = ch.buff * scale
            await ws.send(struct.pack('f'*len(buff), *buff))
        except websockets.exceptions.ConnectionClosed:
            return
        await asyncio.sleep(0.05)

async def send_sounds(ws: websockets.server.WebSocketServerProtocol, ch: Channel) -> None:
    """
    Regularly sends the currently running sounds.

    Args:
        ws: The websocket to send the data to.
        ch: The channel to get the data from.
    """
    while True:
        try:
            await ws.send(json.dumps(list(map(lambda s: s.toJSON(), ch.get_sounds()))))
        except websockets.exceptions.ConnectionClosed:
            return
        await asyncio.sleep(0.1)

async def get_audio(ws: websockets.server.WebSocketServerProtocol, key: bytes, req: Dict[str, Any], 
                    rid: str, ch: Channel) -> None:
    """
    Handles a request to send periodical audio info coming from a websocket.

    Args:
        ws (websockets.server.WebSocketServerProtocol): The websocket to send the data to.
        key (bytes): The key of the websocket.
        req (Dict[str, Any]): The request data.
        rid (str): The request id.
        ch (Channel): The channel to get the data from.
    """
    if 'scale' not in req.keys():
        await sutils.error(ws, key, 'Missing parameter `scale`!')
        return
    asyncio.ensure_future(send_audio(ws, ch, req['scale']))

async def get_sounds(ws: websockets.server.WebSocketServerProtocol, key: bytes, req: Dict[str, Any], 
                     rid: str, ch: Channel) -> None:
    """
    Handles a request to send periodical sound info coming from a websocket.

    Args:
        ws (websockets.server.WebSocketServerProtocol): The websocket to send the data to.
        key (bytes): The key of the websocket.
        req (Dict[str, Any]): The request data.
        rid (str): The request id.
        ch (Channel): The channel to get the data from.
    """
    asyncio.ensure_future(send_sounds(ws, ch))
