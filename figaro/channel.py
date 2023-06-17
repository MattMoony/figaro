"""
Channels the altered input data to the output devices.
"""

import struct
from multiprocessing import Event, Manager, Process
from multiprocessing.managers import ListProxy
from typing import List, Optional

import numpy as np

from figaro import params
from figaro.device import Device
from figaro.filters.filter import Filter
from figaro.sounds.sound import Sound
from figaro.transformer import Transformer


class Channel:
    """
    The channel between input and output.
    """
    
    trf: Transformer
    """The transformer applied to the input."""
    buf: np.ndarray
    """The current buffer."""

    inputs: ListProxy[Device]
    """The input devices."""
    outputs: ListProxy[Device]
    """The output devices."""
    filters: ListProxy[Filter]
    """Filters to be applied."""
    sounds: ListProxy[Sound]
    """Sounds to be played."""

    __dead: Event
    """Indicates whether the channel is dead."""
    __mgr: Manager
    """The manager used to create the proxies."""
    __p: Process
    """The process running the channel."""

    def __init__(self, trf: Optional[Transformer] = None, inputs: Optional[List[Device]] = None,
                 outputs: Optional[List[Device]] = None, filters: Optional[List[Filter]] = None,
                    sounds: Optional[List[Sound]] = None) -> None:
        """
        Initialize a new Channel object.

        Args:
            trf (Optional[Transformer]): The transformer to be applied to the input.
            inputs (List[Device]): The input devices. Default is [].
            outputs (List[Device]): The output devices. Default is [].
            filters (List[Filter]): The filters to be applied. Default is [].
            sounds (List[Sound]): The sounds to be played. Default is [].
        """
        self.__mgr = Manager()
        self.__dead = self.__mgr.Event()

        self.trf = trf or Transformer()
        self.buf = np.array([])
        self.inputs = self.__mgr.list(inputs or [])
        self.outputs = self.__mgr.list(outputs or [])
        self.filters = self.__mgr.list(filters or [])
        self.sounds = self.__mgr.list(sounds or [])

    def start(self) -> None:
        """
        Start the channel.

        Raises:
            IOError: If the channel is already running.
        """
        if not self.__dead.set():
            raise IOError('Channel is already running')
        self.__dead.clear()
        self.__p = Process(target=self.__run)
        self.__p.start()

    def stop(self) -> None:
        """
        Stop the channel.

        Raises:
            IOError: If the channel is not running.
        """
        if self.__dead.set():
            raise IOError('Channel is not running')
        self.__dead.set()
        self.__p.join()

    def __run(self) -> None:
        """
        Read audio from the input streams, run it through the 
        transformer and write the result to the output streams.
        """
        while not self.__dead.is_set():
            self.__read()
            self.__transform()
            self.__write()

    def __read(self) -> None:
        """
        Read audio from the input streams.
        """
        self.buf = np.zeros(params.BUF)
        n: int = 0
        for inp in self.inputs:
            self.buf += np.asarray(struct.unpack('f'*params.BUF, inp.read(params.BUF, exception_on_overflow=False)))
            n += 1
        self.buf /= n   # probably better due to parallelism

    def __transform(self) -> None:
        """
        Transform the input - i.e. run it through the
        transform, add sound effects, etc.
        """
        self.buf = self.trf.apply_all(self.buf)
        for f in self.filters:
            self.buf = f(self.buf)
        for s in reversed(self.sounds):
            raw = s.read(params.BUF)
            if raw == b'':
                self.sounds.remove(s)
                continue
            raw = so = np.asarray(struct.unpack(s.format*(len(raw)//s.f_size), raw)).astype(np.float32)
            raw /= 2**(8*s.f_size-1)
            raw = np.hstack((so, np.zeros(params.BUF-len(so))))*s.amp
            self.buf = np.average([self.buf, raw,], axis=0, weights=[.8, .2,])

    def __write(self) -> None:
        """
        Write the result to the output streams.
        """
        raw = struct.pack('f'*len(self.buf), *self.buf)
        for out in self.outputs:
            out.write(raw)
