"""The base class for all filters"""

import numpy as np

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
        pass

    def apply(self, data: np.ndarray) -> np.ndarray:
        pass

    def __call__(self, data: np.ndarray) -> np.ndarray:
        return self.apply(data)

    def __str__(self) -> str:
        return 'Filter-Blueprint'