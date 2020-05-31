"""Provides a Transformer for raw audio data"""

import numpy as np, json
from typing import List, Optional

from lib.filters.filter import Filter

class Transformer(object):
    """
    A transformer for raw audio data - applies effects, etc.

    ...

    Attributes
    ----------
    filters : List[Filter]
        A list containing all filters.

    Methods
    -------
    apply_all(data: np.ndarray)
        Applies all filters to the given data and returns the result.
    """

    def __init__(self, filters: Optional[List[Filter]] = None):
        self.filters: List[Filter] = filters or []

    def apply_all(self, data: np.ndarray) -> np.ndarray:
        for f in self.filters:
            data = f(data)
        return data

    def __call__(self, data: np.ndarray) -> np.ndarray:
        return self.apply_all(data)