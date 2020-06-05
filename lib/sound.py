"""Wrapper class for a playable wave file"""

import wave, os, pyaudio
from typing import Tuple, Optional

class Sound(object):
    """
    Wrapper for a playable wave file
    
    ...

    Attributes
    ----------
    wf : Wave_read
        The raw wave object.
    format : str
        The wave file's format string.
    f_size : int
        The format's size in bytes.
    srate : int
        The sampling rate.
    name : str
        An optional name for the sound.
    nframes : int
        The number of frames in the file.

    Methods
    -------
    get_format(fcode)
        Returns the format string and size for a pyaudio format code.
    read(buff_s)
        Reads from the wave object.
    get_playtime()
        Gets the remaining playtime as a string.
    """

    def __init__(self, fname: str):
        self.wf: wave.Wave_read = wave.open(fname, 'rb')
        self.format: str; self.f_size: int
        self.format, self.f_size = self.get_format(pyaudio.PyAudio().get_format_from_width(self.wf.getsampwidth()))
        self.srate: int = self.wf.getframerate()
        self.name: str = os.path.basename(fname)
        self.nframes: int = self.wf.getnframes()

    def get_format(self, fcode: int) -> Tuple[str, int]:
        """Get the struct letter for a given pyaudio format code"""
        codes = { 1: ('f', 4), 8: ('h', 2), 2: ('d', 4), }
        return codes[fcode] if fcode in codes.keys() else ''

    def read(self, buff_s: int) -> bytes:
        """Reads from the wave object"""
        self.nframes -= buff_s
        return self.wf.readframes(buff_s)

    def get_playtime(self) -> str:
        s = self.nframes/self.srate
        m = int(s/60)
        s %= 60
        return '{:02d}:{:05.2f}'.format(m, s)