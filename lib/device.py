"""Extends the pyaudio.Stream class for further info"""

import pyaudio
from typing import Optional

class Device(pyaudio.Stream):
    """
    Extends the pyaudio.Stream class and represents an Audio I/O device.

    ...

    Attributes
    ----------
    indi : Optional[int]
        The input device's index.
    indo : Optional[int]
        The output device's index.
    """

    def __init__(self, pa: pyaudio.PyAudio, rate: int, channels: int, format: int, *args, input_device_index: Optional[int] = None, output_device_index: Optional[int] = None, **kwargs):
        self.indi: Optional[int] = input_device_index
        self.indo: Optional[int] = output_device_index
        super(Device, self).__init__(pa, *args, rate=rate, channels=channels, format=format, *args, input_device_index=input_device_index, output_device_index=output_device_index, **kwargs)
        pa._streams.add(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Device):
            return False
        return (self.indi == other.indi and self.indi) or (self.indo == other.indo and self.indo)

    def __hash__(self) -> int:
        return (1 + self.indi if self.indi else 0) ^ (1 + self.indo if self.indo else 0)