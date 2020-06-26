from __future__ import annotations
from typing import Iterator, Tuple, List, Iterable
from math import sqrt

import pandas as pd

class DataPoint:
    def __init__(self, initial: Iterable[float]) -> None:
        self._originals: Tuple[float, ...] = tuple(initial)
        self.dimensions: Tuple[float, ...] = tuple(initial)

    @property
    def num_dimensions(self) -> int:
        return len(self.dimensions)
    
    def distance(self, other: DataPoint) -> float:
        combined: Iterator[Tuple[float, float]] = zip(self.dimensions,other.dimensions)
        differences: List[float] = [(x-y)**2 for x,y in combined]
        return sqrt(sum(differences))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataPoint):
            return NotImplemented
        return self.dimensions == other.dimensions
        
    def __repr__(self) -> str:
        return self._originals.__repr__()


def get_datapoints_from_csv(csv_filepath: str) -> List[DataPoint]:
    '''从csv文件中导入数据获取一系列数据点'''
    df = pd.read_csv(csv_filepath,index_col=False)
    datapoints = []
    for index in range(df.shape[0]):
        datapoints.append(DataPoint(df.loc[index]))
    return datapoints


        
