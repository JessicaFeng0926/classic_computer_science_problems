from random import choice
from string import ascii_uppercase
from typing import Dict,List,NamedTuple,Optional

from csp import CSP,Constraint

Grid = List[List[str]]

class GridLocation(NamedTuple):
    row: int
    column: int

def generate_grid(rows: int, columns: int) -> Grid:
    return [[choice(ascii_uppercase) for c in range(columns)] \
        for r in range(rows)]

def display_grid(grid: Grid) -> None:
    for row in grid:
        print(''.join(row))

def generate_domain(word: str, grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    length: int = len(word)
    for row in range(height):
        for col in range(width):
            columns = range(col,col+length+1)
            rows = range(row,row+length+1)
            if col+length <= width:
                # 从左到右
                domain.append([GridLocation(row,c) for c in columns])
                # 斜着向右下角
                domain.append([GridLocation(r,col+(r-row)) for r in rows])
            if row+length <= height:
                # 从上到下
                domain.append([GridLocation(r,col) for r in rows])
                # 斜着向左下角
                domain.append([GridLocation(r,col-(r-row)) for r in rows])
    return domain

class WordSearchConstraint(Constraint[str,List[GridLocation]]):
    def __init__(self,words: List[str]) -> None:
        super().__init__(words)
        self.words: List[str] = words

    def satisfied(self,assignment: Dict[str, List[GridLocation]]) ->bool:
        # 如果有重复占用的格子，那就是冲突，否则就没有冲突
        all_locations = [locs for values in assignment.values() \
            for locs in values]
        return len(set(all_locations)) == len(all_locations)


if __name__ == '__main__':
    grid: Grid = generate_grid(9,9)
    words: List[str] = ['MATTHEW','JOE','MARY','SARAH','SALLY']
    locations: Dict[str, List[List[GridLocation]]] = {}
    # 这个字典是用于优化的
    cache: Dict[int, List[List[GridLocation]]] = {}
    for word in words:
        # 如果像它这个长度的单词能存放的位置已经保存在缓存字典里了
        # 直接拿出来用
        if (word_length:=len(word)) in cache:
            locations[word] = cache[word_length]
        # 如果第一次遇到这个长度的单词，那就只能调用函数计算可行位置了
        # 但是别忘了往缓存字典里存一份
        else:
            domain = generate_domain(word,grid)
            cache[word_length] = locations[word] = domain
    csp:CSP[str,List[GridLocation]] = CSP(words, locations)
    csp.add_constraint(WordSearchConstraint(words))
    solution:Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print('No solution')
    else:
        for word,grid_locations in solution.items():
            # 随机翻转一半的单词
            if choice([True,False]):
                grid_locations.reverse()
            for index,letter in enumerate(word):
                row,col = grid_locations[index].row,grid_locations[index].column
                grid[row][col] = letter
        display_grid(grid)  
        print(cache.keys())  
    

   

