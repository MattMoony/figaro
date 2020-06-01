"""Provides a Transformer for raw audio data"""

import numpy as np, json
from threading import Lock
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
    _fil_mut : Lock
        A mutex for the filter list.

    Methods
    -------
    apply_all(data: np.ndarray)
        Applies all filters to the given data and returns the result.
    """

    def __init__(self, filters: Optional[List[Filter]] = None):
        self.filters: List[Filter] = filters or []
        self._fil_mut: Lock = Lock()

    def apply_all(self, data: np.ndarray) -> np.ndarray:
        """Apply all filters and return the result"""
        self._fil_mut.acquire()
        for f in self.filters:
            data = f(data)
        self._fil_mut.release()
        return data

    def add_filter(self, f: Filter) -> None:
        """Add a filter to the filters list"""
        self._fil_mut.acquire()
        self.filters.append(f)
        self._fil_mut.release()

    def del_filter(self, i: int) -> None:
        """Remove the filter with the given index from the filter list"""
        self._fil_mut.acquire()
        del self.filters[i]
        self._fil_mut.release()

    def __call__(self, data: np.ndarray) -> np.ndarray:
        """Apply all filters (calls `apply_all`)"""
        return self.apply_all(data)