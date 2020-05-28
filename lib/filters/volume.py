import numpy as np
from lib.filters.filter import Filter

class Volume(Filter):
    def __init__(self, fac: float):
        self.fac: float = fac

    def apply(self, data: np.array) -> np.array:
        return data*self.fac

    def __call__(self, data: np.array) -> np.array:
        return self.apply(data)