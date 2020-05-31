"""Filter to change the voice's volume"""

import numpy as np
from lib.filters.filter import Filter

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

    def __call__(self, data: np.ndarray) -> np.ndarray:
        return self.apply(data)