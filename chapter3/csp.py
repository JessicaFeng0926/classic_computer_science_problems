from abc import ABC,abstractmethod
from typing import Generic,TypeVar,Dict,List,Optional

# 变量类型
V = TypeVar('V')
# domain类型
D = TypeVar('D')


# 这是一个抽象基类
class Constraint(Generic[V,D],ABC):
    def __init__(self, variables: List[V]) -> None:
        # 这里的变量是冲突的变量
        self.variables = variables
    
    # 子类必须覆盖
    @abstractmethod
    def satisfied(self, assignment: Dict[V,D]) -> bool:
        ...


class CSP(Generic[V,D]):
    def __init__(self, variables: List[V], domains: Dict[V,List[D]]) -> None:
        # 这里的变量是全部的变量
        self.variables: List[V] = variables
        self.domains: Dict[V,List[D]] = domains
        self.constraints: Dict[V,List[Constraint[V,D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError('Every variable should have a domain assigned to it.')

    def add_constraint(self, constraint: Constraint[V,D]) -> None:
        '''把限制条件加进来'''
        for variable in constraint.variables:
            # 不能加无关的变量
            if variable not in self.variables:
                raise LookupError('Variable in constraint not in CSP.')
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable: V, assignment: Dict[V,D]) -> bool:
        '''检查目前的安排对当前这个变量来说是否合理'''
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment: Dict[V,D] = {}) -> Optional[Dict[V,D]]:
        # 如果每个变量都被安排了，那么安排就完成了
        if len(assignment) == len(self.variables):
            return assignment

        # 获取所有还没有安排的变量
        unassigned = [v for v in self.variables if v not in assignment]

        # 获取第一个未排定的变量所有可能的值
        first: V = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            # 如果还是一致的，递归
            if self.consistent(first, local_assignment):
                result: Optional[Dict[V,D]] = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None
