"""Channels the altered input data to the output devices"""

import struct, time, numpy as np
from threading import Thread, Lock
from typing import Any, List, Dict, Optional

from lib import params
from lib.device import Device
from lib.sounds.sound import Sound
from lib.transformer import Transformer
from lib.filters.filter import Filter

class Channel(Thread):
    """
    The channel between input and output.

    ...

    Attributes
    ----------
    transf : Transformer
        The transformer applied to the input.
    ist : List[Device]
        The input devices.
    ost : List[Device]
        The output devices.
    buff : np.ndarray
        The current buffer.
    filters : List[Filter]
        Filters to be applied.
    sounds : List[Sound]
        Sounds to be played.
    _running : bool
        Is the channel active?
    _ist_mut : Lock
        Mutex for the input stream.
    _ost_mut : Lock
        Mutex for the output streams.
    _sou_mut : Lock
        Mutex for the sounds list.

    Methods
    -------
    ...
    """

    def __init__(self, transf: Optional[Transformer] = None, ist: List[Device] = [], ost: List[Device] = [], 
                 filters: List[Filter] = [], sounds: List[Sound] = [], *args: List[Any], **kwargs: Dict[str, Any]):
        super(Channel, self).__init__(*args, **kwargs)
        self.transf: Transformer = transf or Transformer()
        self.ist: List[Device] = ist
        self.ost: List[Device] = ost
        self.buff: np.ndarray = np.array([])
        self.filters: List[Filter] = filters
        self.sounds: List[Sound] = sounds
        self._running: bool = False
        self._ist_mut: Lock = Lock()
        self._ost_mut: Lock = Lock()
        self._fil_mut: Lock = Lock()
        self._sou_mut: Lock = Lock()

    def start(self):
        """Start the audio channeling process"""
        if not self.ist or not self.ost:
            raise IOError('Missing I/O devices!')
        return super().start()

    def run(self) -> None:
        """Read audio from the input, run it through the transformer and write the result to the output streams"""
        self._running = True
        while self._running:
            self._ist_mut.acquire()
            self.buff = np.zeros(params.BUF)
            for i in self.ist:
                self.buff += np.asarray(struct.unpack('f'*params.BUF, i.read(params.BUF, exception_on_overflow=False)))
            self.buff /= len(self.ist)
            self._ist_mut.release()
            self.buff = self.transf.apply_all(self.buff)
            self._fil_mut.acquire()
            for f in self.filters:
                self.buff = f(self.buff)
            self._fil_mut.release()
            self._sou_mut.acquire()
            dels = []
            for i, s in enumerate(self.sounds):
                so_raw = s.read(params.BUF)
                if so_raw == b'':
                    dels.append(i)
                    continue
                so = np.asarray(struct.unpack(s.format*(len(so_raw)//s.f_size), so_raw)).astype(np.float32)
                so /= 2**(8*s.f_size-1)
                so = np.hstack((so, np.zeros(params.BUF-len(so))))*s.amp
                self.buff = np.average([self.buff, so], axis=0, weights=[.8,.2])
            for d in reversed(dels):
                del self.sounds[d]
            self._sou_mut.release()
            raw = struct.pack('f'*len(self.buff), *self.buff)
            self._ost_mut.acquire()
            for o in self.ost:
                o.write(raw)
            self._ost_mut.release()

    def add_ist(self, i: Device) -> None:
        """Add an input device"""
        self._ist_mut.acquire()
        if i in self.ist:
            self._ist_mut.release()
            raise Exception("Input Stream is already being used!")
        self.ist.append(i)
        self._ist_mut.release()

    def get_ists(self) -> List[Device]:
        """Get all input devices"""
        self._ist_mut.acquire()
        cp = list(self.ist)
        self._ist_mut.release()
        return cp

    def del_ist(self, dev_ind: int) -> None:
        """Remove an input device"""
        self._ist_mut.acquire()
        if dev_ind not in map(lambda d: d.indi, self.ist):
            self._ist_mut.release()
            raise Exception("Input Stream isn't being used!")
        self.ist = list(filter(lambda i: i.indi != dev_ind, self.ist))
        if not self.ist:
            self.kill()
        self._ist_mut.release()

    def add_ost(self, o: Device) -> None:
        """Add an output device"""
        self._ost_mut.acquire()
        if o in self.ost:
            self._ost_mut.release()
            raise Exception("Output Stream is already being used!")
        self.ost.append(o)
        self._ost_mut.release()

    def get_osts(self) -> List[Device]:
        """Get all output devices"""
        self._ost_mut.acquire()
        cp = list(self.ost)
        self._ost_mut.release()
        return cp

    def del_ost(self, dev_ind: int) -> None:
        """Remove an output device"""
        self._ost_mut.acquire()
        if dev_ind not in map(lambda d: d.indo, self.ost):
            self._ost_mut.release()
            raise Exception("Output Stream isn't being used!")
        self.ost = list(filter(lambda o: o.indo != dev_ind, self.ost))
        if not self.ost:
            self.kill()
        self._ost_mut.release()

    def kill(self) -> None:
        """Stop channeling audio"""
        self._sou_mut.acquire()
        self.sounds = []
        self._sou_mut.release()
        self._running = False

    def kill_all(self) -> None:
        """Stop all audio channels"""
        for i in self.ist:
            i.stop_stream()
            i.close()
        for o in self.ost:
            o.stop_stream()
            o.close()

    def add_filter(self, fil: Filter) -> None:
        """Add a filter to the channel"""
        self._fil_mut.acquire()
        self.filters.append(fil)
        self._fil_mut.release()

    def get_filters(self) -> List[Filter]:
        """Get all currently applied filters"""
        self._fil_mut.acquire()
        cp = list(self.filters)
        self._fil_mut.release()
        return cp

    def del_filter(self, i: int) -> None:
        """Stop a filter that's currently applied"""
        self._fil_mut.acquire()
        del self.filters[i]
        self._fil_mut.release()

    def del_all_filters(self) -> None:
        """Stop all currently applied filters"""
        self._fil_mut.acquire()
        # self.filters = []
        for i in range(len(self.filters)-1, -1, -1):
            del self.filters[i]
        self._fil_mut.release()

    def add_sound(self, sound: Sound) -> None:
        """Add a sound effect to the channel"""
        self._sou_mut.acquire()
        self.sounds.append(sound)
        self._sou_mut.release()

    def get_sounds(self) -> List[Sound]:
        """Get all currently playing soundeffects"""
        self._sou_mut.acquire()
        cp = list(self.sounds)
        self._sou_mut.release()
        return cp

    def del_sound(self, i: int) -> None:
        """Stop a sound effect that's currently running"""
        self._sou_mut.acquire()
        del self.sounds[i]
        self._sou_mut.release()

    def del_all_sounds(self) -> None:
        """Stop all currently running sound effects"""
        self._sou_mut.acquire()
        # self.sounds = []
        for i in range(len(self.sounds)-1, -1, -1):
            del self.sounds[i]
        self._sou_mut.release()

    def is_running(self) -> bool:
        """Returns `True` if the channel is currently active"""
        return self._running

    def __str__(self):
        """Returns a string representation of the channel"""
        return 'Channel: {{{}}} --> {{{}}} | {} ... '.format(
                ', '.join(sorted([str(i.indi) for i in self.ist])) if self.ist else '-', 
                ', '.join(sorted([str(o.indo) for o in self.ost])) if self.ost else '-', 
                'running' if self._running else 'stopped')