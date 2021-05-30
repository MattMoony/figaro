"""Handles configuration requests from websockets"""

import json
import websockets
from typing import Dict, Any

from figaro import params
from figaro.server import sutils
from figaro.channel import Channel

async def get_conf(ws: websockets.server.WebSocketServerProtocol, key: bytes, req: Dict[str, Any], rid: str, ch: Channel) -> None:
    """
    Sends predefined configuration parameters via the websocket.
    """
    await sutils.success(ws, key, None, rid, BUF=params.BUF, SMPRATE=params.SMPRATE, CHNNLS=params.CHNNLS)
