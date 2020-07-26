"""The base class for all filters"""

import numpy as np
from yapsy.IPlugin import IPlugin

from typing import List, Dict, Any

class Filter(IPlugin):
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

        def toJSON(self) -> Dict[str, Any]:
            raise NotImplementedError()

        def __call__(self, data: np.ndarray) -> np.ndarray:
            return self.apply(data)

        def __str__(self) -> str:
            raise NotImplementedError()
    
    @classmethod
    def start(cls, args: List[str]) -> "Filter.Filter":
        """Accepts a list of command line arguments and returns the filter created from those arguments"""
        pass

    @classmethod
    def html(cls) -> str:
        """Returns the HTML necessary for a configuration form"""
        pass