from __future__ import annotations
from typing import List, Optional, Tuple
from enum import Enum
from board import Piece, Board, Move

class C4Piece(Piece, Enum):
    B = 'B'
    R = 'R'
    # 表示空
    E = ' '

    @property
    def opposite(self) -> C4Piece:
        if self == C4Piece.B:
            return C4Piece.R
        elif self == C4Piece.R:
            return C4Piece.B
        else:
            return C4Piece.E

    def __str__(self) -> str:
        return self.value

def generate_segments(num_columns: int, 
                      num_rows: int, 
                      segment_length: int) -> List[List[Tuple[int, int]]]:
    '''生成所有可能会产生胜利结果的部分'''
    segments: List[List[Tuple[int]]] = []
    # 生成纵向的部分
    for c in range(num_columns):
        for r in range(num_rows-segment_length+1):
            segment: List[Tuple[int,int]] = []
            for t in range(segment_length):
                segment.append((c,r+t))
            segments.append(segment)
    # 生成横向的部分
    for c in range(num_columns-segment_length+1):
        for r in range(num_rows):
            segment: List[Tuple[int,int]] = []
            for t in range(segment_length):
                segment.append((c+t,r))
            segments.append(segment)
    # 左下角到右上角(左下角是0的位置)
    for c in range(num_columns-segment_length+1):
        for r in range(num_rows-segment_length+1):
            segment = []
            for t in range(segment_length):
                segment.append((c+t,r+t))
            segments.append(segment)
    # 左上角到右下角
    for c in range(num_columns-segment_length+1):
        for r in range(segment_length-1,num_rows):
            segment = []
            for t in range(segment_length):
                segment.append((c+t,r-t))
            segments.append(segment)
    return segments

class C4Board(Board):
    NUM_ROWS: int = 6
    NUM_COLUMNS: int = 7
    SEGMENT_LENGTH: int = 4
    SEGMENTS: List[List[Tuple[int,int]]] = generate_segments(NUM_COLUMNS,
                                                             NUM_ROWS,
                                                             SEGMENT_LENGTH)

    def __init__(self, position: Optional[List[C4Board.Column]] = None, 
                 turn: C4Piece = C4Piece.B) -> None:
        if position is None:
            self.position: List[C4Board.Column] = [C4Board.Column() for _ in range(C4Board.NUM_COLUMNS)]
        else:
            self.position = position
        self._turn: C4Piece = turn

    @property
    def turn(self) -> Piece:
        return self._turn

    def move(self, location: Move) -> Board:
        temp_position: List[C4Board.Column] = self.position.copy()
        for c in range(C4Board.NUM_COLUMNS):
            temp_position[c] = self.position[c].copy()
        temp_position[location].push(self._turn)
        return C4Board(temp_position,self._turn.opposite)

    @property
    def legal_moves(self) -> List[Move]:
        return [Move(c) for c in range(C4Board.NUM_COLUMNS) if not self.position[c].full] 
    
    def _count_segment(self, segment: List[Tuple[int,int]]) -> Tuple[int,int]:
        '''数出一个能连成4子的部分有多少黑棋和红棋'''
        black_count: int = 0
        red_count: int = 0
        for column, row in segment:
            if self.position[column][row] == C4Piece.B:
                black_count += 1
            elif self.position[column][row] == C4Piece.R:
                red_count += 1
        return black_count, red_count

    @property
    def is_win(self) -> bool:
        for segment in C4Board.SEGMENTS:
            black_count,red_count = self._count_segment(segment)
            # 我把这里的硬编码4，换成了类属性SEGMENT_LENGTH
            if black_count == C4Board.SEGMENT_LENGTH or red_count == C4Board.SEGMENT_LENGTH:
                return True
        return False
    
    def _evaluate_segment(self, segment: List[Tuple[int,int]], 
                          player: Piece) -> float:
        '''计算一个部分的分值'''
        black_count, red_count = self._count_segment(segment)
        # 如果这个小区域里既有黑子又有红子，那就没有用了，所以是0分
        if black_count > 0 and red_count > 0:
            return 0
        count: int = max(red_count,black_count)
        score: float = 0
        # 这个区域只有一种颜色的棋子，并且棋子数量是2，
        # 这个棋子方得1分
        if count == 2:
            score = 1
        elif count == 3:
            score = 100
        elif count == 4:
            score = 1000000
        
        # 得出在这部分占优势的棋子的颜色
        color: C4Piece = C4Piece.B
        if red_count > black_count:
            color = C4Piece.R

        # 如果优势颜色不是我们正在评估的选手
        # 那他就得负分
        if color != player:
            return -score
        return score

    def evaluate(self, player: Piece) -> float:
        '''计算一个选手当前在整盘棋中的总得分'''
        total: float = 0
        for segment in C4Board.SEGMENTS:
            total += self._evaluate_segment(segment,player)
        return total

    def __repr__(self) -> str:
        display: str = ''
        for r in reversed(range(C4Board.NUM_ROWS)):
            display += '|'
            for c in range(C4Board.NUM_COLUMNS):
                display += f'{self.position[c][r]}'+'|'
            display +=  '\n'
        return display

        
        


    class Column:
        def __init__(self) -> None:
            self._container: List[C4Piece] = []

        @property
        def full(self) -> bool:
            return len(self._container) == C4Board.NUM_ROWS

        def push(self, item: C4Piece) -> None:
            if self.full:
                raise OverflowError('Trying to push piece to full column')
            self._container.append(item)

        def __getitem__(self, index: int) -> C4Piece:
            if index > len(self._container)-1:
                return C4Piece.E
            return self._container[index]

        def __repr__(self) -> str:
            return repr(self._container)

        def copy(self) -> C4Board.Column:
            temp: C4Board.Column = C4Board.Column()
            temp._container = self._container.copy()
            return temp
        