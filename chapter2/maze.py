from enum import Enum
import random
from math import sqrt
from typing import NamedTuple,List
from generic_search import dfs,node_to_path,bfs,astar

class Cell(str,Enum):
    # 赋值符号后面的值可以通过类名.value取到
    EMPTY = ' '
    BLOCKED = 'X'
    START = 'S'
    GOAL = 'G'
    PATH = '*'

class MazeLocation(NamedTuple):
    row : int
    column : int

class Maze:
    def __init__(self,rows=10,columns=10,sparseness=0.2,
                 start=MazeLocation(0,0),goal=MazeLocation(9,9)):
        self._rows = rows
        self._columns = columns
        self.start = start
        self.goal = goal
        self._grid = [[Cell.EMPTY for c in range(columns)] 
        for r in range(rows)]
        # 随机绘制一个迷宫
        self._randomly_fill(rows,columns,sparseness)
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _randomly_fill(self,rows,columns,sparseness):
        for row in range(rows):
            for column in range(columns):
                # 如果在我们规定的密度以内，这里就画一个障碍
                if random.uniform(0,1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED 
    
    def goal_test(self,ml:MazeLocation):
        '''检查是否走到出口了'''
        return ml == self.goal
    
    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        locations: List[MazeLocation] = []
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if ml.column + 1 < self._columns and self._grid[ml.row][ml.column + 1] !=Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] !=Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations

    def mark(self,path):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = \
                Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL


    def clear(self,path):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = \
                Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] =  Cell.GOAL

    def __str__(self):
        output = ''
        for row in self._grid:
            output += ''.join(c.value for c in row)+'\n'
        return output

def euclidean_distance(goal:MazeLocation):
    '''直线距离'''
    def distance(ml:MazeLocation):
        xdist = ml.column - goal.column
        ydist = ml.row - goal.row
        return sqrt(xdist**2+ydist**2)
    return distance

def manhattan_distance(goal:MazeLocation):
    '''曼哈顿距离，是只能横走竖走的距离'''
    def distance(ml:MazeLocation):
        xdist = abs(ml.column - goal.column)
        ydist = abs(ml.row - goal.row)
        return xdist + ydist
    return distance



if __name__ == '__main__':
    m = Maze()
    distance = manhattan_distance(m.goal)
    solution3 = astar(m.start,m.goal_test,m.successors,distance)
    solution2 = bfs(m.start,m.goal_test,m.successors)
    if solution3 is None:
        print('No solution by A*')
    else:
        print(solution3[1])
    
    if solution2 is None:
        print('No solution by BFS')
    else:
        print(solution2[1])

