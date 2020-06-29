from typing import List
from math import exp

def dot_product(xs: List[float], ys: List[float]) -> float:
    '''两个向量的点乘'''
    return sum(x*y for x, y in zip(xs, ys))

def sigmoid(x: float) -> float:
    '''S型函数，它被用作激励函数'''
    return 1.0 / (1.0+exp(-x))

def derivative_sigmoid(x: float) -> float:
    '''导数'''
    sig: float = sigmoid(x)
    return sig * (1-sig)