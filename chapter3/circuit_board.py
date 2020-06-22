from typing import Dict,List,NamedTuple,Optional

from csp import CSP,Constraint

Grid = List[List[str]]

class GridLocation(NamedTuple):
    row: int
    column: int

def generate_grid(rows: int, columns: int) -> Grid:
    '''空板用0来填充'''
    return [['0' for c in range(columns)] for r in range(rows)]

def display_grid(grid: Grid) -> None:
    for row in grid:
        print(''.join(row))

def generate_domain(chip: str, grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    # 整块电路板的宽高
    height: int = len(grid)
    width: int = len(grid[0])
    # 这块芯片的宽高
    h: int = int(chip[-1])
    w: int = int(chip[-2])

    for row in range(height):
        for col in range(width):
            # 从左到右
            if col+w <= width and row+h <= height:
                domain.append([GridLocation(r,c) \
                    for r in range(row,row+h) \
                        for c in range(col,col+w)])
            # 如果芯片宽高不一样，再添加从上到下
            if h != w and col+h <= width and row+w <= height:
                domain.append([GridLocation(r,c) \
                    for r in range(row,row+w) \
                        for c in range(col,col+h)])
    return domain

class CircuitBoardConstraint(Constraint[str,List[GridLocation]]):
    def __init__(self,chips: List[str]) -> None:
        super().__init__(chips)
        self.chips: List[str] = chips

    def satisfied(self,assignment: Dict[str, List[GridLocation]]) ->bool:
        # 如果有重复占用的格子，那就是冲突，否则就没有冲突
        all_locations = [locs for values in assignment.values() \
            for locs in values]
        return len(set(all_locations)) == len(all_locations)


if __name__ == '__main__':
    grid: Grid = generate_grid(9,9)
    # 芯片的第0个字符代表芯片的颜色，后面两个字符代表芯片的宽和高
    chips: List[str] = ['A94','B33','D61','E25']
    locations: Dict[str, List[List[GridLocation]]] = {}
    # 这个字典用于优化
    cache: Dict[str,List[List[GridLocation]]] = {}

    # 把可行的domain添加到字典locations里面
    for chip in chips:
        width = int(chip[-2])
        height = int(chip[-1])
        # 一定要保证宽比高长
        if width < height:
            width,height = height,width
        if key:= f'{width}{height}' in cache:
            locations[chip] = cache[key]
        else:
            locations[chip] = cache[key] = generate_domain(chip,grid)
    csp: CSP[str,List[GridLocation]] = CSP(chips,locations)
    csp.add_constraint(CircuitBoardConstraint(chips))
    solution:Optional[Dict[str,List[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print('No solution')
    else:
        for chip,grid_locations in solution.items():
            for grid_location in grid_locations:
                grid[grid_location.row][grid_location.column] = chip[0]
        display_grid(grid)
    
    
    
         


