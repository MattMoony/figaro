"""Filter to add a trippy sound effect"""

import numpy as np, re
from typing import List, Dict, Any

from lib.utils import parse_perc
from lib.filters.filter import Filter

class Trip(Filter):
    """
    Adds a trippy effect to audio.
    
    ...

    Attributes
    ----------
    scale : float
        How much the echo gets damped on each iteration.

    Methods
    -------
    apply(data: np.ndarray)
        Applies the filter and returns the result.
    """

    def __init__(self, scale: float):
        self.scale: float = scale
        self._prev: np.ndarray = None

    def apply(self, data: np.ndarray) -> np.ndarray:
        if self._prev is None:
            self._prev = np.zeros(data.shape)
        data, self._prev = data + self._prev, self._prev * self.scale + data
        return data

    def toJSON(self) -> Dict[str, Any]:
        return dict(name='trip', scale=self.scale)

    def __call__(self, data: np.ndarray) -> np.ndarray:
        return self.apply(data)

    def __str__(self) -> str:
        return f'Trip({self.scale*100:.2f}% damping)'

def start(args: List[str]) -> Trip:
    """Accepts a list of command line arguments and returns the trippy filter created from those arguments"""
    args = [a.strip() for a in args if a.strip()]
    if not args:
        raise Exception('Missing parameter <scale> ... ')
    n = args[0].strip()
    return Trip(parse_perc(n))