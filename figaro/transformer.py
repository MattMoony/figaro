"""
Provides a Transformer for raw audio data.
"""

from threading import Lock
from typing import List, Optional

import numpy as np

from figaro.filters.filter import Filter


class Transformer:
    """
    A transformer for raw audio data - applies effects, etc.
    """

    filters: List[Filter]
    """A list containing all filters."""
    _fil_mut: Lock
    """A mutex for the filter list."""

    def __init__(self, filters: Optional[List[Filter]] = None) -> None:
        """
        Initialize a new Transformer object.

        Args:
            filters: A list of filters to be applied.
        """
        self.filters: List[Filter] = filters or []
        self._fil_mut: Lock = Lock()

    def apply_all(self, data: np.ndarray) -> np.ndarray:
        """
        Apply all filters and return the result.
        
        Args:
            data: The data to be filtered.

        Returns:
            np.ndarray: The filtered data.
        """
        self._fil_mut.acquire()
        for f in self.filters:
            data = f(data)
        self._fil_mut.release()
        return data

    def add_filter(self, f: Filter) -> None:
        """
        Add a filter to the filters list.
        
        Args:
            f: The filter to be added.
        """
        self._fil_mut.acquire()
        self.filters.append(f)
        self._fil_mut.release()

    def del_filter(self, i: int) -> None:
        """
        Remove the filter with the given index from the filter list.

        Args:
            i: The index of the filter to be removed. 
        """
        self._fil_mut.acquire()
        del self.filters[i]
        self._fil_mut.release()

    def __call__(self, data: np.ndarray) -> np.ndarray:
        """
        Apply all filters (calls `apply_all`).

        Args:
            data: The data to be filtered.

        Returns:
            np.ndarray: The filtered data.
        """
        return self.apply_all(data)
