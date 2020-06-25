"""A noise filter for audio"""

import numpy as np
from typing import List

from lib.utils import parse_perc
from lib.filters.filter import Filter

class Noise(Filter):
    """
    Adds noise to audio.
    
    Attributes
    ----------
    amp : float 
        The amplitude.

    Methods
    -------
    apply(data: np.ndarray)
        Applies the filter and returns the result.
    """

    def __init__(self, amp: float):
        self.amp: float = amp

    def apply(self, data: np.ndarray) -> np.ndarray:
        return data + (np.random.rand(*data.shape) - .5) * .05 * self.amp

    def __call__(self, data: np.ndarray) -> np.ndarray:
        return self.apply(data)

    def __str__(self) -> str:
        return f'Noise({self.amp*100:.2f}%)'

def start(args: List[str]) -> Noise:
    """Accepts a list of command line arguments and returns the noise filter created from those arguments"""
    args = [a.strip() for a in args if a.strip()]
    if not args:
        raise Exception('Missing parameter <amplitude> ... ')
    return Noise(parse_perc(args[0]))