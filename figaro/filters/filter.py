"""
The base class for all filters.
"""

from typing import Any, Dict, List

import numpy as np
from yapsy.IPlugin import IPlugin


class Filter(IPlugin):
    """
    A filter plugin.
    """

    desc: str = ''
    """The filter plugin's description. Default is empty string."""

    class Filter:
        """
        A filter for raw voice data.
        """


        def __init__(self) -> None:
            raise NotImplementedError()

        @classmethod
        def parse_args(cls, args: List[str]) -> List[Any]:
            """
            Accepts a list of raw CLI arguments and parses them in accordance to the filter's parameters.
            
            Args:
                args (List[str]): The raw CLI arguments.

            Returns:
                List[Any]: The parsed arguments.
            """
            pass

        def update(self, *args: List[Any]) -> None:
            """
            Accepts a list of all the filters parameters and updates them accordingly.
            
            Args:
                args (List[Any]): The new values for the filters parameters.
            """
            raise NotImplementedError()

        def apply(self, data: np.ndarray) -> np.ndarray:
            """
            Apply the filter to the given data.

            Args:
                data (np.ndarray): The data to apply the filter to.

            Returns:
                np.ndarray: The filtered data.
            """
            raise NotImplementedError()

        def toJSON(self) -> Dict[str, Any]:
            """
            Converts the filter to a JSON object.

            Returns:
                Dict[str, Any]: The filter as a JSON object.
            """
            raise NotImplementedError()

        def __call__(self, data: np.ndarray) -> np.ndarray:
            """
            Wrapper around `apply` to allow for the filter to be called like a function.

            Args:
                data (np.ndarray): The data to apply the filter to.
            
            Returns:
                np.ndarray: The filtered data.
            """
            return self.apply(data)

        def __str__(self) -> str:
            raise NotImplementedError()
    
    @classmethod
    def start(cls, args: List[str]) -> "Filter.Filter":
        """
        Accepts a list of command line arguments and returns the filter created from those arguments.

        Args:
            args (List[str]): The command line arguments.

        Returns:
            Filter.Filter: The filter created from the arguments.
        """
        pass

    @classmethod
    def props(cls) -> List[Dict[str, Any]]:
        """
        Returns a list of all parameters and their constraints.

        Returns:
            List[Dict[str, Any]]: A list of all parameters and their constraints.
        """
        pass
