"""The base class for all filters"""

import numpy as np
from typing import List

class Filter(object):
    """
    A filter for raw voice data.
    
    ...

    Methods
    -------
    apply(data: np.ndarray)
        Applies the filter and returns the result.
    """

    def __init__(self):
        raise NotImplementedError()

    def apply(self, data: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def __call__(self, data: np.ndarray) -> np.ndarray:
        return self.apply(data)

    def __str__(self) -> str:
        raise NotImplementedError()

def start(args: List[str]) -> Filter:
    """Accepts a list of command line arguments and returns the filter created from those arguments"""
    raise NotImplementedError()