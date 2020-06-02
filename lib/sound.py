"""Wrapper class for a playable wave file"""

from wave import Wave_read
from typing import Tuple

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
    f_size : str
        The format's size in bytes.

    Methods
    -------
    get_format(fcode)
        Returns the format string and size for a pyaudio format code.
    read(buff_s)
        Reads from the wave object.
    """

    def __init__(self, wf: Wave_read, fcode: int):
        self.wf: Wave_read = wf
        self.format: str; self.f_size: int
        self.format, self.f_size = self.get_format(fcode)
        if not self.format:
            raise Exception('Unknown format code!')

    def get_format(self, fcode: int) -> Tuple[str, int]:
        """Get the struct letter for a given pyaudio format code"""
        codes = { 1: ('f', 4), 8: ('h', 2), 2: ('d', 4), }
        return codes[fcode] if fcode in codes.keys() else ''

    def read(self, buff_s: int) -> bytes:
        """Reads from the wave object"""
        return self.wf.readframes(buff_s)