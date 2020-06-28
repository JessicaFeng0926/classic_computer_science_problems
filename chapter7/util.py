from typing import List
from math import exp

def dot_product(xs: List[float], ys: List[float]) -> float:
    '''两个向量的点乘'''
    return sum(x*y for x, y in zip(xs, ys))