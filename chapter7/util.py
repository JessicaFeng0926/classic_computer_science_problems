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

# 假设所有行的长度都是一样的
# 把每一列的特征比例缩放到0-1
def normalize_by_feature_scaling(dataset: List[List[float]]) -> None:
    for col_num in range(len(dataset[0])):
        column: List[float] = [row[col_num] for row in dataset]
        maximum = max(column)
        mininum = min(column)
        for row_num in range(len(dataset)):
            dataset[row_num][col_num] = (dataset[row_num][col_num]-mininum)/(maximum-mininum)

