"""Filter to change the voice's pitch"""

import numpy as np
from typing import List, Dict, Any

from lib.utils import parse_perc
import lib.filters.filter

class Pitch(lib.filters.filter.Filter):
    class Filter(lib.filters.filter.Filter.Filter):
        """
        Changes the pitch of raw voice data.
        
        ...
    
        Attributes
        ----------
        fac : float
            The factor by which to change the pitch.
    
        Methods
        -------
        apply(data: np.ndarray)
            Applies the filter and returns the result.
        """
    
        def __init__(self, fac: float):
            self.fac: float = fac

        @classmethod
        def parse_args(cls, args: List[str]) -> List[Any]:
            args = [a.strip() for a in args if a.strip()]
            if not args:
                raise Exception('Missing parameter <factor> ... ')
            return [parse_perc(args[0].strip()),]

        def update(self, *args: List[Any]) -> None:
            self.fac = args[0]
    
        def apply(self, data: np.ndarray) -> np.ndarray:
            freq = np.fft.rfft(data)
            N = len(freq)
            sh_freq = np.zeros(N, freq.dtype)
            S = int(np.round(self.fac if self.fac > 0 else N + self.fac, 0))
            s = int(N-S)
            sh_freq[:S] = freq[s:]
            sh_freq[S:] = freq[:s]
            sh_chunk = np.fft.irfft(sh_freq)
            return sh_chunk.astype(data.dtype)
    
        def toJSON(self) -> Dict[str, Any]:
            return dict(name='Pitch', fac=self.fac)
    
        def __call__(self, data: np.ndarray) -> np.ndarray:
            return self.apply(data)
    
        def __str__(self) -> str:
            return f'Pitch({self.fac*100:.2f}%)'

    desc: str = 'Changes your voice\'s pitch!'

    @classmethod
    def start(cls, args: List[str]) -> "Pitch.Filter":
        return Pitch.Filter(*Pitch.Filter.parse_args(args))

    @classmethod
    def props(cls) -> List[Dict[str, Any]]:
        return [dict(name='fac', min=-30, max=30, step=1, value=0),]