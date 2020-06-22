from typing import List,Dict,Optional

from csp import Constraint,CSP

class QueensConstraint(Constraint[int,int]):
    def __init__(self,columns: List[int]) -> None:
        super().__init__(columns)
        self.columns = columns

    def satisfied(self,assignment: Dict[int,int]) -> bool:
        # q1c 是 queen 1 column, q1r 是 queen 1 row
        for q1c,q1r in assignment.items():
            for q2c in range(q1c+1,len(self.columns)+1):
                if q2c in assignment:
                    q2r = assignment[q2c]
                    # 在同一行，返回False
                    if q1r == q2r:
                        return False
                    # 在同一条斜线上，返回False
                    if abs(q1c-q2c) == abs(q1r-q2r):            
                        return False
        # 没有冲突
        return True

if __name__ == '__main__':
    # 列是变量
    columns: List[int] = [1,2,3,4,5,6,7,8]
    # 行是地域
    rows: Dict[int,List[int]] = {}
    for column in columns:
        rows[column] = [1,2,3,4,5,6,7,8]
    csp: CSP[int,int] = CSP(columns,rows)
    csp.add_constraint(QueensConstraint(columns))
    solution: Optional[Dict[int,int]] = csp.backtracking_search()
    if solution is None:
        print('No solution')
    else:
        print(solution)

    