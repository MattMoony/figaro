"""
Handles configuration requests from websockets.
"""

from typing import Any, Dict

import websockets
import websockets.server

from figaro import params
from figaro.channel import Channel
from figaro.server import sutils


async def get_conf(ws: websockets.server.WebSocketServerProtocol, key: bytes, req: Dict[str, Any], 
                   rid: str, ch: Channel) -> None:
    """
    Sends predefined configuration parameters via the websocket.

    Args:
        ws (websockets.server.WebSocketServerProtocol): The websocket to send the data to.
        key (bytes): The key of the websocket.
        req (Dict[str, Any]): The request data.
        rid (str): The request id.
        ch (Channel): The channel to get the configuration from.
    """
    await sutils.success(ws, key, None, rid, BUF=params.BUF, SMPRATE=params.SMPRATE, CHNNLS=params.CHNNLS)
