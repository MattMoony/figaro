"""A crackling filter for audio"""

import numpy as np
from typing import List, Dict, Any

from lib.utils import parse_perc
from lib.filters.filter import Filter

class Crackle(Filter):
    """
    Adds a crackling effect to audio.
    
    Attributes
    ----------
    fac : float
        How much crackling should be applied.

    Methods
    -------
    apply(data: np.ndarray)
        Applies the filter and returns the result.
    """

    def __init__(self, fac: float):
        self.fac: float = fac

    def apply(self, data: np.ndarray) -> np.ndarray:
        ifac = 1 - .9 * self.fac
        return data.clip(data.min() * ifac, data.max() * ifac) * (.5 / ifac)

    def toJSON(self) -> Dict[str, Any]:
        return dict(name='crackle', fac=self.fac)

    def __call__(self, data: np.ndarray) -> np.ndarray:
        return self.apply(data)

    def __str__(self) -> str:
        return f'Noise({self.fac*100:.2f}%)'

def start(args: List[str]) -> Crackle:
    """Accepts a list of command line arguments and returns the crackle filter created from those arguments"""
    args = [a.strip() for a in args if a.strip()]
    if not args:
        raise Exception('Missing parameter <factor> ... ')
    return Crackle(parse_perc(args[0]))