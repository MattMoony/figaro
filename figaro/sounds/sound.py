"""
Wrapper class for a playable audio file.
"""

import os
from subprocess import Popen, PIPE
from typing import Any, Dict

from figaro import params

try:
    Popen(['ffmpeg',], stdout=PIPE, stderr=PIPE)
except FileNotFoundError:
    os.environ['PATH'] = os.environ['PATH'] + ';' + os.path.abspath(os.path.join(params.BPATH, 'static'))

import pydub as pyd


class Sound:
    """
    Wrapper for a playable audio file.
    """

    audio: pyd.AudioSegment
    """The actual audio source."""
    amp: float
    """How much the sound should be amplified."""
    format: str
    """The audio file's format string (16 bit int. = 'h', etc.)."""
    f_size: int
    """The format's size in bytes."""
    srate: int
    """The sampling rate."""
    name: str
    """A name for the sound."""
    nframes: int
    """The number of frames in the file."""
    _pos: int
    """The position in the audio file (the reading position)."""

    def __init__(self, fname: str, amp: float = 1.) -> None:
        """
        Initialize a new sound.
        """
        with open(fname, 'rb') as f:
            self.audio: pyd.AudioSegment = pyd.AudioSegment.from_file(f)
        self.audio = self.audio.set_frame_rate(params.SMPRATE).set_channels(params.CHNNLS)
        self.amp: float = amp
        self.f_size: int = self.audio.sample_width
        self.format: str = self.get_format(self.f_size)
        self.srate: int = self.audio.frame_rate
        self.name: str = os.path.basename(fname)
        self.nframes: int = self.audio.frame_count()
        self._pos: int = 0
        # print(self.f_size, self.format, self.srate, str(self))

    def get_format(self, sampwidth: int) -> str:
        """
        Get the struct letter for a given pyaudio format code.
        
        Args:
            sampwidth (int): The pyaudio format code.

        Returns:
            str: The struct letter.
        """
        codes = { 1: 'b', 2: 'h', 4: 'i', }
        return codes[sampwidth] if sampwidth in codes.keys() else ''

    def read(self, buff_s: int) -> bytes:
        """
        Reads `buff_s` frames from the wave object.
        
        Args:
            buff_s (int): The number of frames to read.

        Returns:
            bytes: The read frames.
        """
        self.nframes -= buff_s
        data = self.audio.raw_data[self._pos:self._pos+buff_s*self.f_size]
        self._pos += buff_s*self.f_size
        return data

    def get_playtime(self) -> str:
        """
        Gets the remaining playtime as a string.
        
        Returns:
            str: The remaining playtime.
        """
        s = self.nframes/self.srate
        return f'{int(s//60):02d}:{s%60:05.2f}'

    def get_totalplaytime(self) -> str:
        """
        Gets the total playtime as a string.
        
        Returns:
            str: The total playtime.
        """
        s = self.audio.frame_count()/self.srate
        m = s//60
        s %= 60
        return '{:02d}:{:05.2f}'.format(m, s)

    def toJSON(self) -> Dict[str, Any]:
        """
        Gets the sound into a JSON-compatible format.
        
        Returns:
            Dict[str, Any]: The sound as a JSON-compatible dict.
        """
        return dict(name=self.name, cuplay=(self.audio.frame_count()-self.nframes)/self.srate, maxplay=self.audio.frame_count()/self.srate)

    def __str__(self) -> str:
        return self.name + ' [' + self.get_playtime() + ']'
