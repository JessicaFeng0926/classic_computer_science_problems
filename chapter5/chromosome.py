from __future__ import annotations
from typing import TypeVar, Tuple, Type
from abc import ABC, abstractmethod

# 第二个参数说明任何用来传给T类型形参的实参
# 要么是Chromosome类的实例要么是它的子类的实例
T = TypeVar('T', bound='Chromosome')

# 染色体基类，所有的方法都是抽象方法，使用的时候都需要覆盖重写
class Chromosome(ABC):

    @abstractmethod
    def fitness(self) -> self:
        ...
    
    @classmethod
    @abstractmethod
    def random_instance(cls: Type[T]) -> T:
        ...

    @abstractmethod
    def crossover(self: T, othter: T) -> Tuple[T, T]:
        ...

    @abstractmethod
    def mutate(self) -> None:
        ...

    
