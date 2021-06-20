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

        @classmethod
        def parse_args(cls, args: List[str]) -> List[Any]:
            """Accepts a list of raw CLI arguments and parses them in accordance to the filter's parameters"""
            pass

        def update(self, *args: List[Any]) -> None:
            """Accepts a list of all the filters parameters and updates them accordingly"""
            raise NotImplementedError()

        def apply(self, data: np.ndarray) -> np.ndarray:
            raise NotImplementedError()

        def toJSON(self) -> Dict[str, Any]:
            raise NotImplementedError()

        def __call__(self, data: np.ndarray) -> np.ndarray:
            return self.apply(data)

        def __str__(self) -> str:
            raise NotImplementedError()

    desc: str = ''
    
    @classmethod
    def start(cls, args: List[str]) -> "Filter.Filter":
        """Accepts a list of command line arguments and returns the filter created from those arguments"""
        pass

    @classmethod
    def props(cls) -> List[Dict[str, Any]]:
        """Returns a list of all parameters and their constraints"""
        pass