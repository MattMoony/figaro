"""Channels the altered input data to the output devices"""

import struct, time, numpy as np
from threading import Thread, Lock
from typing import Any, List, Dict, Optional

from lib import params
from lib.device import Device
from lib.transformer import Transformer

class Channel(Thread):
    """
    The channel between input and output.

    ...

    Attributes
    ----------
    transf : Transformer
        The transformer applied to the input.
    ist : Optional[Device]
        The input device.
    ost : List[Device]
        The output devices.
    _running : bool
        Is the channel active?
    _ist_mut : Lock
        Mutex for the input stream.
    _ost_mut : Lock
        Mutex for the output streams.
    """

    def __init__(self, transf: Optional[Transformer] = None, ist: Optional[Device] = None, ost: List[Device] = [], 
                 *args: List[Any], **kwargs: Dict[str, Any]):
        super(Channel, self).__init__(*args, **kwargs)
        self.transf: Transformer = transf or Transformer()
        self.ist: Optional[Device] = ist
        self.ost: List[Device] = ost
        self._running: bool = False
        self._ist_mut: Lock = Lock()
        self._ost_mut: Lock = Lock()

    def start(self):
        if not self.ist or not self.ost:
            return
        return super().start()

    def run(self) -> None:
        """Read audio from the input, run it through the transformer and write the result to the output streams"""
        self._running = True
        while self._running:
            self._ist_mut.acquire()
            data = np.asarray(struct.unpack('f'*params.BUF, self.ist.read(params.BUF)))
            self._ist_mut.release()
            data = self.transf.apply_all(data)
            raw = struct.pack('f'*len(data), *data)
            self._ost_mut.acquire()
            for o in self.ost:
                o.write(raw)
            self._ost_mut.release()

    def add_ost(self, o: Device) -> None:
        """Add an output device"""
        self._ost_mut.acquire()
        self.ost.append(o)
        self._ost_mut.release()

    def del_ost(self, dev_ind: int) -> None:
        """Remove an output device"""
        self._ost_mut.acquire()
        self.ost = list(filter(lambda o: o.indo != dev_ind, self.ost))
        self._ost_mut.release()

    def set_ist(self, i: Device) -> None:
        """Set the input device"""
        self._ist_mut.acquire()
        self.ist = i
        self._ist_mut.release()

    def kill(self) -> None:
        """Stop channeling audio"""
        self._running = False

    def kill_all(self) -> None:
        """Stop all audio channels"""
        self.ist.stop_stream()
        self.ist.close()
        for o in self.ost:
            o.stop_stream()
            o.close()

    def __str__(self):
        """Returns a string representation of the channel"""
        return 'Channel: {{{}}} --> {{{}}} | {} ... '.format(self.ist.indi if self.ist else '-', ', '.join([str(o.indo) for o in self.ost]) if self.ost else '-', 'running' if self._running else 'stopped')