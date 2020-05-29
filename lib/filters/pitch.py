import numpy as np
from lib.filters.filter import Filter

class Pitch(object):
    def __init__(self, fac: float):
        self.fac: float = fac

    def apply(self, data: np.array) -> np.array:
        freq = np.fft.rfft(data)
        N = len(freq)
        sh_freq = np.zeros(N, freq.dtype)
        S = int(np.round(self.fac if self.fac > 0 else N + self.fac, 0))
        s = int(N-S)
        sh_freq[:S] = freq[s:]
        sh_freq[S:] = freq[:s]
        sh_chunk = np.fft.irfft(sh_freq)
        return sh_chunk.astype(data.dtype)

    def __call__(self, data: np.array) -> np.array:
        return self.apply(data)