from typing import Dict,List,Optional

from csp import Constraint,CSP


class MapColoringConstraint(Constraint[str,str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2

    def satisfied(self, assignment: Dict[str,str]) -> bool:
        # 如果还有一个地方没有被涂上颜色，那就不可能冲突
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        # 检查两个地方是否用了不同的颜色
        return assignment[self.place1] != assignment[self.place2]


if __name__ == '__main__':
    variables: List[str] = ['Western Australia',
                            'Northern Territory',
                            'South Australia',
                            'Queensland',
                            'New South Wales',
                            'Victoria',
                            'Tasmania',
                            ]
    domains: Dict[str,List[str]] = {}
    for variable in variables:
        domains[variable] = ['red','green','blue']
    # 用七个州和每个洲可选的三种颜色来初始化一个CSP实例
    csp: CSP[str,str] = CSP(variables,domains)
    
    # 把限制条件加进来，所谓的限制就是两两相邻的州
    csp.add_constraint(MapColoringConstraint('Western Australia','Northern Territory'))
    """ csp.add_constraint(MapColoringConstraint('Western Australia','South Australia'))
    csp.add_constraint(MapColoringConstraint('South Australia','Northern Territory'))
    csp.add_constraint(MapColoringConstraint('Queensland','Northern Territory'))
    csp.add_constraint(MapColoringConstraint('Queensland','South Australia'))
    csp.add_constraint(MapColoringConstraint('Queensland','New South Wales'))
    csp.add_constraint(MapColoringConstraint('New South Wales','South Australia'))
    csp.add_constraint(MapColoringConstraint('Victoria','South Australia'))
    csp.add_constraint(MapColoringConstraint('Victoria','New South Wales'))
    csp.add_constraint(MapColoringConstraint('Victoria','Tasmania')) """

    # 调用回溯法搜索解决方案
    solution: Optional[Dict[str,str]] = csp.backtracking_search()
    if solution is None:
        print('No solution')
    else:
        print(solution)




