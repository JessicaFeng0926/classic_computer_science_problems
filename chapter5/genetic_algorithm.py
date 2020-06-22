from __future__ import annotations
from typing import TypeVar, Generic, List, Tuple, Callable
from enum import Enum
from random import choices, random
from heapq import nlargest
from statistics import mean

from chromosome import Chromosome

C = TypeVar('C', bound=Chromosome)

class GeneticAlgorithm(Generic[C]):
    SelectionType = Enum('SelectionType','ROULETTE TOURNAMENT')

    def __init__(self, initial_population: List[C], threshold: float, 
                 max_generations: int = 100, mutation_chance: float = 0.01,
                 crossover_chance: float = 0.7, 
                 selection_type: SelectionType = SelectionType.TOURNAMENT) -> None:
        self._population: List[C] = initial_population
        self._threshold: float = threshold
        self._max_generations: int = max_generations
        self._mutation_chance: float = mutation_chance
        self._crossover_chance: float = crossover_chance
        self._selection_type: SelectionType = selection_type
        self._fitness_key: Callable = type(self._population[0]).fitness
    
    def _pick_roulette(self, wheel: List[float]) -> Tuple[C, C]:
        # 按照权重来随机选择
        return tuple(choices(self._population, weights=wheel, k=2))

    def _pick_tournament(self, num_participants: int) -> Typle[C, C]:
        # 随机选出候选人，然后选出最好的两个
        participants: List[C] = choices(self._population, k=num_participants)
        return tuple(nlargest(2, participants, key=self._fitness_key))

    def _reproduce_and_replace(self) -> None:
        # 用于保存新一代
        new_population: List[C] = []
        # 一直循环，知道我们填满新一代
        while len(new_population) < len(self._population):
            # 选择父母
            if self._selection_type == GeneticAlgorithm.SelectionType.ROULETTE:
                parents: Tuple[C, C] = self._pick_roulette([x.fitness() for x in self._population])
            else:
                parents: Tuple[C, C] = self._pick_tournament(len(self._population)//2)

            # 按照概率随机选择是生新孩子还是复制父母
            if random()<self._crossover_chance:
                new_population.extend(parents[0].crossover(parents[1]))
            else:
                new_population.extend(parents)
        # 老一代是奇数个，那就会多出来一个，就要移除那个多余的
        if len(new_population) > len(self._population):
            new_population.pop()
        # 新一代替换老一代
        self._population = new_population    

    def _mutate(self) -> None:
        # 随机突变
        for individual in self._population:
            if random() < self._mutation_chance:
                individual.mutate()
    
    def run(self) -> C:
        best: C = max(self._population,key=self._fitness_key)
        for generation in range(self._max_generations):
            # 如果已经找到了超过阈值的个体，提前返回结果
            if best.fitness() >= self._threshold:
                return best
            print(f'Generation {generation} Best {best.fitness()} Avg '
                  f'{mean(map(self._fitness_key,self._population))}')
            self._reproduce_and_replace()
            self._mutate()
            highest: C = max(self._population,key=self._fitness_key)
            if highest.fitness() > best.fitness():
                best = highest
        # 这是我们最终找到的，可能并没有高于阈值
        return best
            
