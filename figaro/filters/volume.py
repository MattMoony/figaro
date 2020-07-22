"""Filter to change the voice's volume"""

import numpy as np, re
from typing import List, Dict, Any

from figaro.utils import parse_perc
from figaro.filters.filter import Filter

class Volume(Filter):
    """
    Changes the volume of raw voice data.
    
    ...

    Attributes
    ----------
    fac : float
        The factor by which to change the volume.

    Methods
    -------
    apply(data: np.ndarray)
        Applies the filter and returns the result.
    """

    def __init__(self, fac: float):
        self.fac: float = fac

    def apply(self, data: np.ndarray) -> np.ndarray:
        return data*self.fac

    def toJSON(self) -> Dict[str, Any]:
        return dict(name='volume', fac=self.fac)

    def __call__(self, data: np.ndarray) -> np.ndarray:
        return self.apply(data)

    def __str__(self) -> str:
        return f'Volume({self.fac*100:.2f}%)'

def start(args: List[str]) -> Volume:
    """Accepts a list of command line arguments and returns the volume filter created from those arguments"""
    args = [a.strip() for a in args if a.strip()]
    if not args:
        raise Exception('Missing parameter <factor> ... ')
    n = args[0].strip()
    return Volume(parse_perc(n))